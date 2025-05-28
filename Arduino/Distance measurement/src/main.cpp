#include <Arduino.h>

const int sensorPin = A0;  // Analog pin connected to sensor
float distanceCm;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int adcValue = analogRead(sensorPin);
  float voltage = adcValue * (5.0 / 1023.0);

  // Approximate formula for Sharp GP2Y0A41SK0F
  distanceCm = 13.0 / (voltage - 0.1);

  if (distanceCm >= 4.0 && distanceCm <= 30.0) {
    Serial.print("Distance: ");
    Serial.print(distanceCm, 2);
    Serial.println(" cm");
  } else {
    Serial.println("Out of range");
  }

  delay(80);
}
