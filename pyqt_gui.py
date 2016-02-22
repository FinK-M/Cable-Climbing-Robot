import sys
import threading
from serial import Serial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Example(QMainWindow):

    def __init__(self):
        super(Example, self).__init__()
        self.ser = Serial("COM3", baudrate=57600, timeout=0.1)
        self.ser.flush()

        self.microsteps = 2
        self.rpm = 120
        self.intervals = 200
        self.direction = 1
        self.runs = 4
        self.running = False
        self.position = 0
        self.initUI()
        self.ser.write("RST:0,".encode())

    def initUI(self):

        ui_path = "C:/icons/PNG/32/User_Interface/"
        ch_path = "C:/icons/PNG/32/Computer_Hardware/"

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(218, 223, 225))
        self.setPalette(palette)

        self.reverse_check = QCheckBox("Reverse", self)
        self.reverse_check.move(280, 40)
        self.reverse_check.stateChanged.connect(self.change_direction)

        # Create combobox
        self.mstep_choice = QComboBox(self)
        self.mstep_choice.addItems(("2", "4"))
        self.mstep_choice.move(20, 40)
        self.mstep_choice.activated[str].connect(self.mstep_set)

        self.int_choice = QComboBox(self)
        self.int_choice.addItems(("100", "200", "400"))
        self.int_choice.move(150, 40)
        self.int_choice.activated[str].connect(self.int_set)

        self.run_btn = QPushButton("Run", self)
        self.run_btn.move(20, 90)
        # self.run_btn.setGraphicsEffect(self.shadow)

        self.stop_btn = QPushButton("Stop", self)
        self.stop_btn.setDisabled(True)
        self.stop_btn.move(150, 90)

        self.lcd = QLCDNumber(self)
        self.lcd.move(280, 90)

        self.run_btn.clicked.connect(self.run)
        self.stop_btn.clicked.connect(self.stop)

        self.statusBar()

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

        self.setGeometry(300, 300, 500, 200)
        self.setWindowTitle('Robot Control')
        self.show()

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
                        # print("ack")
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
        self.run_btn.setDisabled(False)
        self.stop_btn.setDisabled(True)

    def mstep_set(self, text):
        self.microsteps = int(text)

    def int_set(self, text):
        self.intervals = int(text)

    def change_direction(self, state):
        self.direction = 0 if state == Qt.Checked else 1

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Save File', 'data.csv')


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
