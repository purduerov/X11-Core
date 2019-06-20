#! /usr/bin/python
from __future__ import print_function 
import rospy
import sys
import cv2
import numpy as np
import imutils

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


bridge = CvBridge()
img = np.zeros((480,640))




def get_largest(im, n):
  # Find contours of the shape
  contours = cv2.findContours(im.copy(), cv2.RETR_LIST,
    cv2.CHAIN_APPROX_NONE)
  contours = imutils.grab_contours(contours)

  # Create array of contour areas
  areas = [cv2.contourArea(contour) for contour in contours]

  # Sort array of areas by size
  sorted_areas = sorted(zip(areas, contours),
    key=lambda x: x[0], reverse=True)

  if sorted_areas and len(sorted_areas) >= n:
  # Find nth largest
    return sorted_areas[n - 1][1]
  else:
    return None





def mouse_callback(event, x, y, flags, params):
  if event == cv2.EVENT_LBUTTONDOWN:
    print (x, y)

def process(data):
  try:
    img= bridge.imgmsg_to_cv2(data, "bgr8")
  except CvBridgeError as e:
    print(e)

  og_img = img
  img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV);
  img = cv2.inRange(img, (200/2,20,20), (236/2,255,220))
  img = cv2.erode(img, np.ones((5,5)))
  img = cv2.dilate(img, np.ones((10,10)))
  contour = get_largest(img, 1)
  print(contour.shape)
  og_img = cv2.drawContours(og_img, contour, -1, (0,255,0), 10)


  mu = cv2.moments(contour)
  cx = int(mu['m10']/mu['m00'])
  cy = int(mu['m01']/mu['m00'])
  cv2.circle(og_img, (cx,cy), 3, (0,0,255))





  

  cv2.imshow("Transformed", og_img)
  cv2.imshow("Dilated", img);
  cv2.waitKey(3)
  


if __name__ == "__main__":
  rospy.init_node("vision_test");

  rospy.Subscriber("/usb_cam/image_raw", Image, process);
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting Down")

  cv2.destroyAllWindows();
