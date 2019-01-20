#include <Servo.h>
#include "pins_arduino.h"

Servo head_rotate_motor;
Servo head_tilt_motor;

// SPI message state
volatile struct spi_data {
  boolean new_message;
  uint8_t data;
} spi_;

// Additional LED for debugging
#define LED_PIN 2

void setup (void) {
  Serial.begin(9600);     // Debugging serial

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  //pinMode(MISO, OUTPUT);  // Send on master in, slave out
  SPCR |= _BV(SPE);       // Turn on SPI in slave mode
  SPCR |= _BV(SPIE);      // Turn on interrupts

  head_rotate_motor.attach(5);
  head_tilt_motor.attach(6);

  spi_ = {false, 0};
}

// SPI interrupt routine
ISR(SPI_STC_vect) {
  uint8_t c = SPDR;
/*
  if (receiving) {
    // New byte of message, check for end
    if (spi_.len) {
      spi_.len--;
      spi_.buf[spi_.idx++] = c;
    }
  } else {
    // New message incoming...
    spi_.len = c - 1; // Length byte counts as one
    spi_.idx = 0;
    spi_.receiving = true;
  }
*/
  spi_.data = c;
  spi_.new_message = true;
}

void loop(void) {
  if (spi_.new_message) {
    spi_.new_message = false;
    int16_t rotate = ((int16_t)(spi_.data & 0xF0) << 2) + 1500;
    int16_t tilt = ((int16_t)((spi_.data << 4) & 0xF0) << 2) + 1500;
    Serial.print("Rotate: ");
    Serial.print(rotate);
    Serial.print(", Tilt: ");
    Serial.println(tilt);

    head_rotate_motor.writeMicroseconds(rotate);
    head_tilt_motor.writeMicroseconds(tilt);
    
    if (spi_.data = 0xFF) {
      digitalWrite(LED_PIN, HIGH);
    } else {
      digitalWrite(LED_PIN, LOW);
    }
  }
}
