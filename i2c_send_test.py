from time import sleep
from serial import Serial

ser = Serial("COM5", baudrate=19200)
while True:
    for i in range(10):
        message = "LED:" + str(i) + ",MOT:80,SER:180\n"
        ser.write(message.encode())
        while(not ser.inWaiting()):
            sleep(0.05)

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
            print(ser.read(available))
            sleep(1)
