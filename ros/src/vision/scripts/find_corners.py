#! /usr/bin/python
import rospy
import cv2      #OpenCV
from cv_bridge import CvBridge, CvBridgeError   #converts between ROS Image messages and OpenCV images
import std_msgs.msg
from sensor_msgs.msg import Image
import numpy as np
import math as m
from enum import Enum

bridge = CvBridge()

class Corner(Enum):
  LOOKING = 0
  FOLLOWING = 1
  EXITING = 2

class View:
  at_beginning = True
  thresh_rngs = { "red": [(0/2,150,115),(35/2,255,255)],
      "blue": [(182/2,10 * 2.56,12 * 2.56),(265/2,100 * 2.56,100 * 2.56)]}
  def __init__(self,cnt = None, bw_img = None):
    self.cnt = cnt
    self.bw_img = bw_img

def get_largest(img):
  #grab all of the contours
  im, contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

  #iterate through contours to find one with largest area 
  largest_area  = -1 
  largest_cnt = -1
  for i in range(len(contours)):
    area = cv2.contourArea(contours[i])
    if largest_area < area:
	largest_area = area
        largest_cnt = contours[i]

  return largest_cnt

def find_corners(img):
    

def process(data):
  #convert img to cv image and convert to HSV
  img = bridge.imgmsg_to_cv2(data,"bgr8")
  img_og = img

  img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) 

  #blurring (median and then gaussian)
  img = cv2.medianBlur(img,5)
  img = cv2.GaussianBlur(img,(5,5),0)
 
  #blue line threshold
  img = cv2.inRange(img,View.thresh_rngs["blue"][0],View.thresh_rngs["blue"][1])

  #erode and dilate image
  img =  cv2.erode(img,np.ones((5,5)))
  img =  cv2.dilate(img,np.ones((10,10)))
  
  #contouring
  contour = get_largest(img)
  
  #show images
  cv2.imshow("Filtered",img)
  cv2.imshow("Image",img_og)
  cv2.waitKey(3)


if __name__ == "__main__":
  rospy.init_node('find_corners',anonymous=True)
  rospy.Subscriber("/usb_cam/image_raw",Image,process)

  rospy.spin()
