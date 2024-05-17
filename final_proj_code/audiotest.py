import time
import board
import busio
import numpy as np
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn




i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)


channel = AnalogIn(ads, ADS.P0)
SAMPLE_RATE = 1000
N_SAMPLES = 1024
FREQ_RANGE = (2200, 2800)

while True:
	analog_data = np.zeros(N_SAMPLES, dtype = np.float)
	for i in range(N_SAMPLES):
		analog_data[i]=channel.value
#		print(analog_data)
		time.sleep(1/SAMPLE_RATE)

	fft_result = np.fft.fft(analog_data)
	freqs = np.fft.fftfreq(N_SAMPLES, 1/SAMPLE_RATE)

	start_idx = np.argmax(freqs>= FREQ_RANGE[0])
	end_idx = np.argmax(freqs>= FREQ_RANGE[1])

	peak_idx = np.argmax(np.abs(fft_result[start_idx:end_idx]))

	peak_freq = freqs[start_idx:end_idx][peak_idx]


	if FREQ_RANGE[0] <= peak_freq <= FREQ_RANGE[1]:
		print("Handclap detected at frequency:", peak_freq)

time.sleep(0.1)

