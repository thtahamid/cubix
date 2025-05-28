const int sensorPin = A0;  // Pin connected to the sensor's output (Vo)
float distanceCm;

void setup() {
  Serial.begin(9600);  // Initialize serial communication
}

void loop() {
  // Read the analog value from the sensor
  int adcValue = analogRead(sensorPin);
  
  // Convert the analog value to voltage (range: 0 - 5V)
  float voltage = adcValue * (5.0 / 1023.0);
  
  // Convert voltage to distance in centimeters
  // Formula: Distance (cm) = 13 / (voltage - 0.1)
  // This is an approximation for the GP2Y0A41SK0F sensor.
  distanceCm = 13.0 / (voltage - 0.1);
  
  // Print the distance if it's within the valid range (4 to 30 cm)
  if (distanceCm >= 4.0 && distanceCm <= 30.0) {
    Serial.print("Distance: ");
    Serial.print(distanceCm, 2);  // 2 decimal places
    Serial.println(" cm");
  } else {
    Serial.println("Out of range");
  }

  delay(50);  // Wait for 200 milliseconds before next reading
}
