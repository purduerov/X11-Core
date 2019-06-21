#! /usr/bin/python
from __future__ import print_function 
import rospy
import sys
import cv2
import numpy as np

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


bridge = CvBridge()
img = np.zeros((480,640))

def mouse_callback(event, x, y, flags, params):
  if event == cv2.EVENT_LBUTTONDOWN:
    print (x, y)

def process(data):
  print("Should have displayed image")
  try:
    img= bridge.imgmsg_to_cv2(data, "bgr8")
  except CvBridgeError as e:
    print(e)

  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
  og = img.copy()

  (rows, cols) = img.shape
  cv2.circle(img, (cols/2, rows/2),2, 255,
      thickness=10)



  # For paper lying on ground 
  H2 = cv2.findHomography(np.array([(198,304), (268,304), (187,355), (273,353)]), 
                     np.array([(0,0), (75,0), (0,101), (75,101)]))

  # For whole ground
  height = 420
  H2 = cv2.findHomography(np.array([(0,244), (640,244), (0,480), (640,480)]), 
                     np.array([(0,0), (640,0), (160,height), (640-160, height)]))


  img = cv2.warpPerspective(img, H2[0], (640, height))
  cv2.imshow("Transformed", img)
  cv2.imshow("Original", og);
  cv2.setMouseCallback("Original", mouse_callback)
  cv2.waitKey(3)
  


if __name__ == "__main__":
  rospy.init_node("vision_test");

  rospy.Subscriber("/usb_cam/image_raw", Image, process);
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting Down")

  cv2.destroyAllWindows();
