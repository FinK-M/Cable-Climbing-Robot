import ipywidgets as widgets
from IPython.display import display
import serial
from time import sleep

ser = serial.Serial(port="COM5")
led_state = 1
servo_pos = 90


def LED_control(state):
    message = "," + str(servo_pos)
    global led_state
    led_state = 1 if state else 0
    command = str(led_state) + message
    ser.write(command.encode())
    sleep(0.1)
    if ser.inWaiting():
        try:
            print(ser.read(ser.inWaiting()).decode().replace('\r', ''))
        except:
            pass


def servo_control(pos):
    global servo_pos
    servo_pos = pos
    message = "," + str(servo_pos)
    command = str(led_state) + message
    ser.write(command.encode())
    sleep(0.1)
    if ser.inWaiting():
        try:
            print(ser.read(ser.inWaiting()).decode().replace('\r', ''))
        except:
            pass

LED_switch = widgets.Checkbox(
    description="LED switch",
    value=False,
    margin=10)

servo_slider = widgets.IntSlider(
    min=0, max=180, value=90,
    description="Servo Angle")

widgets.interactive(
    LED_control,
    state=LED_switch)

widgets.interactive(
    servo_control,
    pos=servo_slider)

display(LED_switch, servo_slider)

"""
while True:
    for i in range(10, 100, 10):
        servo_control(i)
        led_state = 1 if (i % 20 == 0) else 0
        sleep(0.5)
"""
