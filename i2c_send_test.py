
from time import sleep
from serial import Serial

ser = Serial("COM3", baudrate=57600, timeout=0.1)

ser.write("RST:1".encode())
sleep(2)
ser.write("SER:250,INT:200,DIR:1,RUN:1".encode())

i = 0
while True:
    while ser.inWaiting():
        try:
            raw = ser.readline()
            line = raw.decode().rstrip("\r\n")

            if line[0] == "v":
                i += 1
                data = line[1:].split(",")
                if not i % 100:
                    print(
                        "Probe 1: {0} Probe 2: {1} Probe 3: {2}".format(*data))

            elif line[0] == "s":
                data = line[1:].split(",")
                print(data[0], data[1])

            elif line == "ack":
                ser.write("SER:250,INT:200,DIR:1,RUN:1".encode())
                break
            else:
                print(line)

        except:
            print("error", raw)
