from serial import Serial
from time import sleep


def send(message):
    ser = Serial("COM3", baudrate=57600)
    ser.flush()
    ser.write(message.encode())
    sleep(0.1)
    if ser.inWaiting():
        print(ser.readline().decode().rstrip('\r\n').split(",")[0])


def led_string(led=0, status=0):
    return "LED:{0}{1},".format(led, status)


def adc_string(address=8):
    return "ADC:{0},".format(address)


def servo_string(rpm, run=1):
    return "SER:{0},RUN:{1}".format(rpm, run)


def get_input():
    print("\n1: Switch LEDs\n"
          "2: Get ADC value\n"
          "3: Set stepper rpm\n"
          "4: Reset\n")

    option = int(input("Select option: "))

    if option == 1:
        led = input("Select LED: ")
        stat = input("Select LED state: ")
        send(led_string(led, stat))

    elif option == 2:
        address = input("Remote I2C address: ")
        send(adc_string(address))

    elif option == 3:
        position = input("Enter stepper rpm (60 - 200): ")
        send(servo_string(position))

    elif option == 4:
        send("RST:1,")

if __name__ == "__main__":
    while True:
        try:
            get_input()
            sleep(0.5)
        except KeyboardInterrupt:
            break
