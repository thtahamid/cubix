# motor_control.py: Provides basic motor movement functions (forward, stop, turn left/right) by controlling the DC motors.

import RPi.GPIO as GPIO
import time

# Define GPIO pins for Motor 1 (Left Motor)
MOTOR1_IN1 = 7  # Input 1 for Motor 1
MOTOR1_IN2 = 1  # Input 2 for Motor 1
MOTOR1_EN = 8   # Enable Pin for Motor 1 (if using PWM for speed control)

# Define GPIO pins for Motor 2 (Right Motor)
MOTOR2_IN3 = 16  # Input 3 for Motor 2 (IN1 on some L298N boards)
MOTOR2_IN4 = 20  # Input 4 for Motor 2 (IN2 on some L298N boards)
MOTOR2_EN = 21   # Enable Pin for Motor 2 (if using PWM for speed control)

# Global flag to track if GPIO has been set up
gpio_initialized = False
# Global PWM objects
pwm_motor1 = None
pwm_motor2 = None

def setup_motors():
    """
    Sets up the GPIO pins for motor control including PWM.
    """
    global gpio_initialized, pwm_motor1, pwm_motor2
    if gpio_initialized:
        print("GPIO already initialized.")
        return

    GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
    GPIO.setwarnings(False) # Disable warnings

    # Setup Motor 1 pins
    GPIO.setup(MOTOR1_IN1, GPIO.OUT)
    GPIO.setup(MOTOR1_IN2, GPIO.OUT)
    GPIO.setup(MOTOR1_EN, GPIO.OUT) # Uncomment if using Enable pin

    # Setup Motor 2 pins
    GPIO.setup(MOTOR2_IN3, GPIO.OUT)
    GPIO.setup(MOTOR2_IN4, GPIO.OUT)
    GPIO.setup(MOTOR2_EN, GPIO.OUT) # Uncomment if using Enable pin

    # Initially, motors are off
    GPIO.output(MOTOR1_IN1, GPIO.LOW)
    GPIO.output(MOTOR1_IN2, GPIO.LOW)
    GPIO.output(MOTOR2_IN3, GPIO.LOW)
    GPIO.output(MOTOR2_IN4, GPIO.LOW)

    # If using PWM for speed control, you would initialize it here
    # global pwm_motor1, pwm_motor2 # No longer needed here, declared globally
    pwm_motor1 = GPIO.PWM(MOTOR1_EN, 100) # 100 Hz frequency
    pwm_motor2 = GPIO.PWM(MOTOR2_EN, 100) # 100 Hz frequency
    pwm_motor1.start(0) # Start with 0% duty cycle (stopped)
    pwm_motor2.start(0) # Start with 0% duty cycle (stopped)

    gpio_initialized = True
    print("Motor GPIO pins initialized with PWM.")

def forward(speed=75):
    """
    Moves the robot forward.
    Assumes IN1/IN3 HIGH and IN2/IN4 LOW makes motors go forward.
    Adjust if your motor driver behaves differently.
    :param speed: Duty cycle for PWM (0-100)
    """
    if not gpio_initialized:
        print("GPIO not initialized. Call setup_motors() first.")
        return

    print(f"Moving forward at {speed}% speed...")
    GPIO.output(MOTOR1_IN1, GPIO.HIGH)
    GPIO.output(MOTOR1_IN2, GPIO.LOW)
    GPIO.output(MOTOR2_IN3, GPIO.HIGH)
    GPIO.output(MOTOR2_IN4, GPIO.LOW)
    # If using PWM:
    pwm_motor1.ChangeDutyCycle(speed) # Set speed (e.g., 75%)
    pwm_motor2.ChangeDutyCycle(speed) # Set speed (e.g., 75%)

def backward(speed=75):
    """
    Moves the robot backward.
    Assumes IN1/IN3 LOW and IN2/IN4 HIGH makes motors go backward.
    Adjust if your motor driver behaves differently.
    :param speed: Duty cycle for PWM (0-100)
    """
    if not gpio_initialized:
        print("GPIO not initialized. Call setup_motors() first.")
        return

    print(f"Moving backward at {speed}% speed...")
    GPIO.output(MOTOR1_IN1, GPIO.LOW)
    GPIO.output(MOTOR1_IN2, GPIO.HIGH)
    GPIO.output(MOTOR2_IN3, GPIO.LOW)
    GPIO.output(MOTOR2_IN4, GPIO.HIGH)
    # If using PWM:
    pwm_motor1.ChangeDutyCycle(speed) # Set speed (e.g., 75%)
    pwm_motor2.ChangeDutyCycle(speed) # Set speed (e.g., 75%)

def stop():
    """
    Stops both motors.
    """
    if not gpio_initialized:
        print("GPIO not initialized. Call setup_motors() first.")
        return

    print("Stopping motors.")
    GPIO.output(MOTOR1_IN1, GPIO.LOW)
    GPIO.output(MOTOR1_IN2, GPIO.LOW)
    GPIO.output(MOTOR2_IN3, GPIO.LOW)
    GPIO.output(MOTOR2_IN4, GPIO.LOW)
    # If using PWM:
    if pwm_motor1:
        pwm_motor1.ChangeDutyCycle(0) # Stop motor
    if pwm_motor2:
        pwm_motor2.ChangeDutyCycle(0) # Stop motor

def cleanup_gpio():
    """
    Cleans up GPIO settings. Call this when your program exits.
    """
    global gpio_initialized, pwm_motor1, pwm_motor2
    if gpio_initialized:
        print("Cleaning up GPIO.")
        stop() # Ensure motors are stopped
        if pwm_motor1: # Check if PWM was initialized
            pwm_motor1.stop()
        if pwm_motor2: # Check if PWM was initialized
            pwm_motor2.stop()
        GPIO.cleanup()
        gpio_initialized = False

# Example usage (optional, for testing this script directly)
if __name__ == '__main__':
    try:
        setup_motors()
        forward(100) # Move forward at 50% speed
        time.sleep(2)
        backward(50) # Move backward at 50% speed
        time.sleep(2)
        forward(100) # Move forward at 100% speed
        time.sleep(2)
        stop()
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        cleanup_gpio()
