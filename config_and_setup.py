# config_and_setup.py: Manages global constants (pin assignments, baud rates) and initializes all hardware components.
import RPi.GPIO as GPIO
import smbus
import serial
import cv2
import time
import logger # For logging initialization status and errors

# --- Import modules that need initialization ---
import mpu6050_gyro
import servo_and_pickup
# motor_control and line_following use GPIO pins defined here, but are not initialized directly
# here beyond their basic GPIO setup.


# --- Global Constants and Pin Definitions ---
# GPIO Mode
GPIO_MODE = GPIO.BCM # Use Broadcom pin-numbering scheme

# --- Motor Control Pins (L298N) ---
MOTOR_EN_R = 21   # Enable pin for Right motor
MOTOR_IN1_R = 16  # Input 1 for Right motor
MOTOR_IN2_R = 20  # Input 2 for Right motor

MOTOR_EN_L = 1    # Enable pin for Left motor
MOTOR_IN1_L = 7   # Input 1 for Left motor
MOTOR_IN2_L = 8   # Input 2 for Left motor

# PWM Frequencies
PWM_FREQ_MOTORS = 100 # Hz for motor PWM

# --- IR Sensor Array Pins ---
# Assuming a 5-sensor array: Leftmost, Left-Center, Center, Right-Center, Rightmost
# Adjust these pins according to your actual wiring
IR_SENSOR_PINS = [5, 6, 13, 19, 26]

# --- Serial Communication (for Arduino/Sharp Sensor) ---
SERIAL_PORT = '/dev/ttyACM0' # Common port for Arduino, check 'ls /dev/ttyA*'
SERIAL_BAUD_RATE = 9600     # Baud rate must match Arduino sketch

# --- Camera Settings ---
CAMERA_INDEX = 0             # Usually 0 for the first connected camera
CAMERA_RESOLUTION_WIDTH = 640
CAMERA_RESOLUTION_HEIGHT = 480
CAMERA_FPS = 30              # Frames per second

# --- MPU6050 Gyroscope (I2C) ---
# MPU6050 I2C address is 0x68 when AD0 pin is connected to GND
# No need to define MPU6050_ADDRESS here again if mpu6050_gyro.py already defines it.
# Just ensure MPU6050_ADDRESS in mpu6050_gyro.py matches your AD0 wiring.

# --- PCA9685 PWM Driver (for Servos - I2C) ---
# PCA9685 default I2C address is 0x40.
# The adafruit_servokit library handles this internally, no explicit address needed here.

# --- Global Hardware Objects (to be initialized) ---
pwm_right_motor = None
pwm_left_motor = None
camera_capture = None
arduino_serial = None
# mpu6050_gyro handles its own _i2c_bus object internally
# servo_and_pickup handles its own ServoKit object internally


