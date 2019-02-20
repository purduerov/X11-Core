#! /usr/bin/python
import rospy
from shared_msgs.msg import i2c_msg
from sensor_msgs.msg import Temperature

def message_received(msg):
  # This runs on a seperate thread from the pub
  pass

if __name__ == "__main__":
  rospy.init_node('temp_proc')
  
  # Publish to the CAN hardware transmitter
  pub = rospy.Publisher('temp', Temperature,
      queue_size= 100)

  sub = rospy.Subscriber('i2c_rx', i2c_msg,
      message_received)

  rate = rospy.Rate(10) # 10hz
  # TODO: I2C related activities
  while not rospy.is_shutdown():
    sample_message = Temperature()
    pub.publish(sample_message)
    rate.sleep()
    

