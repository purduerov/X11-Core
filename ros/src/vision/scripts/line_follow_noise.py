#! /usr/bin/python
import rospy
import cv2      #OpenCV
from cv_bridge import CvBridge, CvBridgeError   #converts between ROS Image messages and OpenCV images
import std_msgs.msg
from sensor_msgs.msg import Image
import numpy as np

bridge = CvBridge()

def get_largest(img):
  pass

#functions that manipulates the data that comes the camera
def process(data):
  #convert img to cv image and convert to HSV
  img = bridge.imgmsg_to_cv2(data,"bgr8")
  img_og = img

  img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) 

  #blurring (median and then gaussian)
  img = cv2.medianBlur(img,5)
  img = cv2.GaussianBlur(img,(5,5),0)
 
  #color filtold for red at top and bottom of hue spectrum
  #red
  #img = cv2.inRange(img,(0/2,150,115),(35/2,255,255))
  #blue
  img = cv2.inRange(img,(216/2,133,67),(230/2,205,236))

  #erode and dilate image
  img =  cv2.erode(img,np.ones((5,5)))
  img =  cv2.dilate(img,np.ones((10,10)))

  #masking
  


  #contouring
  

  #show images
  cv2.imshow("Image",img_og)
  cv2.imshow("Filtered",img)
  cv2.waitKey(3)

if __name__ == "__main__":
  rospy.init_node('line_follow',anonymous=True)
  rospy.Subscriber("/usb_cam/image_raw",Image,process)

  rospy.spin()



