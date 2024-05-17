#!/bin/bash

sudo rm -r /home/pi/final_proj/photo_library/*

./mic_loop.sh & 

#run the pitft interface
sudo python3 start_screen.py

