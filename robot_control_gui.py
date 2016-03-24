import sys
import threading
import csv
from serial import Serial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from gui.robot_gui_ui import Ui_MainWindow
from time import sleep, time


class Worker(QObject):
    finished = pyqtSignal()
    position = pyqtSignal(float)


class robot_gui(Ui_MainWindow):

    def __init__(self):
        super(robot_gui, self).__init__()

        self.microsteps = 2
        self.rpm = 100
        self.intervals = 500
        self.direction = 1
        self.max_runs = 10
        self.running = False
        self.position = 0
        self.jog_mode = False
        self.probe_data = []
        self.errors = 0

        self.obj = Worker()  # no parent!
        self.obj.finished.connect(self.status_bar_done)
        self.obj.position.connect(self.update_lcd)

        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.setup_xbee()
        self.link_buttons()
        self.ser.flush()
        self.ser.write("RST:0,".encode())
        self.statusBar().showMessage("Ready")

    def update_lcd(self, i):
        if 0 <= i < 10:
            self.motor_pos_lcd.setDigitCount(4)
        elif -10 < i < 0 or i >= 10:
            self.motor_pos_lcd.setDigitCount(5)
        elif i <= -10 or i >= 100:
            self.motor_pos_lcd.setDigitCount(6)
        elif i <= -100 or i >= 1000:
            self.motor_pos_lcd.setDigitCount(7)

        self.motor_pos_lcd.display(i)

    def status_bar_done(self):
        self.statusBar().showMessage("Done")
        self.start_run_button.setDisabled(False)
        self.stop_run_button.setDisabled(True)

    def showDialog(self):
        fname = QFileDialog.getSaveFileName(self, 'Save File', 'data.csv')
        with open(fname[0], "w", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(("Position", "Encoder", "A0", "A1", "A2"))
            for row in self.probe_data:
                csvwriter.writerow(row)

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
        self.link_jog_buttons()
        self.stop_run_button.clicked.connect(self.stop)
        self.start_run_button.clicked.connect(self.run)
        self.pushButton.clicked.connect(self.zero)
        self.pushButton_2.clicked.connect(self.showDialog)

    def link_jog_buttons(self):
        self.jog_up_fast.clicked.connect(lambda: self.set_jog_speed("1000"))
        self.jog_up_slow.clicked.connect(lambda: self.set_jog_speed("300"))
        self.jog_stop.clicked.connect(self.set_jog_stop)
        self.jog_down_slow.clicked.connect(lambda: self.set_jog_speed("-300"))
        self.jog_down_fast.clicked.connect(lambda: self.set_jog_speed("-1000"))

    @pyqtSlot()
    def set_jog_speed(self, speed):
        self.jog_mode = False
        self.ser.write("MIC:{0},JOG:{1}".format(
            self.microsteps, speed).encode())
        self.jog_mode = True
        threading.Thread(target=self.run_jog_mode).start()

    @pyqtSlot()
    def set_jog_stop(self):
        self.jog_mode = False
        self.ser.write("JOG:0".encode())
        sleep(0.1)
        self.ser.write("JOG:0".encode())
        self.jog_stop.setAutoExclusive(False)
        self.jog_stop.setChecked(False)
        self.jog_stop.setAutoExclusive(True)

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        self.start_run_button.setDisabled(True)
        self.stop_run_button.setDisabled(False)
        self.statusBar().showMessage("Running")
        threading.Thread(target=self.run_commands).start()

    def zero(self):
        self.ser.write("ZER:0".encode())
        while not self.ser.inWaiting():
            sleep(0.001)

        line = ""
        while "SP:0" not in line:
            try:
                line = self.get_cleaned_line()
                print(line)
            except:
                pass
        print(line)
        self.handle_status_message(line)

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
        self.rpm = int(b.text()[:3])

    def set_microsteps(self, b):
        self.microsteps = int(b.text()[0])

    def construct_command(self, **kwargs):
        # Start with empty string
        command = ""
        for instruction, value in kwargs.items():
            command += "{0}:{1},".format(instruction, value)
        return command[0:-1].encode()

    def get_cleaned_line(self):
        # Read bytes until EOL
        raw = self.ser.readline()
        # Convert from bytes to string and remove EOL characters
        return raw.decode().rstrip("\r\n")

    def handle_sensor_data(self, line):
        # Split line into individual readings ignoring indicator
        data = line[1:].split(",")
        # Get position in terms of rotations
        self.position = (int(data[0]) / 200)
        # Update motor position QLCDNumber widget
        self.obj.position.emit(self.position)
        # Check data isn't blank
        if len(data) == 5:
            # Add readings to dataset
            self.probe_data.append(data)
        else:
            self.errors += 1

    def handle_status_message(self, line):
        # First split string into individual messages
        data = line[1:].split(",")
        # Get position in terms of rotations
        self.position = (int(data[0][3:]) / 200)
        # Update motor position QLCDNumber widget
        self.obj.position.emit(self.position)
        # Check data isn't blank

    def run_jog_mode(self):
        # Run until jog mode flag is set to False
        while self.jog_mode:
            # Try/Except statements as serial read can fail
            try:
                # Check for available data to read in
                if self.ser.inWaiting():

                    # Decode and strip EOL characters
                    line = self.get_cleaned_line()
                    # Indicates a robot status string
                    if line[0] == "s":
                        self.handle_status_message(line)
                    # Any other string is invalid
                    else:
                        print("Invalid String: {0}".format(line))

            # Debug print any failure in the above code
            except Exception as e:
                self.errors += 1
                print("Exception: {0}".format(e))

        # Wait for any remaining serial data
        sleep(0.1)
        # Handle last few status messages
        while self.ser.inWaiting():
            try:
                # Decode and strip EOL characters
                line = self.get_cleaned_line()
                # Indicates a robot status string
                if line[0] == "s":
                    self.handle_status_message(line)
            except:
                self.errors += 1
                pass

    def run_commands(self):

        start_time = time()
        # Generate a command string from set variables
        command = self.construct_command(
            MIC=self.microsteps,
            SER=self.rpm,
            INT=self.intervals,
            DIR=self.direction,
            RUN=1)

        # Start first run
        self.ser.write(command)

        # Variable to keep track of how many runs have happened
        current_run = 0

        # Keep track if end stop hit
        end_hit = False

        # Run until self.running flag is set to False
        while self.running:
            # Try/Except statements as serial read can fail
            try:
                # Check for available data to read in
                if self.ser.inWaiting():

                    # Decode and strip EOL characters
                    line = self.get_cleaned_line()
                    # Get first character in string to indicate type
                    indicator = line[0]

                    # Indicates a sensor data string
                    if indicator == "v":
                        self.handle_sensor_data(line)

                    # Indicates a robot status string
                    elif indicator == "s":
                        self.handle_status_message(line)

                    # Indicates completion of last command set
                    elif line == "ack":
                        # Move to next run through commands
                        # current_run += 1
                        # Stop sending command strings if at max runs
                        if current_run == self.max_runs or end_hit:
                            self.running = False
                        # Send repeat command to keep running
                        else:
                            self.ser.write(command)
                    elif line == "END":
                        end_hit = True
                    # Debug output for invalid data string
                    else:
                        self.errors += 1
                        print("Invalid String: {0}".format(line))

            # Debug print any failure in the above code
            except Exception as e:
                self.errors += 1
                print("Exception: {0}".format(e))

        # Update status bar to "Done" and enable/disable run/stop buttons
        self.obj.finished.emit()
        print("Error rate: {0}%".format(
            self.errors/len(self.probe_data) * 100))
        print("Frequncy: {0}Hz".format(
            len(self.probe_data)/(time()-start_time)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = robot_gui()
    sys.exit(app.exec_())
