#define INPUT_SIZE 100

#define DIR 42
#define STEP 6
#define RST 40
#define M0 51
#define M1 52
#define M2 53

volatile bool ready_flag = false;
volatile bool jog_mode = false;
volatile bool stopped = true;

int dir = 1;

int stop_value = 0;
int stepper_value = 0;
int send_number = 0;

volatile long stepper_position = 0;
volatile long encoder_position = 0;
long pos = 0;

volatile uint8_t mux = 5;
volatile uint8_t microsteps = 2;
uint8_t temp = 0;

// Value to store analogue results
volatile int analogVal0;
volatile int analogVal1;
volatile int analogVal2;

void setup(){

  attachInterrupt(digitalPinToInterrupt(2), end_stop, RISING);

  setup_stepper();
  setup_microstep(microsteps);
  setup_adc();

  // Serial 1 is for Xbee Module
  Serial1.begin(57600);
  // Must set short timeout otherwise will hang when reading data
  Serial1.setTimeout(5);
  // Debug Serial port setup
  Serial.begin(57600);

  DDRA &= B11110000;

  // Clear any waiting commands
  Serial.flush();
  Serial1.flush();

  // Reset Xbee
  pinMode(26, OUTPUT);
  delay(100);
  pinMode(26, INPUT);
  delay(50);

  // Clear and stop all relevant timers
  TCCR4B = 0;
  TCNT4 = 0;
  TCCR5B = 0;
  TCNT5 = 0;

  // Confirm start-up
  Serial1.println("Control System Online");

}

void loop(){

  if(ready_flag && !jog_mode){
    run_data_aquisition();
  }
  else if(!jog_mode && !stopped){
    stop_stepper();
    stopped = true;
    Serial.println("stopping");
  }
  else if(jog_mode){
    delay(10);
    print_status_report();
    stopped = false;
  }
}

void run_data_aquisition(void){
    //set stopped flag false
    stopped = false;
    // Set motor direction
    digitalWrite(DIR, dir);
    // Set micro-step divisions
    set_microstep(microsteps);
    // Start timer interrupts to drive stepper
    start_stepper(stepper_value);

    bool msg_flg;
    for(int i = 0; i < send_number; i++)
    {
      if(ready_flag){
        msg_flg = false;
        // Send three analogue readings in CSV format
        print_sensor_data();
        if(i % 50 == 0)
        {
          // Every 50 lines send a status report
          print_status_report();
          msg_flg = true;
        }
        delay(5);
      }
      else{
        // Confirm endstop hit
        Serial1.println("END");
        break;
      }
    }
    // Stop timer interrupts
    stop_stepper();
    // Send final status report
    if(msg_flg == false)
    {
      delay(3);
      print_status_report();
    }
    // Confirm end of data transmission
    Serial1.println("ack");
    // Prevents stepper drivers suddenly drawing high current + overheating
    stepper_reset();

    ready_flag = false;
}

void print_sensor_data(){
  temp = PINA & B00001111;
  temp ^= temp >> 4;
  temp ^= temp >> 2;
  temp ^= temp >> 1;
  long pos = 0;
  if(dir)
    pos = stepper_position + (TCNT5 / microsteps);
  else
    pos = stepper_position - (TCNT5 / microsteps);
  
  // Create blank message string
  char s_data [30];
  // Format positional and sensor data into message string
  sprintf(s_data, "v%ld,%d,%d,%d,%d", pos, temp, analogVal0, analogVal1, analogVal2);
  // Print message string
  Serial1.println(s_data);
}

void print_status_report(){
  long pos = 0;
  if(dir)
    pos = stepper_position + (TCNT5 / microsteps);
  else
    pos = stepper_position - (TCNT5 / microsteps);

  // Create blank message string
  char s_report [30];
  // Format positional and micro step into message string
  sprintf(s_report, "sSP:%ld,EP:%ld,MS:%d", pos, encoder_position, microsteps);
  // Print message string
  Serial1.println(s_report);
}

