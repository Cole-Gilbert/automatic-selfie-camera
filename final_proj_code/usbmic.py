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



#record_command = [
#	'arecord', '--format=S16_LE', '--rate=16000', '--file-type=wav','--duration=5', 'out.wav'
#]
#subprocess.run(record_command, check = True)

audio_file = wave.open('outputfile.wav', 'r')
audio_file1 = wave.open('outputfile1.wav', 'r')

num_frames = audio_file.getnframes()
framerate = audio_file.getframerate()
audio_data = audio_file.readframes(num_frames)
audio_data = np.frombuffer(audio_data, dtype=np.int16)
print (audio_data)
max = np.argmax((audio_data))
print (audio_data[max])


num_frames1 = audio_file1.getnframes()
framerate1 = audio_file1.getframerate()
audio_data1 = audio_file1.readframes(num_frames1)
audio_data1 = np.frombuffer(audio_data1, dtype=np.int16)
print (audio_data1)
max1 = np.argmax((audio_data1))
print (audio_data1[max1])


plt.figure(1)
plt.plot((np.abs(audio_data)), label = 'firstmic')

plt.figure(2)
plt.plot((np.abs(audio_data1)), label ='secondmic')

plt.show()

#fft_data = np.fft.fft(audio_data)

#print (fft_data)

#freq_bins = np.fft.fftfreq(len(fft_data), 1.0/framerate)

#plt.plot(np.abs(audio_data))
#plt.show()
#plt.plot(freq_bins, np.abs(fft_data))
#plt.xlabel('Frequency (Hz)')
#plt.ylabel('Magnitude')


#peak_idx = np.argmax(np.abs(fft_data))
#peak_freq = freq_bins[peak_idx]
#peak_amp = np.abs(fft_data[peak_idx])


#print('Fundamental frequency:', peak_freq, 'Hz')


#harmonics = []
#for i in range(2, 10):
#	harmonic_freq = i * peak_freq
#	harmonic_idx = np.argmin(np.abs(freq_bins - harmonic_freq))
#	harmonic_amp = np.abs(fft_data[harmonic_idx])
#	if harmonic_amp > 0.1 * peak_amp:
#		harmonics.append(harmonic_freq)
#		print('Harmonic', i, 'frequency:', harmonic_freq, 'Hz')
#	plt.axvline(harmonic_freq, color='r')
#	plt.show()


#num_frames1 = audio_file1.getnframes()
#framerate1 = audio_file1.getframerate()


#audio_data1 = audio_file1.readframes(num_frames1)

#audio_data1 = np.frombuffer(audio_data1, dtype=np.int16)


#fft_data1 = np.fft.fft(audio_data1)

#freq_bins1 = np.fft.fftfreq(len(fft_data1), 1.0/framerate1)


#plt.plot(freq_bins1, np.abs(fft_data1))
#plt.xlabel('Frequency (Hz)')
#plt.ylabel('Magnitude')


#peak_idx1 = np.argmax(np.abs(fft_data1))
#peak_freq1 = freq_bins1[peak_idx1]
#peak_amp1 = np.abs(fft_data1[peak_idx1])


#print('Fundamental frequency_one:', peak_freq1, 'Hz')


#harmonics1 = []
#for i in range(2, 10):
#        harmonic_freq1 = i * peak_freq1
#        harmonic_idx1 = np.argmin(np.abs(freq_bins1 - harmonic_freq1))
#        harmonic_amp1 = np.abs(fft_data1[harmonic_idx1])
#        if harmonic_amp1 > 0.1 * peak_amp1:
#                harmonics1.append(harmonic_freq1)
#                print('Harmonic', i, 'frequency:', harmonic_freq1, 'Hz')
#        plt.axvline(harmonic_freq1, color='r')
#       plt.show()
