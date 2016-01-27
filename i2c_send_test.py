from time import sleep
from serial import Serial

ser = Serial("COM3", baudrate=57600)
while True:
    for i in range(10):
        ser.flush()
        message = "LED:{0},MOT:80,SER:{1}\n".format(i, i * 10)
        ser.write(message.encode())
        while(ser.inWaiting() < 7):
            sleep(0.05)
        available = ser.inWaiting()

        try:
            available = 0
            while available < 7:
                available = ser.inWaiting()
            line = ser.read(available).decode().rstrip("\r\n")
            data = line.split(",")
            if 0 < int(data[0]) < 1024:
                print("POT:", data[0], "ACK:", data[1] == "ack")
            else:
                print("invalid data")
        except:
            print("failed")
            print(ser.readline())
            sleep(1)
        sleep(0.05)
