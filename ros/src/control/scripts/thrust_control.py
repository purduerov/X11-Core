#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg, auto_control_msg, thrust_control_msg, thrust_status_msg, thrust_command_msg
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32
from rov import movement/mapper/Complex

desired_a = None
desired_p = None
locked_dims_list = None
disabled_list = None
inverted_list = None
auto_ctrl_flag = None

def message_received(msg):
  global desired_a #desired thrust from automatic control
  global locked_dims_list #locked dimensions
  desired_a = msg.thrust_vec
  locked_dims_list = msg.dims_locked

  #initialize flag for automatic control vs pilot control
  auto_ctrl_flag = 0
  #if there are locked dimensions, set flag to use automatic control
  for i in range(0, len(locked_dims_list)):
    if locked_dims_list[i] == True:
      auto_ctrl_flag = 1

def command_received(comm):
  global desired_p #desired thrust from pilot
  global disabled_list #disabled thrusters
  global inverted_list #inverted thrusters
  desired_p = comm.desired_thrust
  disabled_list = comm.disable_thrusters
  inverted_list = comm.inverted

if __name__ == "__main__":
  
  #initialize node and rate
  rospy.init_node('thrust_control')
  rate = rospy.Rate(10) #10 hz

  #initialize subscribers
  auto_sub = rospy.Subscriber('auto_control', 
      auto_control_msg, message_received)
  comm_sub = rospy.Subscriber('/surface/thrust_command',
      thrust_command_msg, command_received)
  
  #initialize publishers
  thrust_pub = rospy.Publisher('thrust_control',
    thrust_control_msg, queue_size=10)
  status_pub = rospy.Publisher('thrust_status',
    thrust_status_msg, queue_size=10)

  #initialize auto_ctrl_flag
  global auto_ctrl_flag
  auto_ctrl_flag = 0

  while not rospy.is_shutdown():

    #set desired thrust to either automatic or pilot control
    if auto_ctrl_flag == 1:
      desired_thrust_final = desired_a
    else:
      desired_thrust_final = desired_p

    #define variable for class Complex to allow calculation of thruster pwm values
    c = Complex()
    #calculate thrust
    output_values = c.calculate(desired_thrust_final, disabled_list, False)
    pwm_values = output_values
    #invert relevant values
    for i in range(0, len(output_values)):
      if inverted_list[i] == 1:
        pwm_values[i] = pwm_values[i] * (-1)

    #assign values to publisher messages for thurst control and status
    tcm = thrust_control_msg()
    tcm.hfl = pwm_values[0]
    tcm.hfr = pwm_values[1]
    tcm.hbl = pwm_values[2]
    tcm.hbr = pwm_values[3]
    tcm.vfl = pwm_values[4]
    tcm.vfr = pwm_values[5]
    tcm.vbl = pwm_values[6]
    tcm.vbr = pwm_values[7]

    tsm = thrust_status_msg()
    tsm.status = pwm_values

    #reset automatic control flag
    auto_ctrl_flag = 0

    #publish data
    thrust_pub.publish(tcm)
    status_pub.publish(tsm)
    rate.sleep()
