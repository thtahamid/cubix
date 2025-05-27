# 📦 Project: 5x5 Grid Logistic Robot

## 📖 Description
This project is a small-scale autonomous logistic robot designed to navigate a 5×5 line-marked grid. It detects, picks up, and delivers colored cubes (red or blue) to matching drop-off zones using computer vision and onboard sensors. The robot uses a Raspberry Pi for high-level planning and vision, and an Arduino Nano for real-time control of movement and actuation.

## 🧠 Key Features
- IR line following with intersection tracking
- Object detection via Pi Camera + OpenCV
- Accurate 90° turns using MPU6050
- Obstacle detection using Sharp IR sensor
- Servo-based claw and arm for pick-and-drop
- Shortest-path planning to navigate between nodes
- Resilient to edge cases like misalignment, repeated detection, and lighting variation

## 🔧 Hardware Used
- Raspberry Pi
- Arduino Nano
- 5-sensor IR array
- MPU6050 (gyro)
- Sharp IR distance sensor
- Pi Camera
- 2x Servo motors (arm + claw)
- L298N motor driver

## 📂 File Structure

Here's a breakdown of the project's file structure:

- **`main.py`**: The main script that orchestrates the robot's operations.
- **`color_detection.py`**: Handles color detection of the cubes using the Pi Camera and OpenCV.
- **`config_and_setup.py`**: Contains configuration settings and setup routines for hardware components.
- **`ir_reading.py`**: Manages readings from the IR sensor array for line following.
- **`line_following.py`**: Implements the line following logic.
- **`logger.py`**: Provides logging functionality for debugging and monitoring.
- **`motor_control.py`**: Controls the robot's motors for movement.
- **`mpu6050_gyro.py`**: Interfaces with the MPU6050 gyroscope for accurate turns.
- **`navigation.py`**: Handles navigation tasks, including path planning and movement between grid nodes.
- **`servo_and_pickup.py`**: Controls the servo motors for the claw and arm mechanism to pick up and drop cubes.
- **`sharp_sensor.py`**: Manages readings from the Sharp IR distance sensor for obstacle detection.
- **`utils.py`**: Contains utility functions used across the project.
- **`logs/`**: Directory where log files are stored.
- **`README.md`**: This file, providing an overview of the project.
- **`LICENSE`**: Contains the project's license information.

## 🛠️ Installation
<!-- Add installation instructions here -->

## 🚀 Usage
<!-- Add usage instructions here -->

## 🤝 Contributing
<!-- Add contribution guidelines here -->

## 📄 License
<!-- Add license information here, e.g., This project is licensed under the MIT License - see the LICENSE file for details. -->