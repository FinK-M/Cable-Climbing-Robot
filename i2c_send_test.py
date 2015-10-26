from time import sleep
from serial import Serial

ser = Serial("COM5", baudrate=19200)
while True:
    for i in range(10):
        message = "LED:" + str(i) + ",MOT:80,SER:180\n"
        print(message)
        ser.write(message.encode())
        while(not ser.inWaiting()):
            sleep(0.05)
        print(ser.read(ser.inWaiting()).decode().rstrip("\r\n"))
        ser.flush()
