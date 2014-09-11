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
from Adafruit_DCMotor import Adafruit_DCMotor
import time

# Create the motor shield object with the default I2C address
AFMS = Adafruit_MotorShield()
# Or, create it with a different I2C address (say for stacking)
# AFMS = Adafruit_MotorShield(0x61); 

# Select which 'port' M1, M2, M3 or M4. In this case, M1
myMotor = AFMS.getMotor(1)

AFMS.begin() # create with the default frequency 1.6KHz
#AFMS.begin(1000);  // OR with a different frequency, say 1KHz

# Set the speed to start, from 0 (off) to 255 (max speed)
myMotor.setSpeed(150);  # 10 rpm
myMotor.run(Adafruit_DCMotor.FORWARD)
# turn on motor
myMotor.run(Adafruit_DCMotor.RELEASE)

try:
	while (True):

		print "tick";

		myMotor.run(Adafruit_DCMotor.FORWARD);
		for i in range(0, 255):
			myMotor.setSpeed(i)
			time.sleep(0.01)			

		for i in range(254, -1):
			myMotor.setSpeed(i)
			time.sleep(0.01)


		print "tock";

		myMotor.run(Adafruit_DCMotor.BACKWARD);
		for i in range(0, 255):
			myMotor.setSpeed(i)  
			time.sleep(0.01)

		for i in range(254, -1):
			myMotor.setSpeed(i) 
			time.sleep(0.01)


		print "tech";
		myMotor.run(Adafruit_DCMotor.RELEASE);
		time.sleep(1)
	
except KeyboardInterrupt:
	myMotor.run(Adafruit_DCMotor.RELEASE)
	print "Clean "
  
