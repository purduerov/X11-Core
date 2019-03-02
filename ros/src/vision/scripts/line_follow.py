#! /usr/bin/python
import rospy
import cv2      #OpenCV
from cv_bridge import CvBridge, CvBridgeError   #converts between ROS Image messages and OpenCV images
import std_msgs.msg
from sensor_msgs.msg import Image
import numpy as np
from vector_functions import getVectorStartPoint, getThrustVect
import math

bridge = CvBridge()

#Change these global variable to a class later on
thresh_rngs = { "red": [(0/2,150,115),(35/2,255,255)],
		"blue": [(182/2,20 * 2.56,20 * 2.56),(225/2,100 * 2.56,100 * 2.56)]
	      }
at_beginning = True

class View:
  def __init__(self,cnt):
    self.cnt = cnt
  
  def compare_cnts(self,ex_cnt):
    return cv2.matchShapes(contour,ex_cnt) < .02
    

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
  squares = [cv2.imread('sq_bl.png'),cv2.imread('sq_ang_bl.png'),cv2.imread('sq_noise_bl.png')]
  circles = [cv2.imread('circ_bl.png'),cv2.imread('circ_ang_bl.png'),cv2.imread('circ_noise_bl.png')]
 
  #need to do some thresholding in here
  squares[img] = bridge.imgmsg_to_cv2(squares[img],"bgr8") for img in range(len(squares)) 
  circles[img] = bridge.imgmsg_to_cv2(circles[img],"bgr8") for img in range(len(circles)) 
   
  squares[img] = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) for img in range(len(squares)) 
  circles[img] = bridge.imgmsg_to_cv2(circles[img],"bgr8") for img in range(len(circles)) 


  #getting contours for each image
  sq_cnts = []
  circ_cnts = []
  for sq, circ in zip(squares, circles):
    im, sq_cnt, hierarchy = cv2.findContours(sq,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    im, circ_cnt, hierarchy = cv2.findContours(circ,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    sq_cnts.append(sq_cnt)
    circ_cnts.append(circ_cnt)

  return sq_cnts, circ_cnts


def match_beggining(contour,sq_cnts,circ_cnts):
  #find matches that have a matchShape value of less than .02
  match = []
  view = View(contour)
  while(len(match) == 0):
    match = filter(view.compare_cnts , sq_cnts + circ_cnts)
  
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
      init_pt = pt

  return (init_pt,center),init_shape  


def traverse_line():
  if contour.all() != -1:
    cv2.drawContours(img_og,[contour],0,(0,255,0),3)
    center_rect = draw_rect(img_og, contour)
    center_cnt = draw_center(img_og, contour)
    cv2.line(img_og,(center_rect[0],center_rect[1]),(center_cnt[0],center_cnt[1]), (0,0,255),1)

  #find moment
  if cv2.isContourConvex(contour):
    center = center_cnt
  else:
    center = center_rect

  cv2.circle(img_og,(center[0],center[1]), 5, (0,0,0), -1)
  print(center)
  
##### NEED A PREV VECTOR VALUE TO INITIALIZE TO.  (Could possibly default to one of the four main directions
  startPointVector = getVectorStartPoint(prevVector)
  curr_thrust_vect, resultant_vect = getThrustVect(prevVector, startPointVector, center)
####OUTPUT curr_thrust_vect, as this is the direction in which the thrusters should be pushing    MAGNITUDES ARE CURRENTLY AN ISSUE
  cv2.circle(img_og,(startPointVector[0],startPointVector[1]), 3, (0,0,255), -1)
  cv2.line(img_og, (startPointVector[0],startPointVector[1]),(center[0],center[1]),(150,255,255),1)


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
  
  global at_beginning
  if (at_beginning):
    #Code to be run only at the start
    at_beginning = False
  else:
    #In here goes the code that we run every time.  
  #contouring
  contour = get_largest(img)	
  
   
  

  #show images
  cv2.imshow("Image",img_og)
  cv2.imshow("Filtered",img)
  cv2.waitKey(3)

if __name__ == "__main__":
  rospy.init_node('line_follow',anonymous=True)
  rospy.Subscriber("/usb_cam/image_raw",Image,process)

  rospy.spin()


# vim: set tabstop=2 shiftwidth=2 fileencoding=utf-8 noexpandtab: 
