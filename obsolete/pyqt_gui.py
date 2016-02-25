import sys
import threading
import csv
from serial import Serial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Example(QMainWindow):

    def __init__(self):
        super(Example, self).__init__()

        self.microsteps = 2
        self.rpm = 120
        self.intervals = 200
        self.direction = 1
        self.runs = 2
        self.running = False
        self.position = 0
        self.probe_data = []

        self.setup_xbee()
        self.initUI()
        self.ser.write("RST:0,".encode())

    def setup_xbee(self):
        self.ser = Serial("COM3", baudrate=57600, timeout=0.1)
        try:
            self.ser.write("+++".encode())
            while not self.ser.inWaiting():
                pass
            if self.ser.read(3) == b'OK\r':
                self.ser.write("ATCN\r".encode())
        except:
            print("Could not open serial port")
        self.ser.flush()

    def initUI(self):

        ui_path = "C:/icons/PNG/32/User_Interface/"
        ch_path = "C:/icons/PNG/32/Computer_Hardware/"
        arr_path = "C:/icons/PNG/32/Arrows/"

        self.reverse_check = QCheckBox("Reverse", self)
        self.reverse_check.move(280, 70)
        self.reverse_check.stateChanged.connect(self.change_direction)

        self.lcd = QLCDNumber(self)
        self.lcd.move(280, 120)

        self.run_stop_btns()
        self.drop_downs()

        self.statusBar()

        self.jog_up = QPushButton("", self)
        pixmap = QPixmap(arr_path + "double_up-32.png")
        self.jog_up.setIcon(QIcon(pixmap))
        self.jog_up.setIconSize(pixmap.rect().size())
        self.jog_up.move(410, 70)

        self.jog_up = QPushButton("", self)
        pixmap = QPixmap(arr_path + "double_down-32.png")
        self.jog_up.setIcon(QIcon(pixmap))
        self.jog_up.setIconSize(pixmap.rect().size())
        self.jog_up.move(410, 120)

        openFile = QAction(QIcon(ui_path + "save-32.png"), 'Save data', self)
        openFile.setShortcut('Ctrl+S')
        openFile.setStatusTip('Save data')
        openFile.triggered.connect(self.showDialog)

        exitAction = QAction(QIcon(ch_path + "shutdown-32.png"), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        openFile.setStatusTip('Quit')
        exitAction.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar("Commands")
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(openFile)

        self.setGeometry(300, 300, 600, 200)
        self.setWindowTitle('Robot Control')
        self.show()

    def run_stop_btns(self):
        self.run_btn = QPushButton("Run", self)
        self.run_btn.move(20, 120)

        self.stop_btn = QPushButton("Stop", self)
        self.stop_btn.setDisabled(True)
        self.stop_btn.move(150, 120)

        self.run_btn.clicked.connect(self.run)
        self.stop_btn.clicked.connect(self.stop)

    def drop_downs(self):
        # Microstepping choice
        self.mstep_choice = QComboBox(self)
        self.mstep_choice.addItems(("2", "4"))
        self.mstep_choice.move(20, 70)
        self.mstep_choice.activated[str].connect(self.mstep_set)

        # Interval choice
        self.int_choice = QComboBox(self)
        self.int_choice.addItems(("100", "200", "400"))
        self.int_choice.move(150, 70)
        self.int_choice.activated[str].connect(self.int_set)

    def run(self):
        self.running = True
        self.run_btn.setDisabled(True)
        self.stop_btn.setDisabled(False)
        threading.Thread(target=self.run_commands).start()
        self.statusBar().showMessage("Running")

    def stop(self):
        self.running = False

    def run_commands(self):

        self.ser.write("MIC:{0},SER:{1},INT:{2},DIR:{3},RUN:1".format(
            self.microsteps, self.rpm,
            self.intervals, self.direction).encode())

        i = 1
        while i < self.runs:
            while self.ser.inWaiting():
                try:
                    raw = self.ser.readline()
                    line = raw.decode().rstrip("\r\n")

                    if line[0] == "v":
                        data = line[1:].split(",")
                        if data:
                            self.probe_data.append(data)

                    elif line[0] == "s":
                        data = line[1:].split(",")
                        self.position = (int(data[0][3:]) /
                                         (200 * self.microsteps))
                        if self.probe_data:
                            self.probe_data[-1].append(self.position)

                    elif line == "ack":
                        i += 1
                        self.ser.write(
                            "MIC:{0},SER:{1},INT:{2},DIR:{3},RUN:1".format(
                                self.microsteps, self.rpm, self.intervals,
                                self.direction).encode())
                        break
                    else:
                        print(line)
                except:
                    print("read error")
                self.lcd.display(self.position)
            if not self.running:
                break
        self.statusBar().showMessage("Done")
        self.run_btn.setDisabled(False)
        self.stop_btn.setDisabled(True)

    def mstep_set(self, text):
        self.microsteps = int(text)

    def int_set(self, text):
        self.intervals = int(text)

    def change_direction(self, state):
        self.direction = 0 if state == Qt.Checked else 1

    def showDialog(self):
        fname = QFileDialog.getSaveFileName(self, 'Save File', 'data.csv')
        with open(fname[0], "w", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(("Position", "A0", "A1", "A2"))
            for row in self.probe_data:
                csvwriter.writerow(row)


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
