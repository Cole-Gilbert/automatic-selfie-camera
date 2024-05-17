import time
import board
import busio
import numpy as np
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from time import sleep
import os
import RPi.GPIO as GPIO
from picamera2 import Picamera2, Preview
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
servo_pwm = GPIO.PWM(27, 50)
servo = GPIO.PWM(17, 50)

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

channel = AnalogIn(ads, ADS.P0)
channel_two = AnalogIn(ads, ADS.P1)


def move_to_the_left():
	print ("turning left")
	servo_pwm.start(0)
	servo.start(0)
	servo_pwm.ChangeDutyCycle(3)
	sleep(1)
	servo.ChangeDutyCycle(7.5)
	sleep(1)
	servo.ChangeDutyCycle(8)
	sleep(2)
#	take_picture()
	sleep(2)
	servo.ChangeDutyCycle(5)
	sleep(1)
	servo_pwm.ChangeDutyCycle(5)
	sleep(1)




def move_to_the_right():
	print ("turning right")
	servo_pwm.start(0)
	servo.start(0)
	servo_pwm.ChangeDutyCycle(8)
	sleep(1)
	servo.ChangeDutyCycle(7.5)
	sleep(2)
	servo.ChangeDutyCycle(8.5)
	sleep(1)
#	take_picture()
	sleep(1)
	servo.ChangeDutyCycle(5)
	sleep(1)
	servo_pwm.ChangeDutyCycle(5)
	sleep(1)


def take_picture():
	picam2 = Picamera2()
	camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores = {"size": (640, 480)}, display = "lores")
	picam2.configure(camera_config)
	picam2.start_preview(Preview.QTGL)
	picam2.start()
	time.sleep(2)
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	picam2.capture_file(f"your_selfie{timestamp}.jpg")
	sleep(2)
	picam2.stop_preview()
	picam2.close()


while True:
	channel_value = channel.voltage * 4
	channel_two_value = channel_two.voltage * 4
	print ("Analog Value one: ", channel.value, "Voltage: ", channel_value)
	print ("Analog Value two: ", channel_two.value, "Voltage: ", channel_two_value)
	if (channel_value > 14 or channel_two_value > 14):
		print("sound detected")
		if(channel_value > channel_two_value):
			move_to_the_left()
			print ("left mic")
		elif(channel_value < channel_two_value):
			move_to_the_right()
			print("right mic")
		channel_value = channel.voltage * 4
		channel_two_value = channel_two.voltage * 4
	time.sleep(0.1)
