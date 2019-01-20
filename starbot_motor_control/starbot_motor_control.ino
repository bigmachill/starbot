#include <Servo.h>
#include "pins_arduino.h"

Servo head_rotate_motor;

// SPI message state
struct spi_data {
  volatile boolean new_message;
  volatile uint8_t data;
} spi_;

void setup (void) {
  Serial.begin(9600);     // Debugging serial

  //pinMode(MISO, OUTPUT);  // Send on master in, slave out
  SPCR |= _BV(SPE);       // Turn on SPI in slave mode
  SPCR |= _BV(SPIE);      // Turn on interrupts

  head_rotate_motor.attach(5);
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
    uint16_t rotate = 3 * ((uint16_t)((int8_t)spi_.data)) + 1500;
    Serial.print("Rotate: ");
    Serial.println(rotate);
    head_rotate_motor.writeMicroseconds(rotate);
  }
}
