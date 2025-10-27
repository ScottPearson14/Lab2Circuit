// Define the trigger string that the Python script is looking for
const char* TRIGGER_MESSAGE = "BLOCK";
// Define the pin connected to the output of your detector/threshold circuit
const int DETECTOR_PIN = A0; 
// Define a threshold value (e.g., analog reading below this means beam is blocked)
const int BLOCK_THRESHOLD = 100; // Adjust value based on your circuit

void setup() {
  // Initialize serial communication at the matching baud rate
  Serial.begin(9600); 
  pinMode(DETECTOR_PIN, INPUT);
  Serial.println("Arduino Ready. Monitoring Beam.");
}

void loop() {
  // Read the analog signal from the receiver circuit
  int signalValue = analogRead(DETECTOR_PIN);

  // Debug: Print the current signal value (optional)
  Serial.print("Signal: ");
  Serial.println(signalValue);

  // Check for the critical safety event: signal below threshold (beam blocked)
  if (signalValue < BLOCK_THRESHOLD) {
    // Send the trigger message!
    Serial.println(TRIGGER_MESSAGE); 
    
    // Optional: Add a delay or a state flag here to prevent sending hundreds of emails 
    // while the object is still blocking the beam.
    delay(5000); // Wait 5 seconds after sending the alert before checking again
  }
  
  delay(100); // Short delay for loop stability
}
