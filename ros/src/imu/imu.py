#! /usr/bin/python
import rospy
#TODO make imu_message

def message_received(msg):
  # This runs on a seperate thread from the pub
  pass

if __name__ == "__main__":
  rospy.init_node('imu_node')
  pub = rospy.Publisher('imu_rx', i2c_msg,
      queue_size= 100)
  sub = rospy.Subscriber('imu_tx', i2c_msg,
      message_received)

  # TODO: I2c parsing and returning  
  # TODO: publish the correct values from the IMU
  rospy.spin()
