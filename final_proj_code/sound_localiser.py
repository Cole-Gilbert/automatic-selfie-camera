import numpy as np
import wave
import struct
import matplotlib.pyplot as plt
import subprocess
import numpy as np
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from time import sleep
import os
import RPi.GPIO as GPIO
from picamera2 import Picamera2, Preview
from datetime import datetime

#gpio setup for servo pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
servo_pwm = GPIO.PWM(27, 50)
servo = GPIO.PWM(17, 50)

def move_to_the_left():
	print ("turning left")
	servo_pwm.start(0)
	servo.start(0)
	servo_pwm.ChangeDutyCycle(3)
	servo.ChangeDutyCycle(8)
	sleep(1)
	servo.ChangeDutyCycle(5)
	servo_pwm.ChangeDutyCycle(5)

def move_to_the_right():
	servo_pwm.start(0)
	servo.start(0)
	servo_pwm.ChangeDutyCycle(8)
	servo.ChangeDutyCycle(8)
	sleep(1)
	servo.ChangeDutyCycle(5)
	servo_pwm.ChangeDutyCycle(5)


def get_max_audio(index):
	audio_file = wave.open('outputfile.wav', 'r')
	if index:
		audio_file = wave.open('outputfile1.wav', 'r')
	num_frames = audio_file.getnframes()
	framerate = audio_file.getframerate()
	audio_data = audio_file.readframes(num_frames)
	audio_data = np.frombuffer(audio_data, dtype=np.int16)
	max = np.argmax((audio_data))
	return audio_data[max]

while True:
	max = get_max_audio(0)
	max1 = get_max_audio(1)

	if (max > 20000) or (max1 > 20000):
		print("handclap detected")
		difference = max - max1
		if difference < 0:
			move_to_the_left()
		else:
			move_to_the_right()
	else:
		print ("no handclap detected")
		sleep(1)
