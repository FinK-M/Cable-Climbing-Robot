import sys
import threading
from serial import Serial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from gui.robot_gui_ui import Ui_MainWindow
from time import sleep


class Worker(QObject):
    finished = pyqtSignal()
    position = pyqtSignal(float)


class robot_gui(Ui_MainWindow):

    def __init__(self):
        super(robot_gui, self).__init__()

        self.microsteps = 2
        self.rpm = 100
        self.intervals = 200
        self.direction = 1
        self.max_runs = 2
        self.running = False
        self.position = 0
        self.probe_data = []

        self.obj = Worker()  # no parent!
        self.obj.finished.connect(self.status_bar_done)
        self.obj.position.connect(self.update_lcd)

        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.setup_xbee()
        self.ser.write("RST:0,".encode())
        self.statusBar().showMessage("Resetting Arduino")
        sleep(1)
        self.statusBar().showMessage("Ready")
        self.link_buttons()

    def update_lcd(self, i):
        self.motor_pos_lcd.display(i)

    def status_bar_done(self):
        self.statusBar().showMessage("Done")
        self.start_run_button.setDisabled(False)
        self.stop_run_button.setDisabled(True)

    def setup_xbee(self):

        try:
            self.ser = Serial("COM3", baudrate=57600, timeout=0.1)
            self.ser.write("+++".encode())
            while not self.ser.inWaiting():
                pass
            if self.ser.read(3) == b'OK\r':
                self.ser.write("ATCN\r".encode())
            while not self.ser.inWaiting():
                pass
            if self.ser.read(3) != b'OK\r':
                print("xbee error")
            self.ser.flush()
        except:
            print("Could not open serial port")

    def link_buttons(self):
        self.link_speed_buttons()
        self.link_microstep_buttons()
        self.stop_run_button.clicked.connect(self.stop)
        self.start_run_button.clicked.connect(self.run)

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        self.start_run_button.setDisabled(True)
        self.stop_run_button.setDisabled(False)
        self.statusBar().showMessage("Running")
        threading.Thread(target=self.run_commands).start()

    def link_speed_buttons(self):
        self.speed_50.pressed.connect(lambda: self.set_speed(self.speed_50))
        self.speed_100.pressed.connect(lambda: self.set_speed(self.speed_100))
        self.speed_150.pressed.connect(lambda: self.set_speed(self.speed_150))
        self.speed_200.pressed.connect(lambda: self.set_speed(self.speed_200))

    def link_microstep_buttons(self):
        self.microstep_1.pressed.connect(
            lambda: self.set_microsteps(self.microstep_1))
        self.microstep_2.pressed.connect(
            lambda: self.set_microsteps(self.microstep_2))
        self.microstep_4.pressed.connect(
            lambda: self.set_microsteps(self.microstep_4))
        self.microstep_8.pressed.connect(
            lambda: self.set_microsteps(self.microstep_8))

    def set_speed(self, b):
        if "50" in b.text():
            self.rpm = 50
        if "100" in b.text():
            self.rpm = 100
        if "150" in b.text():
            self.rpm = 150
        if "200" in b.text():
            self.rpm = 200

    def set_microsteps(self, b):
        if "1" in b.text():
            self.microsteps = 1
        elif "2" in b.text():
            self.microsteps = 2
        elif "4" in b.text():
            self.microsteps = 4
        elif "8" in b.text():
            self.microsteps = 8

    def construct_command(self, **kwargs):
        # Start with empty string
        command = ""
        for instruction, value in kwargs.items():
            command += "{0}:{1},".format(instruction, value)
        return command[0:-1].encode()

    def get_cleaned_line(self):
        raw = self.ser.readline()
        return raw.decode().rstrip("\r\n")

    def handle_sensor_data(self, line):
        data = line[1:].split(",")
        if data:
            self.probe_data.append(data)

    def handle_status_message(self, line):
        data = line[1:].split(",")
        position = (int(data[0][3:]) /
                    (200 * self.microsteps))
        self.obj.position.emit(position)
        if self.probe_data:
            self.probe_data[-1].append(self.position)

    def run_commands(self):

        command = self.construct_command(
            MIC=self.microsteps,
            SER=self.rpm,
            INT=self.intervals,
            DIR=self.direction,
            RUN=1)

        self.ser.write(command)

        current_run = 0
        try:
            while self.running:
                if self.ser.inWaiting():

                    line = self.get_cleaned_line()
                    indicator = line[0]

                    if indicator == "v":
                        self.handle_sensor_data(line)

                    elif indicator == "s":
                        self.handle_status_message(line)

                    elif line == "ack":
                        current_run += 1
                        if current_run == self.max_runs:
                            self.running = False
                        else:
                            self.ser.write(command)
                    else:
                        print("err: {0}".format(line))

        except Exception as e:
            print("Exception: {0}".format(e))

        self.obj.finished.emit()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = robot_gui()

    sys.exit(app.exec_())
