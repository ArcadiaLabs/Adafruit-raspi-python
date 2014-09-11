#!/usr/bin/python

''' 
For Motor Shield for Arduino V2 use with Raspberry Pi and level converter for i2c

This is a test script for the Adafruit assembled Motor Shield for Arduino v2
It won't work with v1.x motor shields! Only for the v2's with built in PWM
control

For use with the Adafruit Motor Shield v2 
---->	http://www.adafruit.com/products/1438
'''


from Adafruit_MotorShield import Adafruit_MotorShield
from Adafruit_StepperMotor import Adafruit_StepperMotor
import time

# Create the motor shield object with the default I2C address
AFMS = Adafruit_MotorShield()
# Or, create it with a different I2C address (say for stacking)
# AFMS = Adafruit_MotorShield(0x61); 

# Connect a stepper motor with 200 steps per revolution (1.8 degree)
# to motor port #2 (M3 and M4)
myMotor = AFMS.getStepper(200, 2)

AFMS.begin() # create with the default frequency 1.6KHz
#AFMS.begin(1000);  // OR with a different frequency, say 1KHz

myMotor.setSpeed(10);  # 10 rpm

try:
	while (True):

		print "Single coil steps"
		myMotor.step(100, Adafruit_StepperMotor.FORWARD, Adafruit_StepperMotor.SINGLE); 
		myMotor.step(100, Adafruit_StepperMotor.BACKWARD, Adafruit_StepperMotor.SINGLE); 

		print "Double coil steps"
		myMotor.step(100, Adafruit_StepperMotor.FORWARD, Adafruit_StepperMotor.DOUBLE)
		myMotor.step(100, Adafruit_StepperMotor.BACKWARD, Adafruit_StepperMotor.DOUBLE)

		print "Interleave coil steps"
		myMotor.step(100, Adafruit_StepperMotor.FORWARD, Adafruit_StepperMotor.INTERLEAVE); 
		myMotor.step(100, Adafruit_StepperMotor.BACKWARD, Adafruit_StepperMotor.INTERLEAVE); 

		print "Microstep steps"
		myMotor.step(50, Adafruit_StepperMotor.FORWARD, Adafruit_StepperMotor.MICROSTEP); 
		myMotor.step(50, Adafruit_StepperMotor.BACKWARD, Adafruit_StepperMotor.MICROSTEP);
	  
except KeyboardInterrupt:
	myMotor.release()
	print "Clean "
  
