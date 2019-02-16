#! /usr/bin/python
import rospy
import time
import smbus
from BNO055 import BNO055
from TYS01 import TSYS01
from shared_msgs.msg import imu_msg
from shared_msgs.msg import temp_message

IMU_PUB_RATE = 50


def message_received(msg):
  # This runs on a seperate thread from the pub
  pass

if __name__ == "__main__":
  rospy.init_node('i2c_node')
  imu_pub = rospy.Publisher('imu_data', imu_msg, qeue_size = 100)
  imu_pub.rate(IMU_PUB_RATE)
  temp_pub = rospy.Publisher('temp_data', temp_msg, qeue_size = 100)
  imu = BNO055()
  temp = TYS01()
  temp.init()
  while not rospy.is_shutdown():
    # using imu rate to poll the temp sensor as well beacuse IMU updates faster
    if imu.update():
      out_message = imu_msg()
      out_message.gyro = {imu.gyro_x(), imu.gyro_y(), imu.gyro_z()}
      out_message.accel = {imu.acceleration_x, imu.acceleration_y, imu.acceleration_z}
      imu_pub.publish(out_message)
      # read the temp in C and send it to a ros
      temp_message = temp_msg()
      temp_message.temperature = {temp.temperature()}
      temp_pub.publish(temp_message)
      r.sleep()

  rospy.spin()
