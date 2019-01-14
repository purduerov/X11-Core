#! /usr/bin/python
import rospy
import cv2      #OpenCV
from cv_bridge import CvBridge, CvBridgeError   #converts between ROS Image messages and OpenCV images
import std_msgs.msg
from sensor_msgs.msg import Image

bridge = CvBridge()

#functions that manipulates the data that comes the camera
def process(data):
  img = bridge.imgmsg_to_cv2(data,"bgr8")
  
  cv2.imshow("Image",img)
  cv2.waitKey(1)

if __name__ == "__main__":
  rospy.init_node('line_follow',anonymous=True)
  rospy.Subscriber("/usb_cam/image_raw",Image,process)

  rospy.spin()



