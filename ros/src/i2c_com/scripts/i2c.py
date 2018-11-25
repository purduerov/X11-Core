#! /usr/bin/python
import rospy
from shared_msgs.msg import i2c_msg

def message_received(msg):
  # This runs on a seperate thread from the pub
  pass

if __name__ == "__main__":
  rospy.init_node('i2c_node')
  pub = rospy.Publisher('i2c_rx', i2c_msg,
      queue_size= 100)
  sub = rospy.Subscriber('i2c_tx', i2c_msg,
      message_received)

  # TODO: I2C related activities
  rospy.spin()