void setup_adc(){
  // Global Interupt Disable
  cli();

  // Clear ADMUX
  ADMUX = 0;
  // Clear ADCSRA
  ADCSRA = 0;

  // Set ADMUX input to value stored in mux, default 5
  // Set REFS0 to change reference voltage to VCC
  ADMUX = mux | _BV(REFS0);
  
  // Set ADEN to enable the ADC
  // Set ADIE to enable the ADC interrupt
  // Set ADSC to start the ADC conversion
  // Set ADPS2:0 for prescaler of 128
  ADCSRA = _BV(ADEN) | _BV(ADIE) | _BV(ADSC) | _BV(ADPS2) | _BV(ADPS1) | _BV(ADPS0);

  // Global Interupt Enable
  sei();
}

void setup_stepper(){
  // Stepper motor pins
  pinMode(RST, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(STEP, OUTPUT);
  pinMode(7, OUTPUT);

  // Reset stepper drivers
  stepper_reset();
  
  // Set to forward motion
  digitalWrite(DIR, HIGH);

  delay(50);
}

void stepper_reset(){
  digitalWrite(RST, LOW);
  delay(50);
  digitalWrite(RST, HIGH);
}

void setup_microstep(uint8_t scale){
  DDRA |= B11100000;
  set_microstep(scale);
}

void set_microstep(uint8_t scale){
  /**************************
  mapping for scale to val 
  1 -> 0 = Full step       
  2 -> 1 = 1/2 Step        
  4 -> 2 = 1/4 Step
  8 -> 3 = 1/8 Step
  16 -> 4 = 1/16 Step
  32 -> 5 = 1/32 Step
  **************************/

  uint8_t val = (uint8_t) (log(scale) / log(2));
  PORTA &= B00011111;
  PORTA |= val << 5;
  Serial.print(microsteps);
  Serial.println(val);
}

void serialEvent1(){

  if(Serial1.available()){
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

        // Number of measurement intervals before next instruction
        if(strcmp(ident, "INT") == 0){
          send_number = atoi(value);
        }
        else if(strcmp(ident, "JOG") == 0){
          // First stop motor running
          if(!stopped){
            stop_stepper();
            stopped = true;
          }
          // Get jog speed
          int stepper_value = atoi(value);
          // Disable jog mode
          if(stepper_value == 0){
            stopped = true;
            jog_mode = false;
            ADCSRA |= _BV(ADIE);
            ADCSRA |= _BV(ADSC);
          }
          // Jog upwards
          else if(stepper_value > 0){
            jog_mode = true;
            dir = 1;
          }
          // Jog downwards
          else if(stepper_value < 0){
            // Servo value must always be positive
            stepper_value = -stepper_value;
            jog_mode = true;
            dir = 0;
          }

          if(jog_mode)
          {
            // Disable ADC interupts as not needed
            ADCSRA &= ~_BV(ADIE);
            digitalWrite(DIR, dir);
            // Set micro-step divisions
            set_microstep(microsteps);
            // Start timer interrupts to drive stepper
            start_stepper(stepper_value);
          }
        }
        else if(strcmp(ident, "DIR") == 0){
          dir = atoi(value);
        }

        else if(strcmp(ident, "RUN") == 0){
          if(strcmp(value, "1") == 0){
            jog_mode = false;
            ready_flag = true;
          }
        }
        // Send the servo position to the appropriate subsystem
        else if(strcmp(ident, "STP") == 0){
          stepper_value = atoi(value);
        }
        else if(strcmp(ident, "MIC") == 0){
          microsteps = atoi(value);
        }
        else if(strcmp(ident, "ZER") == 0){
          stepper_position = 0;
          encoder_position = 0;
          TCNT5 = 0;
          print_status_report();
        }
        else if(strcmp(ident, "RST") == 0){
          pinMode(26, OUTPUT);
          delay(100);
          pinMode(26, INPUT);
          pinMode(A15, OUTPUT);
        }
        if(strcmp(ident, "INIT") == 0){
          //print_sensor_data();
          print_status_report();
        }
      }
      // Find the next command in input string
      command = strtok(0, ",");
    }
  }
}

