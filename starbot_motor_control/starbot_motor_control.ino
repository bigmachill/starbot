#include <Servo.h>
#include "pins_arduino.h"

Servo head_rotate_motor;
Servo head_tilt_motor;
Servo left_arm_motor;
Servo right_arm_motor;

//struct {
//  int8_t head_rotate_speed;   // Positive is right
//  int8_t head_tilt_speed;     // Positive is up
//  int8_t arm_left_speed;      // Positive is raising
//  int8_t arm_right_speed;     // Positive is raising
//
//  uint32_t head_color_left;   // RGB strip on left side of head, 0 means off
//  uint32_t head_color_right;  // RGB strip on right side of head, 0 means off
//
//  uint8_t led_eye_left;
//  uint8_t led_eye_right;
//  uint8_t led_mouth;
//  uint8_t reserved;
//}
//
//enum {
//  CMD_LED               = 0x00
//  CMD_HEAD_ROTATE       = 0x01,
//  CMD_HEAD_TILT         = 0x02,
//  CMD_ARM_LEFT          = 0x03,
//  CMD_ARM_RIGHT         = 0x04,
//  CMD_HEAD_COLOR_LEFT   = 0x05,
//  CMD_HEAD_COLOR_RIGHT  = 0x06,
//  CMD_LED_EYE_LEFT      = 0x07,
//  CMD_LED_EYE_RIGHT     = 0x08,
//  CMD_LED_MOUTH         = 0x09,
//  MESSAGE_START         = 0xF0000000,
//  MESSAGE_END           = 0x0F000000
//}
//
//struct message {
//  uint8_t cmd;
//  uint32_t data;
//}

struct color_message {
  uint8_t reserved;
  uint8_t red;
  uint8_t green;
  uint8_t blue;
};

char buf[20];
volatile uint8_t pos;
volatile boolean new_message;
volatile uint8_t message_started;

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
  left_arm_motor.attach(9);
  right_arm_motor.attach(10);

  pos = 0;
  new_message = false;
}

// SPI interrupt routine
ISR(SPI_STC_vect) {
  byte c = SPDR;

  // add to buffer if room
  if (pos < sizeof(buf)) {
    buf[pos++] = c;
   
    // example: newline means time to process buffer
    //if (c == '\n')
      new_message = true;
  }
}

void loop(void) {
  if (new_message) {
    buf[pos] = 0;
    Serial.println(buf);
    pos = 0;
    new_message = false;
    if (buf[0]) {
      digitalWrite(LED_PIN, HIGH);
    } else {
      digitalWrite(LED_PIN, LOW);
    }
  }
}
