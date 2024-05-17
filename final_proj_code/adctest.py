import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import scipy.fft as fft
import numpy as np
import matplotlib.pyplot as plt
import sys

print (sys.path)

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

channel = AnalogIn(ads, ADS.P0)


adc.gain = 1

chan = AnalogIn(ads, ADS.P0)


sampling_rate = 1000
num_samples = 1024


analog_values = []

for _ in range(num_samples):
	analog_values.append(chan.value)

fft_result = fft.fft(analog_values)
fft_freqs = fft.fftfreq(num_samples, 1/sampling_rate)


magnitude_spectrum = np.abs(fft_result)


plt.figure(figsize = (10,6))
plt.plot(fft_freqs, magnitude_spectrum)
plt.title("Magnitude Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid(True)
plt.show()
