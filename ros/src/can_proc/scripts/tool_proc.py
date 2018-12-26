#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg

def message_received(msg):
  # This runs on a seperate thread from the pub
  pass

if __name__ == "__main__":
  rospy.init_node('tool_proc', anonymous=True)
  
  # Publish to the CAN hardware transmitter
  pub = rospy.Publisher('can_tx', can_msg,
      queue_size= 100)

  sub = rospy.Subscriber('tool_control', can_msg,
      message_received)

  rate = rospy.Rate(10) # 10hz
  # TODO: I2C related activities
  while not rospy.is_shutdown():
    sample_message = can_msg()
    pub.publish(sample_message)
    rate.sleep()
    

