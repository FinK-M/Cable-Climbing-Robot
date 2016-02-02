from serial import Serial


def send(message):
    ser = Serial("COM3", baudrate=57600)
    ser.flush()
    ser.write(message.encode())


def led_string(led=0, status=0):
    return "LED:{0}{1}".format(led, status)


def adc_string(address=8):
    return "ADC:{0}".format(address)



