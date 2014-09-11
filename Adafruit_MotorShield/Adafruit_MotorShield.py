#!/usr/bin/python

from Adafruit_StepperMotor import Adafruit_StepperMotor
from Adafruit_DCMotor import Adafruit_DCMotor
from Adafruit_PWM_Servo_Driver import PWM

class Adafruit_MotorShield :
	
	LOW = 0
	HIGHT = 1
		
	def __init__(self, address=0x60, debug=False):
		self.address = address
		self.pwm = PWM(address, debug)
		self.steppers = [Adafruit_StepperMotor(debug), Adafruit_StepperMotor(debug)]
		self.dcmotors = [Adafruit_DCMotor(debug), Adafruit_DCMotor(debug), Adafruit_DCMotor(debug), Adafruit_DCMotor(debug)]
	
	def begin(self, freq=1600):
		self.pwm.begin()
		self.freq = freq
		self.pwm.setPWMFreq(freq);  # This is the maximum PWM frequency
		for i in range(0, 16):
			self.pwm.setPWM(i, 0, 0);

	def setPWM(self, pin, value):
		if value > 4095:
			self.pwm.setPWM(pin, 4096, 0)
		else:
			self.pwm.setPWM(pin, 0, value);
		
	def setPin(self, pin, value):
		if value == self.LOW:
			self.pwm.setPWM(pin, 0, 0)
		else:
			self.pwm.setPWM(pin, 4096, 0)
	
	def getMotor(self, num):
		if num > 4:
			return
		
		num -= 1
		if (self.dcmotors[num].motornum is None):
			# not init'd yet!
			self.dcmotors[num].motornum = num;
			self.dcmotors[num].MC = self;
			if (num == 0):
				pwm = 8
				in2 = 9
				in1 = 10
			elif (num == 1):
				pwm = 13
				in2 = 12
				in1 = 11
			elif (num == 2):
				pwm = 2
				in2 = 3
				in1 = 4
			elif (num == 3):
				pwm = 7
				in2 = 6
				in1 = 5
			self.dcmotors[num].PWMpin = pwm;
			self.dcmotors[num].IN1pin = in1;
			self.dcmotors[num].IN2pin = in2;
		
		return self.dcmotors[num];
			
	def getStepper(self, steps, num):
		if num > 2:
			return
		
		num -= 1
		if self.steppers[num].steppernum is None:
			# not init'd yet!
			self.steppers[num].steppernum = num;
			self.steppers[num].revsteps = steps;
			self.steppers[num].MC = self

			if num == 0:
				pwma = 8
				ain2 = 9
				ain1 = 10
				pwmb = 13
				bin2 = 12
				bin1 = 11
			elif num == 1:
				pwma = 2
				ain2 = 3
				ain1 = 4
				pwmb = 7
				bin2 = 6
				bin1 = 5		
			self.steppers[num].PWMApin = pwma
			self.steppers[num].PWMBpin = pwmb
			self.steppers[num].AIN1pin = ain1
			self.steppers[num].AIN2pin = ain2
			self.steppers[num].BIN1pin = bin1
			self.steppers[num].BIN2pin = bin2
		
		return self.steppers[num]
