#include <Wire.h>

int pins[] = {2, 5, 4, 3};

void setup()
{

  int pincount  = sizeof(pins);
  pinMode(A0, INPUT);
  for(int i = 0; i < pincount; i++)
    pinMode(pins[i], OUTPUT);
  
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Wire.onRequest(requestEvent);
  
  Serial.begin(19200);           // start serial for output
}

void loop()
{
  
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany)
{
  int x = 0;
  while (Wire.available()) // loop through all but the last
  {
    x = Wire.read();       // receive byte as a character
    updateDisplay(x);
    Serial.print(x);       // print the character
  }
  if(x == 9)
    Serial.println("");
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

void updateDisplay(int value)
{
  if(value >= 0 && value <= 10)
  {
    int bits[4] = {0,0,0,0};
    int result[4] = {0,0,0,0};
    for (int i=3; i >= 0; i--){
      bits[i] = value % 2;
      value /= 2;
      result[3 - i] = bits[i];
    }
    for (int i=0; i < 4; i++)
      digitalWrite(pins[i], result[i]);
  }
}

