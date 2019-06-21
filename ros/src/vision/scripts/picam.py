from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()

while True:
    time.sleep(0.1)
    
    
