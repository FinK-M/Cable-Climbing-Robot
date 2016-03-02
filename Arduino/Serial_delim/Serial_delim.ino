#define INPUT_SIZE 100

#define DIR 42
#define STEP 6
#define RST 40
#define M0 51
#define M1 52
#define M2 53

bool ready_flag = false;
bool jog_mode = false;

unsigned long last_msg_time = 0;

int dir = 1;

int servo_value = 0;
int send_number = 0;

volatile long pulse_count = 0;
volatile long max_pulses;
volatile bool continuous = false;

volatile long stepper_position = 0;
volatile long encoder_position = 0;

volatile uint8_t mux = 5;
volatile uint8_t microsteps = 2;

// Value to store analogue result
volatile int analogVal0;
volatile int analogVal1;
volatile int analogVal2;

void setup(){

  setup_stepper();
  setup_microstep(microsteps);
  setup_adc();

  // Serial 1 is for Xbee Module
  Serial1.begin(57600);
  // Must set short timeout otherwise will hang when reading data
  Serial1.setTimeout(5);
  // Debug Serial port setup
  Serial.begin(57600);
}

void loop(){

  if(ready_flag && !jog_mode)
  {
    // Set motor direction
    digitalWrite(DIR, dir);
    // Set micro-step divisions
    set_microstep(microsteps);
    // Start timer interrupts to drive stepper
    start_run(servo_value);

    bool msg_flg;
    for(int i = 0; i < send_number; i++)
    {
      delay(3);
      msg_flg = false;
      // Send three analogue readings in CSV format
      print_sensor_data();
      if(i % 50 == 0)
      {
        // Every 50 lines send a status report
        print_status_report();
        msg_flg = true;
      }
      
    }
    // Stop timer interrupts
    stop_run();
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
  else if(!jog_mode)
  {
    stop_run();
  }
  else if(jog_mode){
    // Status reporting with no readings every 50ms
    if(millis() - last_msg_time > 50){
      print_status_report();
      last_msg_time = millis();
    }
  }
}

void print_sensor_data(){
  Serial1.print("v");
  Serial1.print(stepper_position);
  Serial1.print(",");
  Serial1.print(analogVal0);
  Serial1.print(",");
  Serial1.print(analogVal1);
  Serial1.print(",");
  Serial1.println(analogVal2);
}

void print_status_report(){
  Serial1.print("sSP:");
  Serial1.print(stepper_position);
  Serial1.print(",EP:");
  Serial1.print(encoder_position);
  Serial1.print(",MS:");
  Serial1.println(microsteps);
}

void setup_adc(){
  // clear ADLAR in ADMUX to right-adjust the result
  // ADCL will contain lower 8 bits, ADCH upper 2 (in last two bits)
  ADMUX &= ~_BV(ADLAR); //B11011111;
  // Set REFS1..0 in ADMUX to change reference voltage to VCC
  ADMUX |= B01000000;  
  // Clear MUX3..0 in ADMUX
  ADMUX &= B11110000;
  // Set ADC input to value stored in mux, default 5
  ADMUX |= mux;
  // Set ADEN in ADCSRA (0x7A) to enable the ADC.
  ADCSRA |= _BV(ADEN);
  // Set the Prescaler to 128 (16000KHz/128 = 125KHz)
  ADCSRA |= B00000111;
  // Set ADIE in ADCSRA (0x7A) to enable the ADC interrupt.
  ADCSRA |= _BV(ADIE);
  // Enable global interrupts
  sei();
  // Set ADSC in ADCSRA (0x7A) to start the ADC conversion
  ADCSRA |= _BV(ADSC);
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
  DDRB |= 7;
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
  PORTB &= B11111000;
  PORTB |= val;
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

        // Number of measurement intervals before next instruction
        if(strcmp(ident, "INT") == 0){
          send_number = atoi(value);
        }
        else if(strcmp(ident, "JOG") == 0){
          // First stop motor running
          stop_run();
          continuous = true;
          // Disable jog mode
          if(strcmp(value, "OFF") == 0){
            jog_mode = false;
            ADCSRA |= _BV(ADIE);
            ADCSRA |= _BV(ADSC);
          }
          // Move down fast
          else if (strcmp(value, "DF") == 0){
            jog_mode = true;
            servo_value = 200;
            dir = 0;
          }
          // Move down slowly
          else if (strcmp(value, "DS") == 0){
            jog_mode = true;
            servo_value = 100;
            dir = 0;
          }
          // Move up slowly
          else if (strcmp(value, "US") == 0){
            jog_mode = true;
            servo_value = 100;
            dir = 1;
          }
          // Move up fast
          else if (strcmp(value, "UF") == 0){
            jog_mode = true;
            servo_value = 200;
            dir = 1;
          }
          if(jog_mode)
          {
            // Disable ADC interupts as not needed
            ADCSRA &= ~_BV(ADIE);
            digitalWrite(DIR, dir);
            // Set micro-step divisions
            set_microstep(microsteps);
            // Start timer interrupts to drive stepper
            start_run(servo_value);
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
        else if(strcmp(ident, "SER") == 0){
          servo_value = atoi(value);
        }
        else if(strcmp(ident, "MIC") == 0){
          microsteps = atoi(value);
        }
        
        else if(strcmp(ident, "RST") == 0){
            pinMode(25, OUTPUT);
            delay(100);
            pinMode(24, OUTPUT);
        }
      }
      // Find the next command in input string
      command = strtok(0, ",");
    }
  }
}

