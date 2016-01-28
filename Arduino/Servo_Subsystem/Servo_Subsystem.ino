#include <Wire.h>
#include <Servo.h>

Servo myservo;

uint8_t last_pos = 0;
uint8_t pos = 0;

void setup()
{
  myservo.attach(3);
  
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
    pos = Wire.read(); // receive byte as a character
    if(pos != last_pos)
    {
      myservo.write(pos);
      last_pos = pos;
    }
    Serial.print(pos);         // print the character
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
