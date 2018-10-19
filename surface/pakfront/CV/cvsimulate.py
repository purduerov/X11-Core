"""
CV simulate simulates a cv process
"""
#!/usr/bin/env  python
from CVhandles import pushframe, pushdata
import time
import cv2
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

imglink = "https://i.pinimg.com/originals/00/21/52/002152ecac89b72d602059193ebdc161.jpg"
"""
to use cv simulate, place a test image in your home directory named 
testimage.jpg" an example working test image was placed in the pakfront foler
"""
if __name__ == "__main__":
    curimage = cv2.imread("$HOME/testimage.jpg")
    while True:
        #curimage = get_image(0)
        data = {"Foo":imglink}
        time.sleep(0.1)
        # CV stuff goes here
        pushframe(curimage, 1)
        pushdata(data, 1)
