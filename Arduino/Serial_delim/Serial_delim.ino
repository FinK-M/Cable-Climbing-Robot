#define INPUT_SIZE 100
#define UNO_0_ADR 8
#define UNO_1_ADR 9

#include <Wire.h>

void setup() {
  pinMode(22, OUTPUT);
  pinMode(23, OUTPUT);
  delay(100);
  pinMode(22, INPUT);
  pinMode(23, INPUT);

  pinMode(9, OUTPUT);
  tone(9, 523, 300);
  delay(50);
  // Serial 1 is for Xbee Module
  Serial1.begin(57600);
  // Must set short timeout otherwise will hang when reading data
  Serial1.setTimeout(5);
  // Debug Serial port setup
  Serial.begin(57600);
  // Start I2C
  Wire.begin();
  tone(9, 1046, 300);
}

void send(char* message, int address, char* type){
  // type variable checks if to convert string to an integer first or not
  Wire.beginTransmission(address);  // transmit to device at address
  if(type == "int")
  {
    Wire.write(atoi(message));
  }
  else
    Wire.write(message);          // send message byte by byte
  Wire.endTransmission();         // stop transmitting
  Wire.flush();
}

int get_adc_val(int address){
    int receivedValue = 0;
    Wire.beginTransmission(address);
    int available = Wire.requestFrom(address, (uint8_t)2);
    if(available == 2)
    {
      receivedValue = Wire.read() << 8 | Wire.read();
      Serial1.print(receivedValue);
    }
    else
    {
      Serial1.print("Incorrect number of bytes: ");
      Serial1.print(available);
    }
    Wire.endTransmission();
    Serial1.println(",ack");
    return receivedValue;
}


void loop() {
  if(Serial1.available()) {
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
            char* value = separator;
    
            // Send the LED value to the appropriate subsystem
            if(strcmp(ident, "LED") == 0){
              char msg[6];
              sprintf(msg, "LED:%s", value);
              send(msg, UNO_0_ADR, "char");
            }
            // Send the servo position to the appropriate subsystem
            else if(strcmp(ident, "SER") == 0){
              send(value, UNO_1_ADR, "int");
            }
            
            else if(strcmp(ident, "RST") == 0){
                pinMode(24, OUTPUT);
            }
            
            // Get an ADC value fr
            else if(strcmp(ident, "ADC") == 0){
              // Value is address, so need to convert from char* to int
              get_adc_val(atoi(value));
            }
        }
        // Find the next command in input string
        command = strtok(0, ",");
    }
  }
}
