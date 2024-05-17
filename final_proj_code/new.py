import time
import board
import busio
import numpy as np
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn




i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

channel = AnalogIn(ads, ADS.P0)

while True:
	print("Analog Value: ", channel.value, "Voltage: ", channel.voltage)
	time.sleep(0.1)
