#! /usr/bin/python
import rospy
import time
import smbus
from BNO055 import BNO055
from shared_msgs.msg import i2c_msg
from shared_msgs.msg import imu_msg



def message_received(msg):
  # This runs on a seperate thread from the pub
  pass

if __name__ == "__main__":
  rospy.init_node('i2c_node')
  imu_pub = rospy.Publisher('imu_data', imu_msg,
	qeue_size = 100)
  imu_pub.rate(50) 
  imu = BNO055()
  if not sensor:
    raise RuntimeError('Failed to initialize BNO055!')
  while not rospy.is_shutdown():
    if imu.update():
      out_message = imu_msg()
      out_message.gyro = {imu.gyro_x, imu.gyro_y, imu.gyro_z}
      out_message.accel = {imu.acceleration_x, imu.acceleration_y, imu.acceleration_z}
      imu_pub.publish(msg)
      r.sleep()

  rospy.spin()
