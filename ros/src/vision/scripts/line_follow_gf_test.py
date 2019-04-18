#! /usr/bin/python
"""
Note:  Right now, no image is dispayed until the at_beginning = true if statement completes running.  
"""
import rospy
import cv2      #OpenCV
from cv_bridge import CvBridge, CvBridgeError   #converts between ROS Image messages and OpenCV images
import std_msgs.msg
from sensor_msgs.msg import Image
import numpy as np
from vectors import Vector
import math
import time
bridge = CvBridge()

class View:
  at_beginning = True 
  thresh_rngs = { "red": [(0/2,150,115),(35/2,255,255)],
      "blue": [(182/2,20 * 2.56,20 * 2.56),(225/2,100 * 2.56,100 * 2.56)]}
  def __init__(self,cnt = None, at_beginning = True):
    self.cnt = cnt
  def compare_cnts(self,ex_cnt):
    return cv2.matchShapes(self.cnt,ex_cnt,1,0.0) < .02

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


def draw_rect(img, contour):
  x,y,w,h = cv2.boundingRect(contour)
  cv2.rectangle(img,(x,y), (x+w,y+h), (255,0,0),2)
  
  x_c = x + int(w/2)
  y_c = y + int(h/2)
  cv2.circle(img, (x_c, y_c), 3, (255, 0, 0), -1)
  return [x_c, y_c]


def draw_center(img, contour):
  #Obtain coordinates of the center of mass of the largest contour
  moment = cv2.moments(contour)
  Cx = int(moment['m10']/moment['m00'])
  Cy = int(moment['m01']/moment['m00'])

  # Print the center of mass onto the screen
  cv2.circle(img, (Cx, Cy), 3, (0, 255, 0), -1)
  return [Cx, Cy]


