/*
 * ESP8266 Normal Boot - Cactus WHID
 * Releases GPIO0 HIGH and ENABLE HIGH so the ESP boots
 * into normal firmware mode (not flash/bootloader).
 * Also bridges serial for debugging.
 */

int program_pin = 12;  // GPIO0
int enable_pin = 13;   // ENABLE

void setup() {
  Serial1.begin(115200);
  Serial.begin(115200);
  pinMode(enable_pin, OUTPUT);
  pinMode(program_pin, OUTPUT);

  digitalWrite(program_pin, HIGH);  // GPIO0 HIGH = normal boot
  digitalWrite(enable_pin, LOW);    // Reset ESP
  delay(200);
  digitalWrite(enable_pin, HIGH);   // Release reset
  delay(500);

  Serial.println("ESP8266 normal boot mode. Serial bridge active.");
}

void loop() {
  while (Serial1.available()) {
    Serial.write((uint8_t)Serial1.read());
  }
  if (Serial.available()) {
    while (Serial.available()) {
      Serial1.write((uint8_t)Serial.read());
    }
  }
}
