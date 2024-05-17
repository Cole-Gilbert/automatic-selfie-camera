#!/bin/bash

while true; do
	arecord -D plughw:4,0 -f cd -t wav -r 44100 -c 2 -d 5 outputfile.wav & arecord -D plughw:3,0 -f cd -t wav -r 44100 -c 2 -d 5 outputfile1.wav
	echo "micloop"
	sleep 1
done
