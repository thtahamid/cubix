# main.py: Orchestrates the robot's overall autonomous operation, calling functions from other modules.

import time
import sys

# Import core modules
import config_and_setup
import motor_control
import line_following
import ir_reading
import mpu6050_gyro
import sharp_sensor
import servo_and_pickup
import color_detection
import navigation
import logger
import utils


def main():
    """
    Main function to run the logistic robot's autonomous operation.
    """
    print("Robot starting up...")

    try:
        # 1. Initialize Hardware and Configurations
        print("Initializing hardware and configurations...")
        config_and_setup.init_hardware()  # Handles GPIO, camera, serial, etc.
        logger.log("Hardware initialized.")

        # 2. Calibrate Sensors (if needed)
        print("Calibrating MPU6050 Gyro...")
        mpu6050_gyro.calibrate_gyro()
        logger.log("MPU6050 Gyro calibrated.")

        # Initialize navigation state (e.g., current position, heading)
        navigation.init_robot_state()
        logger.log(f"Initial robot state: Pos={navigation.get_current_pos()}, Heading={navigation.get_current_heading()}")

        # Main operational loop
        while True:
            print("\nSearching for cubes...")
            logger.log("Entering exploration phase.")

            # Line following handles movement and stops at intersections
            # It should also return if an object is detected
            object_detected = line_following.follow_line_and_explore()

            if object_detected:
                print("Object detected by Sharp IR sensor. Verifying with camera...")
                logger.log("Object detected by Sharp IR sensor.")

                # Verify object presence and identify color
                cube_color = color_detection.detect_cube_color()
                if cube_color:
                    print(f"Detected a {cube_color} cube.")
                    logger.log(f"Detected cube color: {cube_color}.")

                    # Update navigation state with cube position
                    navigation.set_object_location(navigation.get_current_pos(), cube_color)
                    logger.log(f"Cube at {navigation.get_current_pos()}")

                    # Pick up the cube
                    servo_and_pickup.pick_up_object()
                    navigation.set_carrying_object(True)
                    logger.log("Cube picked up.")

                    # Plan path to drop-off zone
                    drop_zone_pos = navigation.get_drop_zone(cube_color)
                    path = navigation.plan_path(navigation.get_current_pos(), drop_zone_pos)

                    if path:
                        print(f"Path planned to {cube_color} drop zone: {path}")
                        logger.log(f"Path planned: {path}")

                        # Navigate to drop-off zone
                        navigation.navigate_path(path)
                        logger.log("Reached drop zone.")

                        # Drop the cube
                        servo_and_pickup.drop_object()
                        navigation.set_carrying_object(False)
                        logger.log("Cube dropped.")
                        print(f"Successfully delivered {cube_color} cube.")
                    else:
                        print(f"Could not plan path to {cube_color} drop zone.")
                        logger.log(f"Error: No path found to {cube_color} drop zone.")
                        # Implement error recovery or re-exploration
                else:
                    print("No colored cube detected or misidentification. Resuming exploration.")
                    logger.log("No colored cube confirmed after Sharp detection.")

            # Check if all cubes are delivered or task complete
            if navigation.is_task_complete():
                print("All cubes delivered. Task complete!")
                logger.log("All cubes delivered. Task complete. Shutting down.")
                break  # Exit the main loop

            # Small delay to prevent busy-looping if no action is taken
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nRobot operation interrupted by user.")
        logger.log("Robot operation interrupted by KeyboardInterrupt.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        logger.log(f"Critical error: {e}", level='ERROR')
    finally:
        # Clean up GPIO and other resources
        print("Cleaning up hardware resources...")
        config_and_setup.cleanup_hardware()
        logger.log("Hardware cleanup complete. Robot shut down.")
        sys.exit(0)


if __name__ == "__main__":
    main()
