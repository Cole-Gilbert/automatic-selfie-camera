import os
import RPi.GPIO as GPIO
import time
import subprocess

#start_time = time.time()
#has_quit = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def send_command(command):
	video_fifo.write(command + "\n")
	video_fifo.flush()

def GPIO17_callback(channel):
	print ("falling edge detected on 17")
	cmd = 'echo "pause" > /home/pi/video_fifo'
	subprocess.check_output(cmd, shell=True)
def GPIO26_callback(channel):
	print ("falling edge detected on 26")
	cmd = 'echo "seek -30" > /home/pi/video_fifo'
	#send_command("seek -30") 
	subprocess.check_output(cmd, shell=True)
def GPIO23_callback(channel):
	print ("falling edge detected on 23")
	cmd = 'echo "seek 10" > /home/pi/video_fifo'
	#send_command("seek 10")
	subprocess.check_output(cmd, shell=True)
def GPIO27_callback(channel):
	print ("falling edge detected on 27")
	cmd = 'echo "seek -10" > /home/pi/video_fifo'
	#send_command("seek -10")
	subprocess.check_output(cmd, shell=True)
def GPIO16_callback(channel):
	print ("falling edge detected on 16")
	cmd = 'echo "seek 30" > /home/pi/video_fifo'
	#send_command("seek 30")
	subprocess.check_output(cmd, shell=True)

GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(26, GPIO.FALLING, callback=GPIO26_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300)
GPIO.add_event_detect(16, GPIO.FALLING, callback=GPIO16_callback, bouncetime=300)
time.sleep(10)

#while (time.time() - start_time < 10) and not has_quit:
	#time.sleep(0.2)
	#try:
		#print ("Waiting for falling edge on port 22")
		#GPIO.wait_for_edge(22, GPIO.FALLING)
		##has_quit = True
		#cmd = 'echo "q" > /home/pi/video_fifo'
		#subprocess.check_output(cmd, shell=True)
		#print ("Falling edge detected on port 22")
	#except KeyboardInterrupt:
		#GPIO.cleanup()
print ("Done")
GPIO.cleanup()
