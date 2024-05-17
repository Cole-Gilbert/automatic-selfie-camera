import RPi.GPIO as GPIO
import os
import time
import board
import busio
import numpy as np
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
servo_pwm = GPIO.PWM(17, 50)

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

channel = AnalogIn(ads, ADS.P0)
channel_two = AnalogIn(ads, ADS.P1)

while True:
	channel_value = channel.voltage * 4
	channel_two_value = channel_two.voltage * 4
	print ("Analog Value one: ", channel.value, "Voltage: ", channel_value)
	print ("Analog Value two: ", channel_two.value, "Voltage: ", channel_two_value)
	while (channel_value > 11 or channel_two_value > 11):
		print("sound detected")
		if(channel_value > channel_two_value):
			print ("mic1 is greater")
		elif(channel_value < channel_two_value):
			print("mic2 is greater")
		channel_value = channel.voltage * 4
		channel_two_value = channel_two.voltage * 4
	time.sleep(0.1)

