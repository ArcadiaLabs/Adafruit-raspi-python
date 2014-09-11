#!/usr/bin/python

import time

class Adafruit_DCMotor :
	
	FORWARD = 1
	BACKWARD = 2
	BRAKE = 3
	RELEASE = 4
	
	LOW = 0
	HIGH = 1
	
	def __init__(self, debug=False):
		self.debug = debug
		self.MC = None
		self.motornum = None
		self.PWMpin = 0
		self.IN1pin = 0
		self.IN2pin = 0
		
	def setSpeed(self, speed):
		self.MC.setPWM(self.PWMpin, speed*16);
		
	def run(self, cmd):
		if cmd == self.FORWARD:
			self.MC.setPin(self.IN2pin, self.LOW)  # take low first to avoid 'break'
			self.MC.setPin(self.IN1pin, self.HIGH)
		elif cmd == self.BACKWARD:
			self.MC.setPin(self.IN1pin, self.LOW)  # take low first to avoid 'break'
			self.MC.setPin(self.IN2pin, self.HIGH)
		elif cmd == self.RELEASE:
			self.MC.setPin(self.IN1pin, self.LOW)
			self.MC.setPin(self.IN2pin, self.LOW)
