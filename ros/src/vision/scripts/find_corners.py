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
  lines = cv2.HoughLines(edges, 1, np.pi/180, 220)

  for line in lines:
    rho = line[0][0]
    theta = line[0][1]

    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 2)

  return None

if __name__ == "__main__":
  filename = str(sys.argv[1]) if len(sys.argv) > 1 else "building.jpg"
  img = cv2.imread(filename, 1)
  
  intersect_pt = find_corners(img)
  #print("Intersection Point:",intersect_pt)

  cv2.imshow("Image",img)
  cv2.waitKey(0)
