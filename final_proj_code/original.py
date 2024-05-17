import time
import board
import busio
import numpy as np
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn




i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

channel = AnalogIn(ads, ADS.P0)
channel_two = AnalogIn(ads, ADS.P1)


while True:
	channel_two_value = channel_two.voltage * 4
	print ("Analog Value two: ", channel_two.value, "Voltage: ", channel_two_value)
	if (channel_two_value > 5.5):
		print("sound detected on mic 2")
	channel_value = channel.voltage * 4
	print("Analog Value one: ", channel.value, "Voltage: ", channel_value)
	if (channel_value > 9):
		print("sound detected on mic one")


	time.sleep(0.1)
