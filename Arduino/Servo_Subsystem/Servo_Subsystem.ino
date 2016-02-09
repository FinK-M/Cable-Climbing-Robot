#include <Wire.h>

#define DIR 4
#define STEP 8

volatile int pulse_count = 0;
volatile int max_pulses;
volatile boolean continuous = false;

uint8_t last_rpm = 0;
uint8_t rpm = 0;

void setup()
{

  pinMode(DIR, OUTPUT);
  pinMode(STEP, OUTPUT);
  
  digitalWrite(DIR, HIGH);
  
  Wire.begin(9);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Wire.onRequest(requestEvent);
  
  Serial.begin(57600);           // start serial for output
}

void loop()
{
  delay(100);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany)
{
  while (Wire.available()) // loop through all but the last
  {
    rpm = Wire.read(); // receive byte as a character
    if(rpm != last_rpm)
    {
      start_run(rpm);
      last_rpm = rpm;
    }
    Serial.println(rpm);         // print the character
  }
}

void requestEvent(void)
{
  int input = analogRead(A0);
  if(input >= 1024)
    input = 1023;
  if(input <= 0)
    input = 1;
  uint8_t buffer[2];
  buffer[0] = input >> 8;
  buffer[1] = input & 0xff;
  Wire.write(buffer, 2);

}

int get_match(int rpm){
  float pulse = 60.0*1000000.0/200.0/(float)rpm/2.0;
  return (int) (16000000.0/(1000000.0/pulse*256.0) - 1.0);
}

void start_run(int rpm){
  //stop interrupts
  cli();
  // set entire TCCR2A register to 0
  TCCR2A = 0;
  // same for TCCR2B
  TCCR2B = 0;
  //initialize counter value to 0
  TCNT2  = 0;
  // match based on pulse length for given rpm
  OCR2A = get_match(rpm);
  // turn on CTC mode
  TCCR2A |= (1 << WGM21);
  // Set CS01 and CS00 bits for 64 prescaler
  TCCR2B |= (1<<CS22) | (1<<CS21);
  // enable timer compare interrupt
  TIMSK2 |= (1 << OCIE2A);
  //start interrupts
  sei();

}

void stop_run(){
  // Disable timer 2 compare interrupts
  TIMSK2 &= (0 << OCIE2A);
}

void move_steps(int steps, int rpm){
  // Enable pulse count checking
  continuous = false;
  // Reset pulse count
  pulse_count = 0;
  // Each step is two pulses
  max_pulses = steps * 2;
  //Start rotation
  start_run(rpm);
}

void move_angle(int angle, int rpm){
  // Number of steps is angle/360 times number of steps in one rotation
  move_steps((int)((float)angle/360.0 * 200.0), rpm);
}

ISR(TIMER2_COMPA_vect)
{
  // Flip pin 8 state
  PORTB ^= B00000001;
  // Increment total pulse count
  pulse_count++;

  // Only stop if not running in continuous mode
  if(!continuous && pulse_count == max_pulses)
  {
    // Disable timer 2 compare interrupts
    TIMSK2 &= (0 << OCIE2A);
    // Reset to continuous mode
    continuous = true;
  }
}