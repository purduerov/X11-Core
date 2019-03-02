#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg, auto_control_msg, auto_command_msg
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32

imu_output = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def imu_received(msg):
  #set IMU output variable to message type based on ROS sensor_msgs standard
  #might change to be specific to the output of our IMU -----------------------------------------------------
  global imu_output = msg.orientation_covariance

def depth_received(msg):
  # do nothing for now; only focusing on roll, pitch, and yaw first
  pass
  
def command_received(msg):
  pass

if __name__ == "__main__":
  rospy.init_node('auto_control')

  #receive data 
  imu_sub = rospy.Subscriber('imu', Imu,
      imu_received)
  depth_sub = rospy.Subscriber('depth', Float32,
      depth_received)
  command_sub = rospy.Subscriber('/surface/auto_command',
    auto_command_msg, command_received)

  #send data
  pub = rospy.Publisher('auto_control',
    auto_control_msg, queue_size=10)


  rate = rospy.Rate(10) # 10hz
  # TODO: I2C related activities
  while not rospy.is_shutdown():
    sample_message = auto_control_msg()
    pub.publish(sample_message)
    rate.sleep()