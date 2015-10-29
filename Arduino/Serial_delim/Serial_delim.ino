#define INPUT_SIZE 24
#include <SoftwareSerial.h>
#include <Wire.h>
SoftwareSerial serial1(8, 9); // RX, TX

void setup() {
  // put your setup code here, to run once:
  serial1.begin(19200);
  Serial.begin(19200);
  Wire.begin();
}

void send(int message, int address){
  
  Wire.beginTransmission(address); // transmit to device a
  Wire.write(message);       // sends one byte
  Wire.endTransmission();    // stop transmitting
}

void loop() {
  if(serial1.available()){
  
    // Get next command from Serial (add 1 for final 0)
    char input[INPUT_SIZE + 1];
    byte size = serial1.readBytes(input, INPUT_SIZE);
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
    
            // Do something with servoId and position
            if(strcmp(ident, "LED") == 0){
              Serial.println("Sending");
              send(value, 8);
            }
            Serial.print(ident);
            Serial.print(" ");
            Serial.println(value);
        }
        // Find the next command in input string
        command = strtok(0, ",");
    }
    delay(100);
    Wire.beginTransmission(8);
    int available = Wire.requestFrom(8, (uint8_t)2);
    delay(100);
    if(available == 2)
    {
      int receivedValue = Wire.read() << 8 | Wire.read();
      serial1.print(receivedValue);
    }
    else
    {
      serial1.print("Incorrect number of bytes: ");
      serial1.print(available);
    }

    Wire.endTransmission();
    delay(100);
    serial1.println(",ack");
    Serial.println("");
  }
}
