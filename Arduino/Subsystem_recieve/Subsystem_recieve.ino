#include <Wire.h>

int pins[] = {2, 5, 4, 3};

void setup()
{

  int pincount  = sizeof(pins);
  pinMode(A0, INPUT);
  pinMode(13, OUTPUT);
  for(int i = 0; i < pincount; i++)
    pinMode(pins[i], OUTPUT);
  
  Wire.begin(8);                // join i2c bus with address #8
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
  char buff[2];
  char str[80] = "";
  while (Wire.available()) // loop through all but the last
  {
    sprintf(buff, "%c", Wire.read());      // receive byte as a character
    strcat(str, buff);
  }
  if(howMany > 0){
    char* separator = strchr(str, ':');
    *separator = 0;
    char* ident = str;
    ++separator;
    int value = atoi(separator);
    Serial.println(value);
    changeLED(value);
  }
}

void requestEvent(void)
{
  int input = analogRead(A0);
  if(input >= 1024)
    input = 1023;
  else if(input <= 0)
    input = 1;
  uint8_t buffer[2];
  buffer[0] = input >> 8;
  buffer[1] = input & 0xff;
  Wire.write(buffer, 2);
}

void changeLED(int value)
{
  if(value % 2 == 0)
    PORTB = PORTB & B11000000;
  else
    PORTB = PORTB | B00100000;
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

