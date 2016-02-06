#include <Wire.h>
#define DIR 8
#define STEP 9

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
      set_speed(rpm);
      last_rpm = rpm;
    }
    Serial.print(rpm);         // print the character
  }
}

void requestEvent(void)
{
  Serial.println("Requested");
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
  int pulse = 60*1000000L/200/rpm/2;
  return 16000000.0/(1000000/(float)pulse*1024.0) - 1;
}

void set_speed(int rpm){
  //stop interrupts
  cli();
  // set entire TCCR1A register to 0
  TCCR1A = 0;
  // same for TCCR1B
  TCCR1B = 0;
  //initialize counter value to 0
  TCNT1  = 0;
  // set compare match register for 1hz increments
  OCR1A = get_match(rpm);
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS12 and CS10 bits for 1024 prescaler
  TCCR1B |= (1 << CS12) | (1 << CS10);  
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);
  //start interrupts
  sei();
}

ISR(TIMER1_COMPA_vect)
{
  PORTB ^= B00000010;
}