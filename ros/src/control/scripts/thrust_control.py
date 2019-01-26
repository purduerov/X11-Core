#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg, auto_control_msg, thrust_control_msg, thrust_status_msg, thrust_command_msg
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32

def message_received(msg):
  # This runs on a seperate thread from the pub
  pass
def command_received(comm):
  # This runs on a seperate thread from the pub
  pass

if __name__ == "__main__":
  rospy.init_node('thrust_control')

  auto_sub = rospy.Subscriber('auto_control', 
      auto_control_msg, message_received)
  comm_sub = rospy.Subscriber('/surface/thrust_command',
      thrust_command_msg, command_received)

  thrust_pub = rospy.Publisher('thrust_control',
    thrust_control_msg, queue_size=10);

  status_pub = rospy.Publisher('thrust_status',
    thrust_status_msg, queue_size=10);

  rate = rospy.Rate(10) # 10hz
  # TODO: I2C related activities
  while not rospy.is_shutdown():
    thrust_pub.publish(thrust_control_msg())
    status_pub.publish(thrust_status_msg())
    rate.sleep()
    

