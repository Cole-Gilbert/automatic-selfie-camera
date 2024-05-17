#!/bin/bash
#
# script to control the video with buttons

sudo SDL_VIDEODRIVER=fbcon SDL_FBDEV=/dev/fb1 mplayer -input file="/home/pi/video_fifo" -vo sdl -framedrop bigbuckbunny320p.mp4 &
echo "bunny playing"

python3 "/home/pi/more_video_control.py" 
echo "video control called"

#mplayer -input file="/home/pi/video_fifo" bigbuckbunny320p.mp4