def get_ex_cnts():
  #recognize starting square/circle

  #****FIND A WAY TO ONLY DECLARE THES EX IMAGAES ONCE AND THEN PASS AS NEEDED*******
  squares = [cv2.imread('sq_bl.jpeg',1),cv2.imread('sq_ang_bl.png',1),cv2.imread('sq_noise_bl.png',1)]
  circles = [cv2.imread('circ_bl.png',1),cv2.imread('circ_ang_bl.png',1),cv2.imread('circ_noise_bl.png',1)]
  
  sq_thresh = []
  circ_thresh = []
  #need to do some thresholding in here
  for img in range(len(squares)):
    #Convert to HSV
    squares[img] = cv2.cvtColor(squares[img],cv2.COLOR_BGR2HSV)
    #threshold for blue
    sq_thresh.append(cv2.inRange(squares[img],(182/2,20 * 2.56,20 * 2.56),(225/2,100 * 2.56,100 * 2.56)))
    #filter out noise
    sq_thresh[img] = cv2.erode(sq_thresh[img],np.ones((5,5)))
    sq_thresh[img] = cv2.dilate(sq_thresh[img],np.ones((10,10)))
    
  for img in range(len(circles)):
    #Convert to HSV
    circles[img] = cv2.cvtColor(circles[img],cv2.COLOR_BGR2HSV)
    #threshold for blue
    circ_thresh.append(cv2.inRange(circles[img],(182/2,20 * 2.56,20 * 2.56),(225/2,100 * 2.56,100 * 2.56)))
    
    #filter out noise
    circ_thresh[img] = cv2.erode(circ_thresh[img],np.ones((5,5)))
    circ_thresh[img] = cv2.dilate(circ_thresh[img],np.ones((10,10)))

  sq_cnts = []
  circ_cnts = []
  #getting contours for each image
  for sq, circ in zip(sq_thresh, circ_thresh):
    im, sq_cnt, hierarchy = cv2.findContours(sq,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    im, circ_cnt, hierarchy = cv2.findContours(circ,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    sq_cnts.append(sq_cnt)
    circ_cnts.append(circ_cnt)

  return sq_cnts, circ_cnts


def match_beginning(img,contour,sq_cnts,circ_cnts):
  #find matches that have a matchShape value of less than .02
  match = []
  view = View(contour)
  sq_circ_cnts = sq_cnts + circ_cnts
  while(len(match) == 0):
    match = filter(view.compare_cnts , np.asarray(sq_circ_cnts))
  
  #if a match is found, identify shape in picuture
  if match != -1:
    if match in squares:
      init_shape = "square"
    else:
      init_shape = "circle"

  #surround the found shape in circle
  (x,y), radius = cv2.minEnclosingCircle(contour)
  center = (int(x),int(y))
  radius = int(radius)
  cv2.circle(img,center,radius,(255,0,0),2)

  poles = {"top": (320,0),
	   "bottom": (320,360),
	   "left": (0,180),
	   "right": (640, 180)}
  
  dist = -1
  for pt in poles.itervalues():
    if((center[0] - pt[0])**2 + (center[1] - pt[1])**2 > dist):
      dist = (center[0] - pt[0])**2 + (center[1] - pt[1])**2 
      wall_md_pt = pt

  return wall_md_pt, center, init_shape, view  


def traverse_line(img_og,contour,vects):
  if contour.all() != -1:
    cv2.drawContours(img_og,[contour],0,(0,255,0),3)
    center_rect = draw_rect(img_og, contour)
    center_cnt = draw_center(img_og, contour)

    #find moment
    if cv2.isContourConvex(contour):
      center = center_cnt
    else:
      center = center_rect

    cv2.circle(img_og,(center[0],center[1]), 5, (0,0,0), -1)
    
    start_point_vector = vects.get_vector_start_point()
    curr_thrust_vect, resultant_vect = vects.get_thrust_vect(start_point_vector, center)
  else:
    curr_thrust_vect = np.multiply(vects.prev_vector,-1)
    resultant_vect = [0, 0]

  ####OUTPUT curr_thrust_vect, as this is the direction in which the thrusters should be pushing    MAGNITUDES ARE CURRENTLY AN ISSUE
  '''
  cv2.circle(img_og, (start_point_vector[0],start_point_vector[1]), 3, (0,0,255), -1)
  cv2.line(img_og, (start_point_vector[0],start_point_vector[1]),(center[0],center[1]),(255,0,255),1)
  cv2.line(img_og, (start_point_vector[0],start_point_vector[1]),(curr_thrust_vect[0] + start_point_vector[0], curr_thrust_vect[1] + start_point_vector[1]),(0,255,0),1)
  '''
  #purple line is missing (maybe because it goes out of bounds of view frame???  or is tired of living????)
  cv2.line(img_og, (center[0],center[1]),(center[0] + curr_thrust_vect[0], center[1] +  curr_thrust_vect[0]),(0,255,0),1)
  cv2.line(img_og, (center[0] + curr_thrust_vect[0], center[1] +  curr_thrust_vect[0]),(center[0] + curr_thrust_vect[0] + \
	   resultant_vect[0], center[1] +  curr_thrust_vect[0] + resultant_vect[0]),(255,0,255),1)

  return curr_thrust_vect, resultant_vect

#functions that manipulates the data that comes the camera
def process(data):
  #convert img to cv image and convert to HSV
  img = bridge.imgmsg_to_cv2(data,"bgr8")
  img_og = img

  img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) 

  #blurring (median and then gaussian)
  img = cv2.medianBlur(img,5)
  img = cv2.GaussianBlur(img,(5,5),0)
 
  #red
  #img = cv2.inRange(img,thresh_rngs["blue"][0],thresh_rngs["blue"][1])
  #blue
  img = cv2.inRange(img,(182/2,20 * 2.56,20 * 2.56),(225/2,100 * 2.56,100 * 2.56))

  #erode and dilate image
  img =  cv2.erode(img,np.ones((5,5)))
  img =  cv2.dilate(img,np.ones((10,10)))
  
  #contouring
  contour = get_largest(img)
  view = View(contour)
  vects = Vector()

  if View.at_beginning:
    print("at beginning")
    '''
    #Code to be run only at the start
    sq_cnts, circ_cnts = get_ex_cnts()
    wall_md_pt, center, init_shape = match_beginning(img,view.cnt,sq_cnts,circ_cnts)

    Vector.prev_vector = [center[0] - wall_md_pt[0],center[1] - wall_md_pt[1]]
    '''
    Vector.prev_vector = [1, 1]
    wall_md_pt = [Vector.x_cam_width / 2, Vector.y_cam_height]
    center = [Vector.x_cam_width / 2, Vector.y_cam_height / 2]

    start_point_vector = [center[0] - wall_md_pt[0],center[1] - wall_md_pt[1]]
    curr_thrust_vect, resultant_vect = vects.get_thrust_vect(wall_md_pt, center)

    #Output thrust vect as cv2 line
    cv2.circle(img_og,(start_point_vector[0],start_point_vector[1]), 3, (0,0,255), -1)
    cv2.line(img_og, (start_point_vector[0],start_point_vector[1]),(wall_md_pt[0],wall_md_pt[1]),(150,255,255),1)
    View.at_beginning = False
    print("Waiting")
    time.sleep(7)
    print("Done waiting")
  else:
    curr_thrust_vect, resultant_vect = traverse_line(img_og,view.cnt,vects)
    print("curr_thr: [%d, %d], resultant: [%d, %d]" % (curr_thrust_vect[0], curr_thrust_vect[1], resultant_vect[0], resultant_vect[1]))

  #Set resultant vect to prev_vector 
  Vector.prev_vector = resultant_vect
  
  #show images
  cv2.imshow("Image",img_og)
  cv2.imshow("Filtered",img)
  cv2.waitKey(3)
  

if __name__ == "__main__":
  if (View.at_beginning == True):
    rospy.Subscriber("/usb_cam/image_raw",Image,process)

  rospy.init_node('line_follow_gf_test',anonymous=True)
  rospy.Subscriber("/usb_cam/image_raw",Image,process)

  rospy.spin()

# vim: set tabstop=2 shiftwidth=2 fileencoding=utf-8 noexpandtab: 
