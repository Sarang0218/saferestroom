#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Original author WindVoiceVox
# Original Author Github: https://github.com/WindVoiceVox/Raspi_SG90
# http://elecrow.com/

import RPi.GPIO as GPIO
import time
import sys

class sg90:

  def __init__( self, direction):

    self.pin = 22
    GPIO.setmode( GPIO.BCM )
    GPIO.setup( self.pin, GPIO.OUT )
    self.direction = int( direction )
    self.servo = GPIO.PWM( self.pin, 50 )
    self.servo.start(0.0)

  def cleanup( self ):

    self.servo.ChangeDutyCycle(self._henkan(0))
    time.sleep(0.3)
    self.servo.stop()
    GPIO.cleanup()

  def currentdirection( self ):

    return self.direction

  def _henkan( self, value ):

    return 0.05 * value + 7.0

  def setdirection( self, direction, speed ):

    for d in range( self.direction, direction, int(speed) ):
      self.servo.ChangeDutyCycle( self._henkan( d ) )
      self.direction = d
      time.sleep(0.1)
    self.servo.ChangeDutyCycle( self._henkan( direction ) )
    self.direction = direction

def main():

    s = sg90(0)

    try:
        while True:
            
            print("CLOSE")
            s.setdirection( 57, 80 )
            time.sleep(5)
            
            print("OPEN")
            s.setdirection( -100, 80 )
            time.sleep(5)
    except KeyboardInterrupt:
        s.cleanup()

def open_():
    s = sg90(0)

    try:

            print("OPEN")
            s.setdirection( -100, 80 )
            time.sleep(5)
            s.cleanup()
    except KeyboardInterrupt:
        s.cleanup()
        
def close():

    s = sg90(0)

    try:
      
            
            print("CLOSE")
            s.setdirection( 57, 80 )
            s.cleanup()
            time.sleep(5)
    except KeyboardInterrupt:
        s.cleanup()
        
def main():



    try:
        while True:
            
            close()
            
            open_()
    except KeyboardInterrupt:
        s.cleanup()
if __name__ == "__main__":
    main()


