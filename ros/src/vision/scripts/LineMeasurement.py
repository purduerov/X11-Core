#! /usr/bin/python

import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError   #converts between ROS Image messages and OpenCV images
from sensor_msgs.msg import Image
from imutils import grab_contours

bridge = CvBridge()

""" OpenCV has a predisposition to find a lot of lines on top of eachother, this code should limit that"""
def find_strong_lines(weak_lines, thresh = 400):

    current_lines = []
    for rho, theta in weak_lines: # Make sure the line is oriented positively
        if rho < 0:
            rho *= -1
            theta -= np.pi 

        if len(current_lines) == 0:
          current_lines.append((rho, theta))
          continue

        np_current_lines = np.asarray(current_lines)
        close_rho = np.isclose(rho, np_current_lines[:, 0], atol=thresh)  # lines should be far from each other
        close_theta = np.isclose(theta, np_current_lines[:, 1], atol=np.pi/4)
        close_lines = np.all([close_rho, close_theta], axis=0)

        if not any(close_lines):
           current_lines.append((rho, theta))

    return current_lines


def measure_img(orig_img):

  hsvImage = cv2.cvtColor(orig_img, cv2.COLOR_BGR2HSV)
  redMask = cv2.add(cv2.inRange(hsvImage, (0, 150, 45), (13, 255, 255)),
                    cv2.inRange(hsvImage, (150, 150, 45), (180, 255, 255)))
  blueMask = cv2.inRange(hsvImage, (100, 100, 45), (140, 255, 255))


  # Locate Horizontal and vertical lines
  _, lineMask = cv2.threshold(cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY), 25, 255, cv2.THRESH_BINARY_INV)
  kernel = np.ones((3, 3))
  lineMask = cv2.erode(lineMask, kernel)
  lineMask = cv2.dilate(lineMask, kernel)
  weak_lines = cv2.HoughLines(lineMask, 1, np.pi/180, 200)

  y_intercepts = []
  x_intercepts = []
  if weak_lines is None:
    return

  lines = find_strong_lines(weak_lines[:, 0, :], thresh=int(lineMask.shape[0]* .3))
  # Go through each of the detected lines for measurement
  for rho, theta in lines:
      a = np.cos(theta)
      b = np.sin(theta)
      x0 = a*rho
      y0 = b*rho
      x1 = int(x0 + 1000*(-b))
      y1 = int(y0 + 1000*(a))
      x2 = int(x0 - 1000*(-b))
      y2 = int(y0 - 1000*(a))


      # Line is horizontal
      if theta < np.pi /4:
          x_intercepts.append(np.cos(theta) * rho)
      else:
          y_intercepts.append(np.sin(theta) * rho)


      cv2.line(orig_img,(x1,y1),(x2,y2),(0,255,0),2)

  ratio = 1
  intersection = False
  # If we found more than one vertical line
  if len(x_intercepts) > 1:
      # If there's an x and y intercept then there's a corner!
      if len(y_intercepts):
          c1 = [x_intercepts[0], y_intercepts[0]]
          c2 = [x_intercepts[1], y_intercepts[0]]
          dist = np.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
          known_dist = .30
          ratio = known_dist / dist
          intersection = True
  elif len(y_intercepts) > 1:
      if len(x_intercepts):
          c1 = [x_intercepts[0], y_intercepts[0]]
          c2 = [x_intercepts[0], y_intercepts[1]]
          dist = np.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
          known_dist = .30
          ratio = known_dist / dist
          intersection = True

  contours = cv2.findContours(blueMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  contours = grab_contours(contours)

  # If we found any contours
  if len(contours):
      width, height = cv2.minAreaRect(contours[0])[1]
      centerX, centerY = cv2.minAreaRect(contours[0])[0]
      length = width if width > height else height
      vertical = True if height > width else False

      # Only save measurement while camera is looking straight on (error less than 30 px)
      if not vertical and intersection and abs(centerX - blueMask.shape[1] / 2) < 30:
          print length
          print "Actual distance: " + str(length * ratio)
      elif vertical and intersection and abs(centerY - blueMask.shape[0] / 2) < 30:
          print length
          print "Actual distance: " + str(length * ratio)
  cv2.imshow("RedMask", orig_img)
  cv2.waitKey(1)

def image_callback(image_message):
  img = bridge.imgmsg_to_cv2(image_message,"bgr8")
  measure_img(img)

if __name__ == "__main__":
  rospy.init_node('line_measurement')
  rospy.Subscriber("/usb_cam/image_raw", Image, image_callback)
  rospy.spin()

