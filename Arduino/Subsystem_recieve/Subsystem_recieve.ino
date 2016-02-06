#include <Wire.h>
#define ARRAY_LEN 10

uint8_t pins[] = {2, 5, 4, 3};

int vals[ARRAY_LEN] = {0};
int new_val = 1;
int avg = 1;


void setup()
{
  int pincount  = sizeof(pins);
  pinMode(A0, INPUT);
  pinMode(13, OUTPUT);
  pinMode(8, OUTPUT);
  for(int i = 0; i < pincount; i++)
    pinMode(pins[i], OUTPUT);
  
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Wire.onRequest(requestEvent);
  
  Serial.begin(57600);           // start serial for output
}

void loop()
{
  // shift array one place to right
  for(int i = ARRAY_LEN - 1; i > 0; i--)
    vals[i] = vals[i-1];

  // get latest reading and insert into array
  cli();
  vals[0] = analogRead(A0);
  sei();
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
  cli();
  if(howMany > 0){
    char* separator = strchr(str, ':');
    *separator = 0;
    char* ident = str;
    ++separator;
    
    if(strcmp(ident, "LED") == 0){
      int value = atoi(separator);
      int led = value / 10;
      int val = value % 10;
      if(led == 1)
        changeLED0(val);
      else if(led == 2)
        changeLED1(val);
    }
    else if(strcmp(ident, "RCV") == 0){
      if(strcmp(separator, "IDENT") == 0){

      }
    }
    

  sei();
  }
}

void requestEvent(void)
{
  int sum = 0;
  // get sum of latest array
  for(int i = 0; i < ARRAY_LEN; i++)
    sum += vals[i];
  // get current average
  avg = sum/ARRAY_LEN;

  // Deal with incorrect values
  if(avg >= 1024)
    avg = 1023;
  // Zeros will not send correctly, set to one
  else if(avg <= 0)
    avg = 1;

  // Create two bytes to send
  uint8_t buff[2];
  // Low byte
  buff[0] = avg >> 8;
  // High byte
  buff[1] = avg & 0xff;
  Wire.write(buff, 2);
}

void changeLED0(int value)
{
  if(value % 2 == 0)
    //digitalWrite(13, LOW);
    PORTB = PORTB & B11011111;
  else
    //digitalWrite(13, HIGH);
    PORTB = PORTB | B00100000;
}

void changeLED1(int value)
{
  if(value % 2 == 0)
    //digitalWrite(8, LOW);
    PORTB = PORTB & B11111110;
  else
    //digitalWrite(8, HIGH);
    PORTB = PORTB | B00000001;
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

