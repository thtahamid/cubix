const int sensorPin = A0;  // Pin connected to the sensor's output (Vo)
float distanceCm;

void setup() {
  Serial.begin(115200);  // Increased baud rate
}

void loop() {
  int adcValue = analogRead(sensorPin);
  float voltage = adcValue * (5.0 / 1023.0);
  distanceCm = 13.0 / (voltage - 0.1);

  if (distanceCm >= 4.0 && distanceCm <= 30.0) {
    Serial.println(distanceCm, 2);  // Only the number, 2 decimal places
  } else {
    Serial.println(-1.0);  // Use -1.0 to indicate "Out of range"
  }

  delay(50);
}
