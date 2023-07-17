import time
from picamera2 import Picamera2, Preview
import os
from os import system
import datetime
from time import sleep

    
dirPath = "/home/timelapse/Pictures/run_002"
print("Using next available directory {}".format(dirPath))

fps = 30 #frames per second timelapse video

dateraw= datetime.datetime.now()
datetimeformat = dateraw.strftime("%Y-%m-%d_%H:%M")
print("Please standby as your timelapse video is created.")
#system('ffmpeg -r {} -f image2 -s 1024x768 -nostats -loglevel 0 -pattern_type glob -i "{}*.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p /home/timelapse/Videos/{}.mp4'.format(fps,dirPath,datetimeformat))
system('ffmpeg -r {} -f image2 -s 1024x768 -pattern_type glob -i "{}/*.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p /home/timelapse/Videos/{}.mp4'.format(fps,dirPath,datetimeformat))
#system('rm /home/pi/Pictures/*.jpg')
print('Timelapse video is complete. Video saved as /home/timelapse/Videos/{}.mp4'.format(datetimeformat))


###
    
