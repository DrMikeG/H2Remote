import time
from picamera2 import Picamera2, Preview
from os import system
import datetime
from time import sleep

tlminutes = 10 #set this to the number of minutes you wish to run your timelapse camera
secondsinterval = 1 #number of seconds delay between each photo taken
fps = 30 #frames per second timelapse video
numphotos = int((tlminutes*60)/secondsinterval) #number of photos to take
print("number of photos to take = ", numphotos)

dateraw= datetime.datetime.now()
datetimeformat = dateraw.strftime("%Y-%m-%d_%H:%M")
print("RPi started taking photos for your timelapse at: " + datetimeformat)

picam = Picamera2()
config = picam.create_preview_configuration()
picam.configure(config)
picam.start()

#system('rm /home/timelapse/Pictures/*.jpg') #delete all photos in the Pictures folder before timelapse start

for i in range(numphotos):
    picam.capture_file('/home/timelapse/Pictures/image{0:06d}.jpg'.format(i))    
    sleep(secondsinterval)
print("Done taking photos.")
picam.stop()
print("Please standby as your timelapse video is created.")

system('ffmpeg -r {} -f image2 -s 1024x768 -nostats -loglevel 0 -pattern_type glob -i "/home/pi/Pictures/*.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p /home/timelapse/Videos/{}.mp4'.format(fps, datetimeformat))
#system('rm /home/pi/Pictures/*.jpg')
print('Timelapse video is complete. Video saved as /home/timelapse/Videos/{}.mp4'.format(datetimeformat))


###
    
