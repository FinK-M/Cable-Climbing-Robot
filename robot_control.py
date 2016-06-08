import serial
from serial.tools import list_ports
from time import sleep, time


class robot(object):
    """
    Robot command class
    """

    def __init__(self):
        self.xbee = self.get_xbee()

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

    def robot_init(self):
        if not self.xbee:
            return -1

        self.xbee.write(b'INIT:0')
        print(self.get_cleaned_line())

    def get_cleaned_line(self):
        # Read bytes until EOL
        raw = self.xbee.readline()
        # Convert from bytes to string and remove EOL characters
        return raw.decode().rstrip("\r\n")

if __name__ == "__main__":
    r = robot()
    r.robot_init()
