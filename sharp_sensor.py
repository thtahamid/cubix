# sharp_sensor.py: Communicates with Arduino Nano to read and provide distance data from the Sharp IR sensor.
import serial

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            try:
                distance = float(line)
                if distance == -1.0:
                    print("Out of range")
                else:
                    print(f"Distance in cm: {distance}")
            except ValueError:
                print(f"Ignored invalid line: {line}")
except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    ser.close()
# distance_sensor.py

import serial

class DistanceSensor:
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)

    def read_distance(self):
        line = self.ser.readline().decode('utf-8').strip()
        if not line:
            return None
        try:
            distance = float(line)
            if distance == -1.0:
                return None  # Out of range
            return distance
        except ValueError:
            return None  # Invalid line

    def close(self):
        self.ser.close()

