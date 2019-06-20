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

x_cam_width = 640
y_cam_height = 480

#Line with form ax + by + c = 0
class Line:
  def __init__(self, a, b, c):
    self.a = a
    self.b = b
    self.c = c

def get_line(x1,y1,x2,y2):
  if x1 == x2 and y1 == y2:
    raise ValueError("Points coincide")
    return None
  else:
    if x1 == x2:
      return Line(1, 0, -x1)
    else:
      m = (y2-y1)/(x2-x1)
      return Line(-m, 1, (m * x1 - y1))

def get_intersection_pt(l1,l2):
  if l1.a * l2.b == l2.a * l1.b:
    try:
      raise ValueError("Lines have the same slope")   #Clean this up whenever, learning how to raise exceptions
    except ValueError as e:
      print("Value Error: %s" % (e))
      return None

  # x, y  =  solution to the simultaneous linear equations
  #       (l1.a * x + l1.b * y = -l1.c) and
  #       (l2.a * x + l2.b * y = -l2.c) 
  a = np.array(((l1.a, l1.b), (l2.a, l2.b)))
  b = np.array((-l1.c, -l2.c))
  x, y = np.linalg.solve(a,b)

  return (x, y)

def find_corners(img):
  #Convert img to grayscale and do Canny edge det. on img to get Hough lines
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  edges = cv2.Canny(gray, 50, 200, 3)
  lines = cv2.HoughLines(edges, 1, np.pi/180, 220)
  
  #Draw and create equations of lines if at least 4 lines (corner detected)
  line_eqns = [] 
  try:
    if len(lines) >= 4:
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

        cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 2)
        line_eqns.append(get_line(x1,y1,x2,y2))
  except TypeError:
    print("No lines found above set threshold")
    return None

  #Get all intersection points of lines (exclude points off of screen or lines that are parallel)
  intersec_pts = []
  for i in range(len(line_eqns)):
    for j in range(i + 1, len(line_eqns)):
      pt = get_intersection_pt(line_eqns[i], line_eqns[j])
      if pt != None and pt[0] <= x_cam_width and pt[1] <= y_cam_height:
        intersec_pts.append(pt)

  #Decide which intersection point is the corner (right now just getting middle of points)
  x_sum = 0
  y_sum = 0
  for pt in intersec_pts:
    x_sum += pt[0]
    y_sum += pt[1]

  corner_pt = (int(x_sum/len(intersec_pts)), int(y_sum/len(intersec_pts)))

  return corner_pt

if __name__ == "__main__":
  filename = str(sys.argv[1]) if len(sys.argv) > 1 else "building.jpg"
  img = cv2.imread(filename, 1)
  
  corner_pt = find_corners(img)
  print("Intersection Point:",corner_pt)

  cv2.imshow("Image",img)
  cv2.waitKey(0)

  ### Test these helpers more if problems ensue
  # l1 = get_line(1,3,1,5)
  # l2 = get_line(0,4,3,4)
  # print(get_intersection_pt(l1,l2))
