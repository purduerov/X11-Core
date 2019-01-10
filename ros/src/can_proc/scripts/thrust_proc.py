#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg, thrust_control_msg, esc_single_msg

def message_received(msg):
  # This runs on a seperate thread from the pub
  pass

if __name__ == "__main__":
  rospy.init_node('thrust_proc')
  
  # Publish to the CAN hardware transmitter
  can_pub = rospy.Publisher('can_tx', can_msg,
      queue_size= 10)
  esc_pub = rospy.Publisher('esc_single', esc_single_msg,
      queue_size= 10)

  sub = rospy.Subscriber('thrust_control', thrust_control_msg,
      message_received)

  rate = rospy.Rate(10) # 10hz
  # TODO: I2C related activities
  while not rospy.is_shutdown():
    sample_message = can_msg()
    can_pub.publish(sample_message)
    sample_message = esc_single_msg()
    esc_pub.publish(sample_message)
    rate.sleep()
    