void start_stepper(int rpm){
  // Global interrupt disable
  cli();
  // remember value to decelerate from
  stop_value = rpm;
  // Update stepper position
  stepper_position += TCNT5 / microsteps;
  // If stopping
  if(rpm == 0){
    Serial.println("Stopping because 0");

    stop_stepper();
    // Global interrupt enable
    sei();
  }
  // Otherwise set RPM
  else{
    // Set entire TCCR4A register to 0
    TCCR4A = 0;
    // Same for TCCR4B
    TCCR4B = 0;
    // Initialize counter value to 0
    TCNT4 = 0;
    // Turn on phase correct PWM mode
    TCCR4A = _BV(COM4A0) | _BV(WGM40);
    // Set CS40 bit for no pre-scaler
    TCCR4B = _BV(WGM43) | _BV(CS40);
    // Starts pulse counter
    start_counter(100);
    // Global interrupt enable
    sei();
    // Accelerate to max speed
    accelerate_stepper(rpm);
  }
}

void accelerate_stepper(int rpm){
  for(int temp = 20; temp < rpm; temp += rpm/100){
    OCR4A = get_ocrna(temp);
        if(jog_mode)
      print_status_report();
    else
      print_sensor_data();
    delay(5);
  }
  OCR4A = get_ocrna(rpm);
}

int get_ocrna(int rpm){
  // Frequency = rotations per second * motor steps * microstep resolution
  float freq = ((float) rpm / 60.0) * 200.0 * (float) microsteps;
  // OCR4A = clock / 2 / prescaler / desired frequency
  float val = 8000000L / freq;
  // Convert to integer
  return (int) val;
}

void start_counter(int compare){
  // Global interrupt disable
  cli();
  // Clear TCCR5A
  TCCR5A = 0;
  // Clear TCCR5B
  TCCR5B = 0;
  // Set inital count to 0
  TCNT5 = 0;
  // Set compare/match to 100
  OCR5A = compare;

  // Enable CTC mode
  TCCR5A |= _BV(WGM52);
  // Set external clock source, falling edge
  TCCR5B |= _BV(CS52) | _BV(CS51);
  // Timer/Countern Output Compare A Match interrupt enable
  TIMSK5 |= _BV(OCIE5A);
  // Global interrupt enable
  sei();
}

void stop_stepper(){
  // Slow to a halt
  decelerate_stepper(stop_value);
  // Global Interrupt Disable
  cli();
  // Clear TCCR4A
  TCCR4A = 0;
  // same for TCCR4B
  TCCR4B = 0;
  //initialize counter value to 0
  TCNT4  = 0;
  // Global Interrupt Enable
  sei();
  if(jog_mode)
    print_status_report();
  else
    print_sensor_data();
}

void decelerate_stepper(int stop_value){
  for(int temp = stop_value; temp > 20; temp -= stop_value/100){
    OCR4A = get_ocrna(temp);
    if(jog_mode)
      print_status_report();
    else
      print_sensor_data();
    delay(5);
  }
  OCR4A = 0;
}

ISR(TIMER5_COMPA_vect){
  // Reset counter
  TCNT5 = 0;
  // If moving upwards
  if(dir)
    stepper_position += 100 / microsteps;
  // If moving downwards
  else
    stepper_position -= 100 / microsteps;
}

// Interrupt service routine for the ADC completion
ISR(ADC_vect){
  
  // Must read low first
  if(mux == 5){
    analogVal0 = ADCL | (ADCH << 8);
    // Read pin A6 next
    mux = 6;
  }
  else if(mux == 6){
    analogVal1 = ADCL | (ADCH << 8);
    // Read pin A7 next
    mux = 7;
  }
  else if(mux == 7){
    analogVal2 = ADCL | (ADCH << 8);
    // Read pin A5 next
    mux = 5;
  }
  // Clear ADC input selection
  ADMUX &= B11111000;
  // Set new ADC input
  ADMUX |= mux;
  // Set ADSC in ADCSRA (0x7A) to start another ADC conversion
  ADCSRA |= _BV(ADSC);
}

// If the robot has hit something
void end_stop(){
  stop_stepper();
  ready_flag = false;
  if(jog_mode){
    jog_mode = false;
    ADCSRA |= _BV(ADIE);
    ADCSRA |= _BV(ADSC);
  }
}
