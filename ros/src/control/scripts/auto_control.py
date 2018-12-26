#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg, auto_control_msg, auto_command_msg
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32

def imu_received(msg):
  # This runs on a seperate thread from the pub
  pass

def depth_received(msg):
  # This runs on a seperate thread from the pub
  pass
def command_received(msg):
  # This runs on a seperate thread from the pub
  pass

if __name__ == "__main__":
  rospy.init_node('auto_control')

  imu_sub = rospy.Subscriber('imu', Imu,
      imu_received)

  depth_sub = rospy.Subscriber('depth', Float32,
      depth_received)

  command_sub = rospy.Subscriber('/surface/auto_command',
    auto_command_msg, command_received)

  pub = rospy.Publisher('auto_control',
    auto_control_msg, queue_size=10);


  rate = rospy.Rate(10) # 10hz
  # TODO: I2C related activities
  while not rospy.is_shutdown():
    sample_message = auto_control_msg()
    pub.publish(sample_message)
    rate.sleep()
    

