📦 Project: 5x5 Grid Logistic Robot
This project is a small-scale autonomous logistic robot designed to navigate a 5×5 line-marked grid. It detects, picks up, and delivers colored cubes (red or blue) to matching drop-off zones using computer vision and onboard sensors. The robot uses a Raspberry Pi for high-level planning and vision, and an Arduino Nano for real-time control of movement and actuation.

🧠 Key Features
IR line following with intersection tracking

Object detection via Pi Camera + OpenCV

Accurate 90° turns using MPU6050

Obstacle detection using Sharp IR sensor

Servo-based claw and arm for pick-and-drop

Shortest-path planning to navigate between nodes

Resilient to edge cases like misalignment, repeated detection, and lighting variation

🔧 Hardware Used
Raspberry Pi

Arduino Nano

5-sensor IR array

MPU6050 (gyro)

Sharp IR distance sensor

Pi Camera

2x Servo motors (arm + claw)

L298N motor driver