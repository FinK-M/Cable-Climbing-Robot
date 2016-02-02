from time import sleep
from serial import Serial

ser = Serial("COM3", baudrate=57600)
while True:
    for i in range(9):
        ser.flush()
        message = "LED:1{0},LED:2{1},SER:{2},ADC:8".format(i, i + 1, i * 10)
        ser.write(message.encode())
        try:
            available = 0
            while available < 7:
                available = ser.inWaiting()
            line = ser.read(available).decode().rstrip("\r\n")
            data = line.split(",")
            if 0 < int(data[0]) < 1024:
                print("POT:", data[0], "ACK:", data[1] == "ack")
            else:
                print("invalid data: {0}".format(data))
        except:
            print("failed")
            print(ser.readline())
            ser.close()
            sleep(.2)
            ser.open()
            sleep(1)
        sleep(0.01)
