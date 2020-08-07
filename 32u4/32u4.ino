#include <Servo.h>
#include <AStar32U4.h>
#include <PololuRPiSlave.h>

/* 
 * This program sets the A-Star 32U4 Robot Controller up as a 
 * Raspberry Pi I2C slave. The RPi and A-Star can exchange data 
 * bidirectionally.
 * 
 * This program is based on the example script provided by 
 * Pololu in the following library:
 * 
 * https://github.com/pololu/pololu-rpi-slave-arduino-library
 */

/*
 * Custom data structure that is used for interpreting the buffer.
 * We recommend keeping this under 64 bytes total.  If you change
 * the data format, make sure to update the corresponding code in
 * a_star.py on the Raspberry Pi.
 */

struct Data
{
  char motorDirection;
  uint8_t motorPwm;
  uint8_t steerDirection;
};

PololuRPiSlave<struct Data,5> slave;
#define drivePwmPin 5
#define driveDirPin 4
#define steerPin 6
Servo steerServo;

void setup()
{
  // Set up the slave at I2C address 20.
  slave.init(20);

  // setup pinmodes for motor and servo
  pinMode(drivePwmPin, OUTPUT);
  pinMode(driveDirPin, OUTPUT);
  steerServo.attach(steerPin);
}

void loop()
{
  // Call updateBuffer() before using the buffer, to get the latest
  // data including recent master writes.
  slave.updateBuffer();

  // Sets motor drive direction, either forward with 'f' or
  // backward with 'b'
  if (slave.buffer.motorDirection == 'f') {
      digitalWrite(driveDirPin, HIGH);
  }
  else if (slave.buffer.motorDirection == 'b') {
      digitalWrite(driveDirPin, LOW);
  }

  // Sets motor drive speed
  analogWrite(drivePwmPin, slave.buffer.motorPwm);

  // Sets steer servo direction
  steerServo.write(slave.buffer.steerDirection);

  // When you are done WRITING, call finalizeWrites() to make modified
  // data available to I2C master.
  slave.finalizeWrites();
}
