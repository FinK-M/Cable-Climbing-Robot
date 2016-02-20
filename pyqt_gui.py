import sys
import threading
from serial import Serial
from PyQt4 import QtGui


class Example(QtGui.QMainWindow):

    def __init__(self):
        super(Example, self).__init__()
        self.ser = Serial("COM3", baudrate=57600, timeout=0.1)

        self.microsteps = 2
        self.rpm = 60
        self.intervals = 200
        self.direction = 1
        self.runs = 4
        self.running = False
        self.position = 0
        self.initUI()
        self.ser.write("RST:0,".encode())

    def initUI(self):

        # Create combobox
        mstep_choice = QtGui.QComboBox(self)
        mstep_choice.addItem("2")
        mstep_choice.addItem("4")
        mstep_choice.move(20, 20)
        mstep_choice.activated[str].connect(self.mstep_set)

        int_choice = QtGui.QComboBox(self)
        int_choice.addItem("100")
        int_choice.addItem("200")
        int_choice.addItem("400")
        int_choice.move(150, 20)
        int_choice.activated[str].connect(self.int_set)

        btn1 = QtGui.QPushButton("Run", self)
        btn1.move(20, 70)

        btn2 = QtGui.QPushButton("Stop", self)
        btn2.move(150, 70)

        self.lcd = QtGui.QLCDNumber(self)
        self.lcd.move(280, 70)

        btn1.clicked.connect(self.run)
        btn2.clicked.connect(self.stop)

        self.statusBar()

        self.setGeometry(300, 300, 500, 150)
        self.setWindowTitle('Robot Control')
        self.show()

    def run(self):
        self.running = True
        threading.Thread(target=self.run_commands).start()
        self.statusBar().showMessage("Running")

    def stop(self):
        self.running = False

    def run_commands(self):

        
        self.ser.write("MIC:{0},SER:{1},INT:{2},DIR:{3},RUN:1".format(
            self.microsteps, self.rpm,
            self.intervals, self.direction).encode())

        i = 0
        probe_data = []
        while i <= self.runs:
            while self.ser.inWaiting():
                try:
                    raw = self.ser.readline()
                    line = raw.decode().rstrip("\r\n")

                    if line[0] == "v":
                        data = line[1:].split(",")
                        if data:
                            probe_data.append(data)

                    elif line[0] == "s":
                        data = line[1:].split(",")
                        self.position = (int(data[0][3:]) /
                                         (200 * self.microsteps))
                        print(data[0], data[1], data[2])

                    elif line == "ack":
                        i += 1
                        print("ack")
                        self.ser.write(
                            "MIC:{0},SER:{1},INT:{2},DIR:{3},RUN:1".format(
                                self.microsteps, self.rpm, self.intervals,
                                self.direction).encode())
                        break
                    else:
                        print(line)
                except:
                    print("error", raw)
                self.lcd.display(self.position)
            if not self.running:
                break
        self.statusBar().showMessage("Done")

    def mstep_set(self, text):
        self.microsteps = int(text)

    def int_set(self, text):
        self.intervals = int(text)


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
