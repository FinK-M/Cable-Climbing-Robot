
from time import sleep
from serial import Serial
import csv

microsteps = 4
rpm = 100
intervals = 200
direction = 1

ser = Serial("COM3", baudrate=57600, timeout=0.1)
sleep(2)
ser.write("MIC:{0},SER:{1},INT:{2},DIR:{3},RUN:1".format(
    microsteps, rpm, intervals, direction).encode())

i = 0
probe_data = []
while True:
    while ser.inWaiting():
        try:
            raw = ser.readline()
            line = raw.decode().rstrip("\r\n")

            if line[0] == "v":
                i += 1
                data = line[1:].split(",")
                if data:
                    probe_data.append(data)
                # print("Probe 1: {0} Probe 2: {1} Probe 3: {2}".format(*data))

            elif line[0] == "s":
                data = line[1:].split(",")
                print(data[0], data[1], data[2])

            elif line == "ack":
                ser.write("MIC:{0},SER:{1},INT:{2},DIR:{3},RUN:1".format(
                    microsteps, rpm, intervals, direction).encode())
                break
            else:
                print(line)
        except:
            print("error", raw)
    if i > 1000:
        break

with open('probe_data.csv', 'w', newline='') as csvfile:
    data_writer = csv.writer(csvfile)
    for row in probe_data:
        data_writer.writerow(row)
