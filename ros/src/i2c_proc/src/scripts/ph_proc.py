#! /usr/bin/python
import rospy
from shared_msgs.msg import i2c_msg
from std_msgs.msg import Float32

def message_received(msg):
  # This runs on a seperate thread from the pub
  pass

if __name__ == "__main__":
  rospy.init_node('ph_proc')
  
  sub = rospy.Subscriber('i2c_rx', i2c_msg,
      message_received)
  pub= rospy.Publisher('ph', Float32,
    queue_size=10);

  rate = rospy.Rate(10) # 10hz

  # TODO: I2C related activities
  while not rospy.is_shutdown():
    pub.publish(Float32())
    rate.sleep()
    

