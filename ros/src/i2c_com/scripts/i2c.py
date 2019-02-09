#! /usr/bin/python
import rospy
from shared_msgs.msg import i2c_msg
from smbus2 import SMBusWrapper
from threading import Thread, Lock

#mutex = Lock()

def message_received(msg):
  # This runs on a seperate thread from the pub

  # Read block of 8 bytes from 'i2c_tx', offest 0
  with SMBusWrapper(1) as bus:
    b = bus.read_i2c_block_data(i2c_tx, 0, 8)
    b = bus.read_i2c_block_data(i2c_tx, 0, 64)
    
    # Set i2c_msg type
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

  # Set rate and tell ROS node name
  rospy.init_node('talker', anomymous=True)
  rate = rospy.Rate(10) # 10hz

  # Get i2c_msg type
  msg = i2c_msg()
  
  # Publish msg to topic
  while not rospy.is_shutdown():
    rospy.loginfo(msg)
    pub.publish(msg)
    rate.sleep()
  
  rospy.spin()
