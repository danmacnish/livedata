void setup() {
  Serial.begin(9600);

}

void loop() {
  if(Serial.available() > 0) {
    if(Serial.read() == 1) {//if we read '1' from the serial port
      unsigned int moisture = analogRead(0);
      Serial.write(moisture);
    }
  }
}
