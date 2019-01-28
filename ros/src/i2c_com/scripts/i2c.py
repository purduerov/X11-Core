#! /usr/bin/python
import rospy
from shared_msgs.msg import i2c_msg
from threading import Thread, Lock

#mutex = Lock()

def message_received(msg):
  # This runs on a seperate thread from the pub
  m = i2c_msg()
  m.data = msg.data
  m.addr = msg.addr
  
  rospy.loginfo(m)
  pass

if __name__ == "__main__":
  rospy.init_node('i2c_node')
  pub = rospy.Publisher('i2c_rx', i2c_msg,
      queue_size= 100)
  sub = rospy.Subscriber('i2c_tx', i2c_msg,
      message_received)

  # TODO: I2C related activities
  rospy.init_node('talker', anomymous=True)
  rate = rospy.Rate(10) # 10hz

  msg = i2c_msg()
  while not rospy.is_shutdown():
    rospy.loginfo(msg)
    pub.publish(msg)
    rate.sleep()
  
  rospy.spin()
