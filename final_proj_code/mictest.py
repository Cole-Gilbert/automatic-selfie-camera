import pyaudio
import numpy as np
import wave
import subprocess
import os



record_command = [
	'arecord', '-D', 'plughw:1', '-c1', '-r', '44100', '-f', 'S32_LE', '-t', 'wav', '-V', 'mono','-v','-d','7', 'output.wav'
]


subprocess.run(record_command, check=True)

wf = wave.open('output.wav', 'rb')
print (wf)
signal = np.frombuffer(wf.readframes(-1), dtype = np.int32)
#signal = signal.astype(np.float32) / np.max(np.abs(signal))
signal -= np.mean(signal)

#print(signal[0])
#print(signal[1])
#print('signal')

wf.close()

window = np.hanning(len(signal))
signal *= window


frequencies = np.fft.fft(signal)
frequencies = np.abs(frequencies[:len(frequencies)//2])
frequencies /= len(signal)
#n = signal.size
#timestep = 0.1
#freq = np.fft.fftfreq(n, d=timestep)
#print(freq)
#print("FFT values:", frequencies)


RATE = 44100

frequency_bins = np.fft.fftfreq(len(signal), 1/RATE)[:len(signal)//2]
peak_frequency_index = np.argmax(frequencies)

print (len(signal))
print (peak_frequency_index)
peak_frequency = frequency_bins[peak_frequency_index]
 
print ("Dominant frequency:", peak_frequency, "Hz")
