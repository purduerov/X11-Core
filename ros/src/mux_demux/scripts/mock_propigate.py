#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg, auto_command_msg, thrust_status_msg, thrust_command_msg, esc_single_msg
from sensor_msgs.msg import Imu, Temperature
from std_msgs.msg import Float32

import random

mock = thrust_command_msg()

def mock_catch(msg):
  global mock
  mock = msg

if __name__ == "__main__":
    rospy.init_node('mock_prop')
    ns = rospy.get_namespace() # This should return /surface

    status_sub = rospy.Subscriber(ns + 'thrust_mock',
        thrust_command_msg, mock_catch)

    # Publishers out onto the ROS System
    thrust_pub = rospy.Publisher(ns + 'thrust_command',
      thrust_command_msg, queue_size=10)

    rate = rospy.Rate(50) # 50hz
    # TODO: I2C related activities
    while not rospy.is_shutdown():
      thrust_pub.publish(mock)
      rate.sleep()
      

