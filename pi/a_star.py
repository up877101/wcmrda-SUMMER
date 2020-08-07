# Customised AStar class that serves information over the i2c bus
# to perform low level operations on the AStar board directly.

# Based on the initial version provided by Pololu for use with the
# AStar boards. Copyright Pololu Corporation.

import smbus
import struct
import time

class AStar:
  def __init__(self):
    self.bus = smbus.SMBus(1)

  def read_unpack(self, address, size, format):
    # Ideally we could do this:
    #    byte_list = self.bus.read_i2c_block_data(20, address, size)
    # But the AVR's TWI module can't handle a quick write->read 
    # transition, since the STOP interrupt will occasionally happen 
    # after the START condition, and the TWI module is disabled until
    # the interrupt can be processed.
    #
    # A delay of 0.0001 (100 us) after each write is enough to account
    # for the worst-case situation in our example code.

    self.bus.write_byte(20, address)
    time.sleep(0.0001)
    byte_list = [self.bus.read_byte(20) for _ in range(size)]
    return struct.unpack(format, bytes(byte_list))

  def write_pack(self, address, format, *data):
    data_array = list(struct.pack(format, *data))
    self.bus.write_i2c_block_data(20, address, data_array)
    time.sleep(0.0001)

  def write_motors(self, motorDirection, motorPwm):
      self.write_pack(0, 'c', motorDirection)
      self.write_pack(1, 'B', motorPwm)

  def write_steer(self, steerDirection):
      self.write_pack(2, 'B', steerDirection)