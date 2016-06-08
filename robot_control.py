import serial
from serial.tools import list_ports
from time import sleep


class Robot(object):
    """
    Robot command class
    """

    def __init__(self):
        self.xbee = self.get_xbee()
        self.position = 0
        self.microsteps = 2
        self.rpm = 100
        self.intervals = 200
        self.direction = 1
        self.command_string = ""

    def get_comport(self):
        # Get details of all serial devices
        devices = list(list_ports.comports())
        # Iterate through all available COM devices
        for d in devices:
            # Identifies device as USB FTDI bridge, or XBee Explorer.
            if "VID:PID=0403:6015" in d.hwid:
                # Found Explorer, no need to keep searching
                return d.device
        # No XBee Explorers found
        else:
            return None

    def get_xbee(self):
        port = self.get_comport()
        if port:
            try:
                ser = serial.Serial(port=port, baudrate=57600, timeout=0.1)
                # Set XBee to AT command mode
                ser.write(b"+++")
                # Wait for response
                while not ser.inWaiting():
                    pass
                # Check for correct response
                if ser.readline() != b'OK\r':
                    raise serial.SerialException("Invalid reply to command")
                # Set XBee back to AT mode
                ser.write(b"ATCN\r")
                # Wait for response
                while not ser.inWaiting():
                    pass
                # Check for correct response
                if ser.readline() != b'OK\r':
                    raise serial.SerialException("Invalid reply to command")
                # If all is good, set XBee to this serial object
                return ser
            except Exception as e:
                print("Could not configure XBee module:", e)
                return None
        else:
            print("No XBee modules found!")
            return None

    def initialise(self):
        # Check a working xbee module is actually connected
        if not self.xbee:
            return -1
        # Reset the controller
        self.xbee.write(b'RST:0')
        self.xbee.flush()
        self.wait_for_data(max_retries=40)

        data = self.get_cleaned_line()
        # 1 for correct message, -1 otherwise
        return 1 if data == "Control System Online" else -1

    def get_cleaned_line(self):
        # Read bytes until EOL
        raw = self.xbee.readline()
        # Convert from bytes to string and remove EOL characters
        return raw.decode().rstrip("\r\n")

    def handle_sensor_data(self, line):
        # Split line into individual readings ignoring indicator
        data = line[1:].split(",")
        # Get position in terms of rotations
        self.position = (int(data[0]) / 200)
        # Check data isn't blank
        if len(data) == 5:
            # Add readings to dataset
            return data
        else:
            self.errors += 1

    def handle_status_message(self, line):
        # First split string into individual messages
        data = line[1:].split(",")
        # Get position in terms of rotations
        self.position = (int(data[0][3:]) / 200)
        # return position
        return self.position

    def jog_speed(self, speed):
        try:
            self.xbee.write("MIC:{0},JOG:{1}".format(
                self.microsteps, speed).encode())
            return 1
        except:
            return -1

    def zero(self):
        # Send zero command
        self.xbee.write("ZER:0".encode())

        self.wait_for_data(max_retries=10)

        line = ""
        while "SP:0" not in line:
            try:
                line = self.get_cleaned_line()
            except Exception as e:
                print(e)
        return self.handle_status_message(line)

    def wait_for_data(self, max_retries):
        retries = 0
        while not self.xbee.inWaiting():
            if retries >= max_retries:
                return -1
            sleep(0.05)
            retries += 1

    def construct_command(self, **kwargs):
        # Start with empty string
        command = ""
        # Iterate through input commands and add to output string
        for instruction, value in kwargs.items():
            command += "{0}:{1},".format(instruction, value)
        # Remove final comma and encode for sending
        self.command_string = command[0:-1].encode()

    def send_command(self):
        self.xbee.write(self.command_string)

if __name__ == "__main__":
    r = Robot()
    r.initialise()
    r.zero()
