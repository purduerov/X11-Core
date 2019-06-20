#! /usr/bin/python
import rospy
import cv2      #OpenCV
from cv_bridge import CvBridge, CvBridgeError   #converts between ROS Image messages and OpenCV images
from std_msgs.msg import String
from sensor_msgs.msg import Image
import numpy as np
import math as m
from enum import Enum

bridge = CvBridge()

class Corner(Enum):
  LOOKING = 0
  FOLLOWING = 1
  EXITING = 2

# class StartPoint(Enum):
#   UP = 0
#   RIGHT = 1
#   DOWN = 2
#   LEFT = 3
  
class Vector:
  prev_vector = []
  x_cam_width = 640
  y_cam_height = 480
  def __init__(self,thrust_vect = [], resultant_vect = [], start_point = []):
    self.thrust_vect = thrust_vect
    self.resultant_vect = resultant_vect  
    self.start_point =  start_point 

  def get_corner_detect(self):
    #This function returns enums for 1 of four directions if a corner is detected, and another separate enum for no corner detected

    if(not corner_detected):
      return Corner.NO_CORNER
    else:
      #Decision-making for which corner to output.
        
    
  def get_vector_start_point(self):
    origin = [0, 0]
    prev_mag = m.sqrt((self.prev_vector[0])**2 + (self.prev_vector[1]**2))
    unit_vect = [self.prev_vector[0]/prev_mag, self.prev_vector[1]/prev_mag]
    if(abs(unit_vect[0]) > abs(unit_vect[1])):
      if (unit_vect[0] > 0):
        #This origin point is the left middle
        print("left middle")
        start_point = [origin[0], origin[1] + self.y_cam_height / 2]
      else:
        #This origin point is the right middle
        print("right middle")
        start_point = [origin[0] + self.x_cam_width, origin[1] + self.y_cam_height / 2]  
    else:
      if (unit_vect[1] < 0):
        #This origin point is the bottom middle
        print("bottom middle")
        start_point = [origin[0] + self.x_cam_width / 2, origin[1] + self.y_cam_height]
      else:
        #This origin point is the top middle
        start_point = [origin[0] + self.x_cam_width / 2, origin[1]] 
        print("top middle")

    self.start_point = start_point

  def get_thrust_vect(self, center):
    self.resultant_vect = [center[0] - self.start_point[0], center[1] - self.start_point[1]]
    self.thrust_vect = [self.resultant_vect[0] - self.prev_vector[0], self.resultant_vect[1] - self.prev_vector[1]] 
    
    return self.thrust_vect, self.resultant_vect  

class View:
  at_beginning = True
  beginning_frames_seen = 0; 
  thresh_rngs = { "red": [(0/2,150,115),(35/2,255,255)],
      "blue": [(182/2,10 * 2.56,12 * 2.56),(265/2,100 * 2.56,100 * 2.56)]}
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

def match_beginning(img,contour,sq_cnts,circ_cnts):
  '''
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
  '''
  return None


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
    cv2.circle(img_og,(center[0],center[1]), 7, (0,0,0), -1)
 
    vects.get_vector_start_point()
    thrust_vect, resultant_vect = vects.get_thrust_vect(center)
  else:
    thrust_vect = np.multiply(Vector.prev_vector,-1)
    resultant_vect = [0, 0]

  #### MAGNITUDES ARE CURRENTLY AN ISSUE -- Need a base_load thrust
  #draw previous vector - yellow
  cv2.line(img_og, (vects.start_point[0],vects.start_point[1]), (vects.start_point[0] + Vector.prev_vector[0],vects.start_point[1] + Vector.prev_vector[1]),(18,222,218),6)
  #draw resultant vector - orange
  cv2.line(img_og, (vects.start_point[0],vects.start_point[1]),(vects.start_point[0] + resultant_vect[0], vects.start_point[1] +  resultant_vect[1]),(15,125,210),3)
  #draw thrust vector - red
  cv2.line(img_og, (center[0] - thrust_vect[0], center[1] - thrust_vect[1]),(center[0],center[1]),(0,0,255),1)   

  return thrust_vect, resultant_vect

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
  #img = cv2.inRange(img,View.thresh_rngs["red"][0],View.thresh_rngs["red"][1])
  #blue
  img = cv2.inRange(img,View.thresh_rngs["blue"][0],View.thresh_rngs["blue"][1])

  #erode and dilate image
  img =  cv2.erode(img,np.ones((5,5)))
  img =  cv2.dilate(img,np.ones((10,10)))
  
  #contouring
  contour = get_largest(img)
  view = View(contour)
  vects = Vector()

  if View.at_beginning:
    print("at beginning")
    View.beginning_frames_seen += 1
    '''
    #Code to be run only at the start
    sq_cnts, circ_cnts = get_ex_cnts()
    wall_md_pt, center, init_shape = match_beginning(img,view.cnt,sq_cnts,circ_cnts)

    Vector.prev_vector = [center[0] - wall_md_pt[0],center[1] - wall_md_pt[1]]
    '''
    Vector.prev_vector = [0, 5]
    vects.start_point = [Vector.x_cam_width / 2, Vector.y_cam_height]
    center = [Vector.x_cam_width / 2, Vector.y_cam_height / 2]

    thrust_vect, resultant_vect = vects.get_thrust_vect(center)
    if (View.beginning_frames_seen == 5):
      View.at_beginning = False

    #draw previous vector - yellow
    cv2.line(img_og, (vects.start_point[0],vects.start_point[1]), (vects.start_point[0] + Vector.prev_vector[0],vects.start_point[1] + Vector.prev_vector[1]),(18,222,218),7)
    #draw resultant vector - orange
    cv2.line(img_og, (vects.start_point[0],vects.start_point[1]),(vects.start_point[0] + resultant_vect[0], vects.start_point[1] +  resultant_vect[1]),(15,125,210),5)
    #draw thrust vector - red
    cv2.line(img_og, (center[0] - thrust_vect[0], center[1] - thrust_vect[1]),(center[0],center[1]),(0,0,255),3)
  else:
    thrust_vect, resultant_vect = traverse_line(img_og,view.cnt,vects)
    #print("curr_thr: [%d, %d], resultant: [%d, %d]" % (thrust_vect[0], thrust_vect[1], resultant_vect[0], resultant_vect[1]))
      
    #Publish unit thrust vector
    thrust_mag = m.sqrt((thrust_vect(center)[0])**2 + (thrust_vect(center)[1])**2)
    unit_thrust_vect = [thrust_vect[0]/prev_mag, thrust_vect[1]/thrust_mag]

    pub = rospy.Publisher("thrust_output_topic",String,queue_size=10)
    pub.publish(String(unit_thrust_vect))


  #Set resultant vect to prev_vector 
  Vector.prev_vector = resultant_vect
  
  #Show images
  cv2.imshow("Filtered",img)
  cv2.imshow("Image",img_og)
  cv2.waitKey(3)


if __name__ == "__main__":
  rospy.init_node('line_follow',anonymous=True)
  rospy.Subscriber("/usb_cam/image_raw",Image,process)

  rospy.spin()
