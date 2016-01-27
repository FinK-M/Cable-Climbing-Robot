
// Written by Nick Gammon
// February 2011


#include <SPI.h>

uint8_t i = 0;

void setup (void)
{
  Serial1.begin(115200);
  digitalWrite(SS, HIGH);  // ensure SS stays high for now

  // Put SCK, MOSI, SS pins into output mode
  // also put SCK, MOSI into LOW state, and SS into HIGH state.
  // Then put SPI hardware into Master mode and turn SPI on
  SPI.begin ();

  // Slow down the master a bit
  SPI.setClockDivider(SPI_CLOCK_DIV8);
  
}  // end of setup


void loop (void)
{

  char c;
  char num[2];
  itoa(i++, num, 10);
  if(i > 10)
    i = 0;

  // enable Slave Select
  digitalWrite(SS, LOW);    // SS is pin 10

  // send test string
  for (const char * p = "Hello, world!\n" ; c = *p; p++)
    SPI.transfer (c);
  Serial1.print("Hello World");
  // disable Slave Select
  digitalWrite(SS, HIGH);

  delay (1000);  // 1 seconds delay 
}  // end of loop