void start_run(int rpm){

  // Global interrupt disable
  cli();
  // If stopping
  if(rpm == 0)
    stop_run();
  // Otherwise set RPM
  else
  {
    // Set entire TCCR4A register to 0
    TCCR4A = 0;
    // Same for TCCR4B
    TCCR4B = 0;
    // Initialize counter value to 0
    TCNT4  = 0;
    // Get TOP value from desired rpm
    OCR4A = get_ocrna(rpm);
    // Turn on phase correct PWM mode
    TCCR4A = _BV(COM4A0) | _BV(COM4B1) | _BV(WGM40);
    // Set CS41 bit for 8 prescaler
    TCCR4B = _BV(WGM43) | _BV(CS41);
  }
  // Starts pulse counter
  start_counter();
  // Global interrupt enable
  sei();
}

int get_ocrna(int rpm){
  // Frequency = rotations per second * motor steps * microstep resolution
  float freq = ((float) rpm / 60.0) * 200.0 * (float) microsteps;
  // OCR4A = clock / 2 / prescaler / desired frequency
  float val = 500000.0 / freq;
  // Convert to integer
  return (int) val;
}

void start_counter(){
  // Global interrupt disable
  cli();
  // Clear TCCR5A
  TCCR5A = 0;
  // Clear TCCR5B
  TCCR5B = 0;
  // Set inital count to 3 to compensate for trigger lag
  TCNT5 = 0;
  // Set compare/match to 100
  OCR5A = 100;

  // Enable CTC mode
  TCCR5A |= _BV(WGM52);
  // Set external clock source, rising edge
  TCCR5B |= _BV(CS52) | _BV(CS51) | _BV(CS50);
  // Timer/Countern Output Compare A Match interrupt enable
  TIMSK5 |= _BV(OCIE5A);
  // Global interrupt enable
  sei();
}

void stop_run(){
  cli();
  // Clear TCCR4A
  TCCR4A = 0;
  // same for TCCR4B
  TCCR4B = 0;
  //initialize counter value to 0
  TCNT4  = 0;
  sei();
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
  move_steps((int)((float)angle/360.0 * 200.0 * microsteps), rpm);
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
  // Clear ADC selection and set new value
  ADMUX = B11110000 | mux;
  // Set ADSC in ADCSRA (0x7A) to start another ADC conversion
  ADCSRA |= _BV(ADSC);
}
