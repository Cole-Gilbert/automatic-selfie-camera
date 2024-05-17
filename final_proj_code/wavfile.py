import pyaudio
import numpy as np
import wave



CHUNK = 4096
FORMAT = pyaudio.paInt32
CHANNELS = 1
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"
RATE = 16000

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT, 
		channels = CHANNELS,
		rate = RATE,
		input = True, 
		frames_per_buffer= CHUNK)

frames = []


try:
#	while True:
	for _ in range (0, int(RATE/CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
#		print(data)
		frames.append(data)
#		samples = np.frombuffer(data, dtype = np.int32)
#		frequencies = np.fft.fft(samples)
#		frequencies = np.abs(frequencies[:len(frequencies)//2])
#		frequencies /= len(samples)

#		peak_frequency_index = np.argmax(frequencies)
#		peak_frequency = peak_frequency_index * RATE / len(samples)

#		print("Dominant frequency:", peak_frequency, "Hz")
except KeyboardInterrupt:
	pass

stream.stop_stream()
stream.close()
p.terminate()

with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))

wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
signal = np.frombuffer(wf.readframes(-1), dtype = np.int32)
wf.close()


frequencies = np.fft.fft(signal)
frequencies = np.abs(frequencies[:len(frequencies)//2])
frequencies /= len(signal)

peak_frequency_index = np.argmax(frequencies)
peak_frequency = peak_frequency_index * RATE/len(signal)

print("Dominant frequency:", peak_frequency, "Hz")


samples = np.frombuffer(b''.join(frames), dtype = np.int32)
frequencies = np.fft.fft(samples)
frequencies = np.abs(frequencies [:len(frequencies)//2])
frequencies /= len(samples)

peak_frequency_index = np.argmax(frequencies)
peak_frequency = peak_frequency_index * RATE/ len(samples)

print("Dominant frequency:", peak_frequency, "Hz")
