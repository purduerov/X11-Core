#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg

def message_received(msg):
  # This runs on a seperate thread from the pub
  pass

if __name__ == "__main__":
  rospy.init_node('can_node')
  pub = rospy.Publisher('can_rx', can_msg,
      queue_size= 100)
  sub = rospy.Subscriber('can_tx', can_msg,
      message_received)

  # TODO: CAN related activities
  rospy.spin()
