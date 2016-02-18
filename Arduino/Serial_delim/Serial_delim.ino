#define INPUT_SIZE 100
#define UNO_0_ADR 8
#define UNO_1_ADR 9

#define DIR 42
#define STEP 41
#define RST 40

#include <Wire.h>

unsigned long last_time = 0;

bool ready_flag = false;
int dir = 1;

char* servo_msg;
int servo_value = 0;
int last_servo_value;
char* led_state;
char* adc_msg;
int send_number = 0;

volatile unsigned long pulse_count = 0;
volatile unsigned long max_pulses;
volatile bool continuous = false;

volatile long stepper_position = 0;
volatile long encoder_position = 0;

void setup() {

  // Reset Arduino Unos
  DDRA |= B00000011;
  delay(100);
  DDRA &= B11111100;

  delay(50);
  // Serial 1 is for Xbee Module
  Serial1.begin(57600);
  // Must set short timeout otherwise will hang when reading data
  Serial1.setTimeout(5);
  // Debug Serial port setup
  Serial.begin(57600);
  // Start I2C
  Wire.begin();
  
  // Stepper motor pins
  pinMode(RST, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(STEP, OUTPUT);

  // Reset stepper drivers
  digitalWrite(RST, LOW);
  delay(100);
  digitalWrite(RST, HIGH);
  
  // Set to forward motion
  digitalWrite(DIR, HIGH);
  
}

void send(char* message, int address, char* type){
  // type variable checks if to convert string to an integer first or not
  Wire.beginTransmission(address);  // transmit to device at address
  if(type == "int")
  {
    // Convert string to integer
    int val = atoi(message);
    // Create array for high and low bytes
    uint8_t buff[2];
    // Split integer into high and low bytes
    buff[0] = val >> 8;
    buff[1] = val & 0xff;
    // Send both bytes
    Wire.write(buff, 2);
  }
  else
    Wire.write(message);          // send message byte by byte
  Wire.endTransmission();         // stop transmitting
  //Wire.flush();
}

int get_adc_val(int address){
    int receivedValue = 0;
    Wire.beginTransmission(address);
    int available = Wire.requestFrom(address, (uint8_t)2);
    if(available == 2)
    {
      receivedValue = Wire.read() << 8 | Wire.read();
      Serial1.print("a");
      Serial1.print(receivedValue);
      Serial1.println(",ack");
    }
    else
    {
      Serial1.print("Incorrect number of bytes: ");
      Serial1.print(available);
    }
    Wire.endTransmission();
    return receivedValue;
}

void serialEvent1(){

  if(Serial1.available())
  {
    // Get next command from Serial (add 1 for final 0)
    char input[INPUT_SIZE + 1];
    byte size = Serial1.readBytes(input, INPUT_SIZE);
    // Add the final 0 to end the C string
    input[size] = 0;
    while(Serial1.available())
    {
        Serial1.read();
    }
    
    // Read each command pair 
    char* command = strtok(input, ",");
    while (command != 0)
    {
      // Split the command in two values
      char* separator = strchr(command, ':');
      if (separator != 0)
      {
          // Actually split the string in 2: replace ':' with 0
          *separator = 0;
          char* ident = command;
          ++separator;
          char* value = separator;

          // Send the LED value to the appropriate subsystem
          if(strcmp(ident, "LED") == 0){
            led_state = value;
            
            /*
            char msg[6];
            sprintf(msg, "LED:%s", value);
            send(msg, UNO_0_ADR, "char");
            */
            
          }
          // Number of measurement intervals before next instruction
          else if(strcmp(ident, "INT") == 0){
            send_number = atoi(value);
          }

          else if(strcmp(ident, "DIR") == 0){
            dir = atoi(value);
          }


          else if(strcmp(ident, "RUN") == 0){
            if(strcmp(value, "1") == 0){
              ready_flag = true;
            }
          }
          // Send the servo position to the appropriate subsystem
          else if(strcmp(ident, "SER") == 0){
            servo_msg = ident;
            servo_value = atoi(value);
            //send(value, UNO_1_ADR, "int");
          }
          
          else if(strcmp(ident, "RST") == 0){
              pinMode(24, OUTPUT);
          }
          
          // Get an ADC value fr
          else if(strcmp(ident, "ADC") == 0){
            adc_msg = value;
            // Value is address, so need to convert from char* to int
            // get_adc_val(atoi(value));
          }
          
      }
      // Find the next command in input string
      command = strtok(0, ",");
    }
  }
}

void loop(){
  if(ready_flag)
  {
    digitalWrite(DIR, dir);
    start_run(servo_value);
    for(int i = 0; i < send_number; i++)
    {
      delay(3);
      if(i % 50 == 0)
      {
        Serial1.print("sSP:");
        Serial1.print(stepper_position);
        Serial1.print(",EP:");
        Serial1.println(encoder_position);
      }
      Serial1.print("v");
      Serial1.print(analogRead(A0));
      Serial1.print(",");
      Serial1.print(analogRead(A1));
      Serial1.print(",");
      Serial1.println(analogRead(A2));
      
    }
    stop_run();
    Serial1.println("ack");
    ready_flag = false;
  }
  else
  {
    stop_run();
    last_servo_value = 0;
  }
}

int get_match(int rpm){
  float pulse = 60.0*1000000.0/200.0/(float)rpm/2.0;
  return (int) (16000000.0/(1000000.0/pulse*256.0) - 1.0);
}

void start_run(int rpm){


  //stop interrupts
  cli();
  // If stopping
  if(rpm == 0)
    stop_run();
  // Otherwise set RPM
  else
  {
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
  }
  //start interrupts
  sei();
}

void stop_run(){
  // Disable timer 2 compare interrupts
  TIMSK2 &= (0 << OCIE2A);
  //
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
  int x = 0;
  while(pulse_count < max_pulses)
    x = x;
}

void move_angle(int angle, int rpm){
  // Number of steps is angle/360 times number of steps in one rotation
  move_steps((int)((float)angle/360.0 * 200.0), rpm);
}

ISR(TIMER2_COMPA_vect){
  // Flip pin 41 state
  PORTG ^= B00000001;
  // Increment total pulse count
  pulse_count++;

  if(dir)
    stepper_position += pulse_count * 2;
  else
    stepper_position -= pulse_count * 2;

  // Only stop if not running in continuous mode
  if(!continuous && pulse_count == max_pulses)
  {
    // Disable timer 2 compare interrupts
    TIMSK2 &= (0 << OCIE2A);
    // Reset to continuous mode
    continuous = true;
  }
}
