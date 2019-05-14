#! /usr/bin/python
import rospy
import cv2      #OpenCV
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String
from sensor_msgs.msg import Image
import numpy as np
import math as m
from enum import Enum
import sys

bridge = CvBridge()

def find_corners(img):
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  edges = cv2.Canny(gray, 50, 200, 3)
  lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, 100, 10)

  for l in lines:
    print(l[0])
    cv2.line(img, (l[0][0],l[0][1]), (l[0][2],l[0][3]), (0,0,255), 2)
    cv2.line(edges, (l[0][0],l[0][1]), (l[0][2],l[0][3]), (0,0,255), 2)

  cv2.imshow("Edges",edges)
  return None

if __name__ == "__main__":
  filename = str(sys.argv[1]) if len(sys.argv) > 1 else "building.jpg"
  img = cv2.imread(filename, 1)
  
  intersect_pt = find_corners(img)
  #print("Intersection Point:",intersect_pt)

  cv2.imshow("Image",img)
  cv2.waitKey(0)
