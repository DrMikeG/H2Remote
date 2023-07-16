import time
from picamera2 import Picamera2, Preview

picam = Picamera2()

capture_config = picamera.create_still_configuration()
picam.configure(capture_config)

picam.start()
time.sleep(2)
#picam.capture_file('~/2023_pi_pico_ths/camera/image.jpg')
picam.capture_file('/home/timelapse/Pictures/onepicture.jpg')

picam.close()