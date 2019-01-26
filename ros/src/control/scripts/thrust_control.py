#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg, auto_control_msg, thrust_control_msg, thrust_status_msg, thrust_command_msg
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32
from rov import movement/mapper/Complex

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
    thrust_control_msg, queue_size=10)

  status_pub = rospy.Publisher('thrust_status',
    thrust_status_msg, queue_size=10)

  rate = rospy.Rate(10) # 10hz

  #define variable for class Complex to allow calculation of thruster pwm values
  c = Complex()

  #TODO: decide to use automatic or pilot control using dims_locked

  #TODO: read desired thrust and disabled thrusters and inverted thrusters

  #calculate thrust
  thrust_values = c.calculate(desired, disabled, False)

  #TODO: redo this with tcm = thrust_control_msg() and tcm.hfl ...
  thrust_control_msg.hfl = thrust_values[0]
  thrust_control_msg.hfr = thrust_values[1]
  thrust_control_msg.hbl = thrust_values[2]
  thrust_control_msg.hbr = thrust_values[3]
  thrust_control_msg.vfl = thrust_values[4]
  thrust_control_msg.vfr = thrust_values[5]
  thrust_control_msg.vbl = thrust_values[6]
  thrust_control_msg.vbr = thrust_values[7]

  #TODO: invert thrust values

  # TODO: I2C related activities
  while not rospy.is_shutdown():
    #TODO: change thrust_control_msg() to tcm?
    thrust_pub.publish(thrust_control_msg())
    status_pub.publish(thrust_status_msg())
    rate.sleep()
    

