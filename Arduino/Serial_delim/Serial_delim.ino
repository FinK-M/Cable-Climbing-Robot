#define INPUT_SIZE 24
#include <Wire.h>
<<<<<<< HEAD

void setup() {
  // Serial 1 is for Xbee Module
  Serial1.begin(57600);
  // Must set short timeout otherwise will hang when reading data
  Serial1.setTimeout(5);
  // Debug Serial port setup
  Serial.begin(57600);
  // Start I2C
  Wire.begin();
}

void send(int message, int address){
  Wire.beginTransmission(address); // transmit to device a
  Wire.write(message);       // sends one byte
  Wire.endTransmission();    // stop transmitting
}

void loop() {
<<<<<<< HEAD
  if(Serial1.available()){
    // Get next command from Serial (add 1 for final 0)
    char input[INPUT_SIZE + 1];
    byte size = Serial1.readBytes(input, INPUT_SIZE);
    // Add the final 0 to end the C string
    input[size] = 0;
    
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
            int value = atoi(separator);
    
            // Send the LED value to the appropriate subsystem
            if(strcmp(ident, "LED") == 0){
              send(value, 8);
            }
            // Send the servo position to the appropriate subsystem
            else if(strcmp(ident, "SER") == 0){
              send(value, 9);
            }
        }
        // Find the next command in input string
        command = strtok(0, ",");
    }
    Wire.beginTransmission(8);
    int available = Wire.requestFrom(8, (uint8_t)2);
    if(available == 2)
    {
      int receivedValue = Wire.read() << 8 | Wire.read();
      Serial1.print(receivedValue);
      Serial.print(receivedValue);
    }
    else
    {
      Serial1.print("Incorrect number of bytes: ");
      Serial1.print(available);
      Serial.print("Incorrect number of bytes: ");
      Serial.print(available);
    }

    Wire.endTransmission();
    Serial1.println(",ack");
    Serial.println(",ack");
  }
}
