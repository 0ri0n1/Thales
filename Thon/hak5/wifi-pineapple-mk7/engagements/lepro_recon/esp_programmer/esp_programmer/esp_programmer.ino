/*
 * ESP8266 Programmer for Cactus WHID
 * Turns the ATmega32U4 into a serial pass-through bridge
 * so esptool can flash the ESP-12S (ESP8266) over USB.
 *
 * Pin mapping (Cactus WHID):
 *   ESP GPIO0  -> ATmega Pin 12
 *   ESP ENABLE -> ATmega Pin 13
 *   ESP RX     -> ATmega Serial1 TX
 *   ESP TX     -> ATmega Serial1 RX
 */

int program_pin = 12;
int enable_pin = 13;

void setup() {
  Serial1.begin(115000);
  Serial.begin(115000);
  pinMode(enable_pin, OUTPUT);
  pinMode(program_pin, OUTPUT);

  digitalWrite(program_pin, LOW);
  digitalWrite(enable_pin, LOW);
  delay(100);
  digitalWrite(enable_pin, HIGH);
  delay(100);

  Serial.println("ESP8266 programmer ready.");
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
