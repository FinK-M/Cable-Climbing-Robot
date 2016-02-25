#define INPUT_SIZE 100

#define DIR 42
#define STEP 41
#define RST 40
#define M0 51
#define M1 52
#define M2 53

unsigned long last_time = 0;

bool ready_flag = false;
bool jog_mode = false;
int dir = 1;

char* servo_msg;
int servo_value = 0;
int last_servo_value;
char* led_state;
char* adc_msg;
int send_number = 0;

volatile long pulse_count = 0;
volatile long max_pulses;
volatile bool continuous = false;

volatile long stepper_position = 0;
volatile long encoder_position = 0;

volatile uint8_t mux = 5;
volatile uint8_t microsteps = 1;

// Value to store analogue result
volatile int analogVal0;
volatile int analogVal1;
volatile int analogVal2;

void setup(){

  // Serial 1 is for Xbee Module
  Serial1.begin(57600);
  // Must set short timeout otherwise will hang when reading data
  Serial1.setTimeout(5);
  // Debug Serial port setup
  Serial.begin(57600);
  
  setup_stepper();
  setup_microstep(microsteps);
  setup_adc();
}

void loop(){
  if(ready_flag)
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
      cli();
      print_sensor_data();
      if(i % 50 == 0)
      {
        // Every 50 lines send a status report
        print_status_report();
        msg_flg = true;
      }
      sei();
      
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
  else
  {
    stop_run();
    last_servo_value = 0;
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

        else if(strcmp(ident, "DIR") == 0){
          dir = atoi(value);
        }

        else if(strcmp(ident, "RUN") == 0){
          if(strcmp(value, "1") == 0){
            ready_flag = true;
          }
        }
        // Send the servo position to the appropriate subsystem
        else if(strcmp(ident, "SER") == 0){
          servo_msg = ident;
          servo_value = atoi(value);
        }
        else if(strcmp(ident, "MIC") == 0){
          microsteps = atoi(value);
        }
        
        else if(strcmp(ident, "RST") == 0){
            pinMode(24, OUTPUT);
        }
      }
      // Find the next command in input string
      command = strtok(0, ",");
    }
  }
}

int get_match(int rpm){
  float pulse = 60.0*1000000.0/(200.0*microsteps)/(float)rpm/2.0;
  return (int) (16000000.0/(1000000.0/pulse*256.0) - 1.0);
}

void start_run(int rpm){

  //stop interrupts
  cli();
  // If stopping
  if(rpm == 0)
    stop_run();
  // Otherwise set RPM
  else
  {
    // set entire TCCR2A register to 0
    TCCR2A = 0;
    // same for TCCR2B
    TCCR2B = 0;
    //initialize counter value to 0
    TCNT2  = 0;
    // match based on pulse length for given rpm
    OCR2A = get_match(rpm);
    // turn on CTC mode
    TCCR2A |= _BV(WGM21);
    // Set CS01 and CS00 bits for 64 prescaler
    TCCR2B |= _BV(CS22) | _BV(CS21);
    // enable timer compare interrupt
    TIMSK2 |= _BV(OCIE2A);
  }
  //start interrupts
  sei();
}

void stop_run(){
  // Disable timer 2 compare interrupts
  TIMSK2 &= ~_BV(OCIE2A);
  //
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

ISR(TIMER2_COMPA_vect){
  // Flip pin 41 state
  PORTG ^= B00000001;
  // Increment total pulse count
  

  if(dir)
    pulse_count++;
  else
    pulse_count--;

  // Each step is two pulses
  stepper_position = pulse_count / 2;

  // Only stop if not running in continuous mode
  if(!continuous && pulse_count == max_pulses)
  {
    // Disable timer 2 compare interrupts
    TIMSK2 &= ~_BV(OCIE2A);
    // Reset to continuous mode
    continuous = true;
  }
}

// Interrupt service routine for the ADC completion
ISR(ADC_vect){
  
  // Must read low first
  if(mux == 5){
    analogVal0 = ADCL | (ADCH << 8);
    // Read pin A6 next
    mux++;
  }
  else if(mux == 6){
    analogVal1 = ADCL | (ADCH << 8);
    // Read pin A7 next
    mux++;
  }
  else if(mux == 7){
    analogVal2 = ADCL | (ADCH << 8);
    // Read pin A5 next
    mux = 5;
  }
  // Clear ADC selection Mux
  ADMUX &= B11110000;
  // Set Mux to new value
  ADMUX |= mux;
  // Set ADSC in ADCSRA (0x7A) to start another ADC conversion
  ADCSRA |= _BV(ADSC);
}
