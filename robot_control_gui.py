import sys
import threading
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from gui.robot_gui_ui import Ui_MainWindow
from time import sleep, time
from robot_control import Robot


class Worker(QObject):
    finished = pyqtSignal()
    position = pyqtSignal(float)


class robot_gui(Ui_MainWindow):

    def __init__(self):
        super(robot_gui, self).__init__()

        self.robot = Robot()
        self.robot.initialise()

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
        self.link_buttons()
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

    def link_buttons(self):
        self.link_speed_buttons()
        self.link_microstep_buttons()
        self.link_jog_buttons()
        self.stop_run_button.clicked.connect(self.stop)
        self.start_run_button.clicked.connect(self.run)
        self.pushButton.clicked.connect(self.zero)
        self.pushButton_2.clicked.connect(self.showDialog)

    def link_jog_buttons(self):
        self.jog_up_fast.clicked.connect(lambda: self.set_jog_speed("1500"))
        self.jog_up_slow.clicked.connect(lambda: self.set_jog_speed("100"))
        self.jog_stop.clicked.connect(self.set_jog_stop)
        self.jog_down_slow.clicked.connect(lambda: self.set_jog_speed("-100"))
        self.jog_down_fast.clicked.connect(lambda: self.set_jog_speed("-1500"))

    @pyqtSlot()
    def set_jog_speed(self, speed):
        self.jog_mode = False
        self.robot.jog_speed(speed)
        self.jog_mode = True
        threading.Thread(target=self.run_jog_mode).start()

    @pyqtSlot()
    def set_jog_stop(self):
        self.robot.jog_speed(0)
        sleep(0.1)
        self.robot.jog_speed(0)
        self.jog_stop.setAutoExclusive(False)
        self.jog_stop.setChecked(False)
        self.jog_stop.setAutoExclusive(True)
        self.jog_mode = False

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        self.start_run_button.setDisabled(True)
        self.stop_run_button.setDisabled(False)
        self.statusBar().showMessage("Running")
        threading.Thread(target=self.run_commands).start()

    def zero(self):
        # Update motor position QLCDNumber widget
        self.obj.position.emit(self.robot.zero())

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

    def handle_sensor_data(self, line):
        data = self.robot.handle_sensor_data(line)
        # Update motor position QLCDNumber widget
        self.obj.position.emit(self.robot.position)
        # Check data isn't blank
        if len(data) == 5:
            # Add readings to dataset
            self.probe_data.append(data)
        else:
            self.errors += 1

    def handle_status_message(self, line):
        self.position = self.robot.handle_status_message(line)
        # Update motor position QLCDNumber widget
        self.obj.position.emit(self.position)
        # Check data isn't blank

    def run_jog_mode(self):
        # Run until jog mode flag is set to False
        while self.jog_mode:
            # Try/Except statements as serial read can fail
            try:
                # Check for available data to read in
                if self.robot.xbee.inWaiting():

                    # Decode and strip EOL characters
                    line = self.robot.get_cleaned_line()
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

        self.handle_end_data()

    def run_commands(self):

        start_time = time()
        # Generate a command string from set variables
        self.robot.construct_command(
            MIC=self.microsteps,
            STP=self.rpm,
            INT=self.intervals,
            DIR=self.direction,
            RUN=1)

        # Start first run
        self.robot.send_command()

        # Variable to keep track of how many runs have happened
        current_run = 0

        # Keep track if end stop hit
        end_hit = False

        # Run until self.running flag is set to False
        while self.running:
            # Try/Except statements as serial read can fail
            try:
                # Check for available data to read in
                if self.robot.xbee.inWaiting():

                    # Decode and strip EOL characters
                    line = self.robot.get_cleaned_line()
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
                            self.robot.send_command()
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
                # Wait for any remaining serial data
        self.handle_end_data()
        # Update status bar to "Done" and enable/disable run/stop buttons
        self.obj.finished.emit()
        print("Error rate: {0}%".format(
            self.errors / len(self.probe_data) * 100))
        print("Frequncy: {0}Hz".format(
            len(self.probe_data) / (time() - start_time)))

    def handle_end_data(self):
        # Wait for any remaining serial data
        sleep(0.1)
        # Handle last few status messages
        while self.robot.xbee.inWaiting():
            try:
                # Decode and strip EOL characters
                line = self.robot.get_cleaned_line()
                # Indicates a robot status string
                if line[0] == "v":
                    self.handle_sensor_data(line)
                # Indicates a robot status string
                elif line[0] == "s":
                    self.handle_status_message(line)
            except:
                self.errors += 1
                print(self.errors)
                pass
            sleep(0.005)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = robot_gui()
    sys.exit(app.exec_())
