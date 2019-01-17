#! /usr/bin/python
import rospy
import cv2      #OpenCV
from cv_bridge import CvBridge, CvBridgeError   #converts between ROS Image messages and OpenCV images
import std_msgs.msg
from sensor_msgs.msg import Image

bridge = CvBridge()

#functions that manipulates the data that comes the camera
def process(data):
  #convert img to cv image and convert to HSV
  img = bridge.imgmsg_to_cv2(data,"bgr8")
  img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) 
 
  #color filtold for red at top and bottom of hue spectrum
  img_filt = cv2.inRange(img,(0/2,75,48),(30/2,100,75))
  #img_filt = cv2.inRange(img_filt,(),())

  #errode and dilate image


  #contour/mapp the image??

  #show images
  cv2.imshow("Image",img)
  cv2.imshow("Filtered",img_filt)
  cv2.waitKey(1)

if __name__ == "__main__":
  rospy.init_node('line_follow',anonymous=True)
  rospy.Subscriber("/usb_cam/image_raw",Image,process)

  rospy.spin()



