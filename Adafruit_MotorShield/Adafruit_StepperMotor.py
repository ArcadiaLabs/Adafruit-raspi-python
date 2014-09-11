#!/usr/bin/python

import time

class Adafruit_StepperMotor :
	
	__MICROSTEPCURVE = [0, 25, 50, 74, 98, 120, 141, 162, 180, 197, 212, 225, 236, 244, 250, 253, 255]
	#__MICROSTEPCURVE = [0, 50, 98, 142, 180, 212, 236, 250, 255] #with MICROSTEPS = 8
	MICROSTEPS = 16         #8 or 16
	
	FORWARD = 1
	BACKWARD = 2
	BRAKE = 3
	RELEASE = 4

	SINGLE = 1
	DOUBLE = 2
	INTERLEAVE = 3
	MICROSTEP = 4
	
	LOW = 0
	HIGH = 1
	
	def __init__(self, debug=False):
		self.debug = debug
		self.revsteps = 0
		self.steppernum = None
		self.currentstep = 0
		
	def setSpeed(self, rpm):
		#Serial.println("steps per rev: "); Serial.println(revsteps);
		#Serial.println("RPM: "); Serial.println(rpm);

		self.usperstep = 60000000.0 / (self.revsteps * rpm)
		self.steppingcounter = 0
	
	def release(self):
		self.MC.setPin(self.AIN1pin, self.LOW)
		self.MC.setPin(self.AIN2pin, self.LOW)
		self.MC.setPin(self.BIN1pin, self.LOW)
		self.MC.setPin(self.BIN2pin, self.LOW)
		self.MC.setPWM(self.PWMApin, 0)
		self.MC.setPWM(self.PWMBpin, 0)
		
	def step(self, steps, dir, style):
		uspers = self.usperstep
		ret = 0
		if style == self.INTERLEAVE:
			uspers /= 2
		elif style == self.MICROSTEP:
			uspers /= self.MICROSTEPS
			steps *= self.MICROSTEPS
			if self.debug:
				print "steps = %d" % steps
		
		while steps > 0:
			steps -= 1;
			#if self.debug:
			#	print "step! %d uspers: %d" % (steps, uspers)
			ret = self.onestep(dir, style);
			time.sleep(uspers/1000000); # in seconde (uspers/1000 in ms)
			self.steppingcounter += (uspers % 1000)
			if self.steppingcounter >= 1000:
				time.sleep(0.001) # 1 ms
				self.steppingcounter -= 1000
				
				
		if style == self.MICROSTEP:
			while ((ret != 0) and (ret != self.MICROSTEPS)):
				ret = self.onestep(dir, style)
				time.sleep(uspers/1000000); # in seconde (uspers/1000 in ms)
				self.steppingcounter += (uspers % 1000)
				if self.steppingcounter >= 1000:
					time.sleep(0.001); # 1 ms
					self.steppingcounter -= 1000

	def onestep(self, dir, style):
		ocra = 255
		ocrb = 255

		# next determine what sort of stepping procedure we're up to
		if style == self.SINGLE:
			if ((self.currentstep/(self.MICROSTEPS/2)) % 2) > 0: # we're at an odd step, weird
				if (dir == self.FORWARD):
					self.currentstep += self.MICROSTEPS/2
				else:
					self.currentstep -= self.MICROSTEPS/2
			else:           # go to the next even step
				if (dir == self.FORWARD):
					self.currentstep += self.MICROSTEPS
				else:
					self.currentstep -= self.MICROSTEPS
				
		elif (style == self.DOUBLE):
			if ((self.currentstep/(self.MICROSTEPS/2) % 2) == 0): # we're at an even step, weird
				if (dir == self.FORWARD):
					self.currentstep += self.MICROSTEPS/2
				else:
					self.currentstep -= self.MICROSTEPS/2
			else:           # go to the next odd step
				if (dir == self.FORWARD):
					self.currentstep += self.MICROSTEPS
				else:
					self.currentstep -= self.MICROSTEPS

		elif (style == self.INTERLEAVE):
			if (dir == self.FORWARD):
				self.currentstep += self.MICROSTEPS/2
			else:
				self.currentstep -= self.MICROSTEPS/2

		elif (style == self.MICROSTEP):
			if (dir == self.FORWARD):
				self.currentstep += 1
			else:
				# BACKWARDS
				self.currentstep -= 1
			
			self.currentstep += self.MICROSTEPS*4;
			self.currentstep %= self.MICROSTEPS*4;

			ocra = 0
			ocrb = 0
					
			if ( (self.currentstep >= 0) and (self.currentstep < self.MICROSTEPS)):
				ocra = self.__MICROSTEPCURVE[self.MICROSTEPS - self.currentstep]
				ocrb = self.__MICROSTEPCURVE[self.currentstep]
			elif ( (self.currentstep >= self.MICROSTEPS) and (self.currentstep < self.MICROSTEPS*2)):
				ocra = self.__MICROSTEPCURVE[self.currentstep - self.MICROSTEPS]
				ocrb = self.__MICROSTEPCURVE[self.MICROSTEPS*2 - self.currentstep]
			elif ( (self.currentstep >= self.MICROSTEPS*2) and (self.currentstep < self.MICROSTEPS*3)):
				ocra = self.__MICROSTEPCURVE[self.MICROSTEPS*3 - self.currentstep]
				ocrb = self.__MICROSTEPCURVE[self.currentstep - self.MICROSTEPS*2]
			elif ( (self.currentstep >= self.MICROSTEPS*3) and (self.currentstep < self.MICROSTEPS*4)):
				ocra = self.__MICROSTEPCURVE[self.currentstep - self.MICROSTEPS*3]
				ocrb = self.__MICROSTEPCURVE[self.MICROSTEPS*4 - self.currentstep]
			
  
		self.currentstep += self.MICROSTEPS*4
		self.currentstep %= self.MICROSTEPS*4

		if self.debug:
			print "current step: %d" % self.currentstep
			print " pwmA = %d pwmB = %d" % (ocra, ocrb) 
	
		self.MC.setPWM(self.PWMApin, ocra*16)
		self.MC.setPWM(self.PWMBpin, ocrb*16)
  
		# release all
		latch_state = 0 # all motor pins to 0

		#Serial.println(step, DEC);
		if (style == self.MICROSTEP):
			if ((self.currentstep >= 0) and (self.currentstep < self.MICROSTEPS)):
				latch_state |= 0x03
			if ((self.currentstep >= self.MICROSTEPS) and (self.currentstep < self.MICROSTEPS*2)):
				latch_state |= 0x06
			if ((self.currentstep >= self.MICROSTEPS*2) and (self.currentstep < self.MICROSTEPS*3)):
				latch_state |= 0x0C
			if ((self.currentstep >= self.MICROSTEPS*3) and (self.currentstep < self.MICROSTEPS*4)):
				latch_state |= 0x09
		else:
			switchValue = (self.currentstep/(self.MICROSTEPS/2))
			if switchValue == 0:
				latch_state |= 0x1; # energize coil 1 only
			elif switchValue ==  1:
				latch_state |= 0x3; # energize coil 1+2
			elif switchValue ==  2:
				latch_state |= 0x2; # energize coil 2 only
			elif switchValue ==  3:
				latch_state |= 0x6; # energize coil 2+3
			elif switchValue ==  4:
				latch_state |= 0x4; # energize coil 3 only
			elif switchValue ==  5:
				latch_state |= 0xC; # energize coil 3+4
			elif switchValue ==  6:
				latch_state |= 0x8; # energize coil 4 only
			elif switchValue ==  7:
				latch_state |= 0x9; # energize coil 1+4
		
		if self.debug:
			print "Latch: 0x%x" % latch_state
  
		if (latch_state & 0x1):
			# Serial.println(self.AIN2pin)
			self.MC.setPin(self.AIN2pin, self.HIGH)
		else:
			self.MC.setPin(self.AIN2pin, self.LOW)
		
		if (latch_state & 0x2):
			self.MC.setPin(self.BIN1pin, self.HIGH)
			# Serial.println(self.BIN1pin)
		else:
			self.MC.setPin(self.BIN1pin, self.LOW)
		
		if (latch_state & 0x4):
			self.MC.setPin(self.AIN1pin, self.HIGH)
			# Serial.println(self.AIN1pin)
		else:
			self.MC.setPin(self.AIN1pin, self.LOW)
		
		if (latch_state & 0x8):
			self.MC.setPin(self.BIN2pin, self.HIGH)
			# Serial.println(self.BIN2pin)
		else:
			self.MC.setPin(self.BIN2pin, self.LOW)
		
		return self.currentstep
