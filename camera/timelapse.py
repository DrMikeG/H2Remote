import time
from picamera2 import Picamera2, Preview
import os
from os import system
import datetime
from time import sleep

def does_file_exist(filename):
    try:
        status = os.stat(filename)
        file_exists = True
    except OSError:
        file_exists = False
    return file_exists

def does_directory_exist(filename):
    try:
        status = os.stat(filename)
        isdir = status[0] & 0x4000
    except OSError:
        isdir = False
    return isdir

def get_next_run_path():
    basePath = "/home/timelapse/Pictures/run_"
    threeDigitNumberAsString = "000"
    # Keep generating numbers until find an unused folder name
    # and then create the folder
    # and return the path
    for i in range(1000):
        path = "/home/timelapse/Pictures/run_{0:0>3}".format(i)
        if not does_directory_exist(path):
            os.mkdir(path)
            return path
    print("Card too full! (over 999 directories)")

dirPath = get_next_run_path()
print("Using next available directory {}".format(dirPath))

tlminutes = 720 #set this to the number of minutes you wish to run your timelapse camera
secondsinterval = 10 #number of seconds delay between each photo taken
fps = 30 #frames per second timelapse video
# One frame every 10 seconds is 6 frames per minute
# @30fps thats 5 minutes per second
# or 20 seconds per hour

numphotos = int((tlminutes*60)/secondsinterval) #number of photos to take
print("number of photos to take = ", numphotos)

dateraw= datetime.datetime.now()
datetimeformat = dateraw.strftime("%Y-%m-%d_%H:%M")
print("RPi started taking photos for your timelapse at: " + datetimeformat)

picam = Picamera2()
picam.still_configuration.size = (1600, 1200)
picam.still_configuration.enable_raw()
picam.still_configuration.raw.size = picam.sensor_resolution
picam.start()

#system('rm /home/timelapse/Pictures/*.jpg') #delete all photos in the Pictures folder before timelapse start

for i in range(numphotos):
    picam.switch_mode_and_capture_file("still", '{}/image{:06d}.jpg'.format(dirPath,i))
    sleep(secondsinterval)
print("Done taking photos.")
picam.stop()
#print("Please standby as your timelapse video is created.")

#system('ffmpeg -r {} -f image2 -s 1024x768 -nostats -loglevel 0 -pattern_type glob -i "/home/timelapse/Pictures/*.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p /home/timelapse/Videos/{}.mp4'.format(fps, datetimeformat))
#system('rm /home/pi/Pictures/*.jpg')
#print('Timelapse video is complete. Video saved as /home/timelapse/Videos/{}.mp4'.format(datetimeformat))


###
    
