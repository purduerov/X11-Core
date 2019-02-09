#! /usr/bin/python
import rospy
import cv2      #OpenCV
from cv_bridge import CvBridge, CvBridgeError   #converts between ROS Image messages and OpenCV images
import std_msgs.msg
from sensor_msgs.msg import Image
import numpy as np

bridge = CvBridge()

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
  cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
  return x,y,w,h

def draw_center(img, contour):
  #Obtain coordinates of the center of mass of the largest contour
  moment = cv2.moments(contour)
  Cx = int(moment['m10']/moment['m00'])
  Cy = int(moment['m01']/moment['m00'])

  # Print the center of mass onto the screen
  cv2.circle(img, (Cx, Cy), 3, (255, 255, 255), -1)
  return (Cx, Cy)


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
  #img = cv2.inRange(img,(0/2,150,115),(35/2,255,255))
  #blue
  img = cv2.inRange(img,(182/2,20 * 2.56,20 * 2.56),(225/2,100 * 2.56,100 * 2.56))
  

  #erode and dilate image
  img =  cv2.erode(img,np.ones((5,5)))
  img =  cv2.dilate(img,np.ones((10,10)))
  
  #contouring
  '''
  contour = np.array([get_largest(img)])
  
  #if contour.size == 0:
    cv2.drawContours(img_og,[contour],0,(0,255,0),3)
  '''
  contour = get_largest(img)	
  
  if contour.all() != -1:
    cv2.drawContours(img_og,[contour],0,(0,255,0),3)
    x,y,w,h = draw_rect(img_og,contour)

  #find moment
  if isContourConvex(contour):
    center = draw_center(img_og, contour)
  else:
    center = draw_center(img_og, contour)

  #show images
  cv2.imshow("Image",img_og)
  cv2.imshow("Filtered",img)
  cv2.waitKey(3)

if __name__ == "__main__":
  rospy.init_node('line_follow',anonymous=True)
  rospy.Subscriber("/usb_cam/image_raw",Image,process)

  rospy.spin()