def initialize_all_hardware():
    """
    Initializes all robot hardware components and GPIO settings.
    This function should be called once at the start of the main program.
    """
    global pwm_right_motor, pwm_left_motor, camera_capture, arduino_serial

    logger.log("Starting hardware initialization sequence.")
    print("Config & Setup: Setting up GPIO...")
    GPIO.setmode(GPIO_MODE)
    GPIO.setwarnings(False) # Disable GPIO warnings

    # --- 1. Setup Motor Pins ---
    GPIO.setup(MOTOR_EN_R, GPIO.OUT)
    GPIO.setup(MOTOR_IN1_R, GPIO.OUT)
    GPIO.setup(MOTOR_IN2_R, GPIO.OUT)
    GPIO.setup(MOTOR_EN_L, GPIO.OUT)
    GPIO.setup(MOTOR_IN1_L, GPIO.OUT)
    GPIO.setup(MOTOR_IN2_L, GPIO.OUT)

    # Initialize PWM for motor enable pins
    pwm_right_motor = GPIO.PWM(MOTOR_EN_R, PWM_FREQ_MOTORS)
    pwm_left_motor = GPIO.PWM(MOTOR_EN_L, PWM_FREQ_MOTORS)
    pwm_right_motor.start(0) # Start PWM with 0% duty cycle (motors off)
    pwm_left_motor.start(0)
    logger.log("Motor GPIO and PWM initialized.")
    print("Config & Setup: Motor GPIO set up.")

    # --- 2. Setup IR Sensor Pins ---
    for pin in IR_SENSOR_PINS:
        GPIO.setup(pin, GPIO.IN)
    logger.log("IR sensor GPIO initialized.")
    print("Config & Setup: IR sensors GPIO set up.")

    # --- 3. Initialize MPU6050 Gyroscope (via mpu6050_gyro module) ---
    # The mpu6050_gyro module handles its own smbus initialization and address.
    print("Config & Setup: Initializing MPU6050 Gyro...")
    mpu6050_gyro.initialize_mpu6050()
    # It's crucial to calibrate the gyro after it's initialized and the robot is still.
    mpu6050_gyro.perform_calibration()
    logger.log("MPU6050 Gyro initialized and calibrated.")
    print("Config & Setup: MPU6050 Gyro initialized and calibrated.")

    # --- 4. Initialize PCA9685 PWM Driver for Servos (via servo_and_pickup module) ---
    # The servo_and_pickup module will encapsulate the ServoKit initialization.
    print("Config & Setup: Initializing Servos (PCA9685)...")
    servo_and_pickup.initialize_servos() # Assumes this sets up the ServoKit object
    servo_and_pickup.set_initial_positions() # Set arm/claw to a default safe position
    logger.log("Servos (PCA9685) initialized and set to initial positions.")
    print("Config & Setup: Servos initialized and set to initial positions.")

    # --- 5. Initialize Camera (OpenCV) ---
    print("Config & Setup: Initializing Camera (OpenCV)...")
    camera_capture = cv2.VideoCapture(CAMERA_INDEX)
    if not camera_capture.isOpened():
        logger.log("ERROR: Could not open camera. Check camera index or connection.", level='CRITICAL')
        print("Config & Setup: ERROR - Could not open camera!")
        camera_capture = None # Ensure it's None if failed
        # Consider adding sys.exit(1) here for critical failure
    else:
        camera_capture.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_RESOLUTION_WIDTH)
        camera_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_RESOLUTION_HEIGHT)
        camera_capture.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
        logger.log(f"Camera initialized with resolution {CAMERA_RESOLUTION_WIDTH}x{CAMERA_RESOLUTION_HEIGHT} at {CAMERA_FPS} FPS.")
        print("Config & Setup: Camera initialized.")

    # --- 6. Initialize Serial Communication (for Arduino/Sharp Sensor) ---
    print("Config & Setup: Initializing Serial communication with Arduino...")
    try:
        arduino_serial = serial.Serial(SERIAL_PORT, SERIAL_BAUD_RATE, timeout=1)
        time.sleep(2) # Give Arduino time to reset after serial connection
        logger.log(f"Serial communication established on {SERIAL_PORT} at {SERIAL_BAUD_RATE} baud.")
        print(f"Config & Setup: Serial communication with Arduino established on {SERIAL_PORT}.")
    except serial.SerialException as e:
        logger.log(f"ERROR: Could not open serial port {SERIAL_PORT}: {e}", level='CRITICAL')
        print(f"Config & Setup: ERROR - Could not open serial port {SERIAL_PORT}! {e}")
        arduino_serial = None # Ensure it's None if failed
        # Consider adding sys.exit(1) here for critical failure
    
    logger.log("All hardware initialization complete.")
    print("Config & Setup: All hardware initialization complete.")


def cleanup_hardware():
    """
    Cleans up all initialized hardware resources.
    This function should be called at the end of the main program, typically in a finally block.
    """
    logger.log("Starting hardware cleanup sequence.")
    print("Config & Setup: Cleaning up hardware resources...")

    # Stop motor PWM
    if pwm_right_motor:
        pwm_right_motor.stop()
    if pwm_left_motor:
        pwm_left_motor.stop()
    logger.log("Motor PWM stopped.")

    # Release camera
    if camera_capture and camera_capture.isOpened():
        camera_capture.release()
        logger.log("Camera released.")

    # Close serial port
    if arduino_serial and arduino_serial.is_open:
        arduino_serial.close()
        logger.log("Serial port closed.")

    # Clean up GPIO
    GPIO.cleanup()
    logger.log("GPIO cleanup complete.")
    print("Config & Setup: All hardware cleanup complete.")