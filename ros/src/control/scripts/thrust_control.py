#! /usr/bin/python
import rospy
from shared_msgs.msg import auto_control_msg, thrust_control_msg, thrust_status_msg, thrust_command_msg
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32
import numpy as np
import Complex_1

desired_a = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
desired_p = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
locked_dims_list = [False, False, False, False, False, False]
disabled_list = [False, False, False, False, False, False, False, False]
inverted_list = [0, 0, 0, 0, 0, 0, 0, 0]

def _auto_command(msg):
  global desired_a #desired thrust from automatic control
  global locked_dims_list #locked dimensions
  desired_a = msg.thrust_vec
  locked_dims_list = msg.dims_locked

def _pilot_command(comm):
  global desired_p #desired thrust from pilot
  global disabled_list #disabled thrusters
  global inverted_list #inverted thrusters
  desired_p = comm.desired_thrust
  disabled_list = comm.disable_thrusters
  inverted_list = comm.inverted

if __name__ == "__main__":
  '''
  Note that this file is only set up for using 8 thrusters. 
  ''' 

  #initialize node and rate
  rospy.init_node('thrust_control')
  rate = rospy.Rate(10) #10 hz

  #initialize subscribers
  auto_sub = rospy.Subscriber('auto_control', 
      auto_control_msg, _auto_command)
  comm_sub = rospy.Subscriber('/surface/thrust_command',
      thrust_command_msg, _pilot_command)
  
  #initialize publishers
  thrust_pub = rospy.Publisher('thrust_control',
    thrust_control_msg, queue_size=10)
  status_pub = rospy.Publisher('thrust_status',
    thrust_status_msg, queue_size=10)

  #define variable for class Complex to allow calculation of thruster pwm values
  c = Complex_1.Complex()
  desired_thrust_final = [0, 0, 0, 0, 0, 0]

  while not rospy.is_shutdown():
    
    for i in range(6):
      #if dimension locked, set desired thrust to auto; else set to pilot controls
      if locked_dims_list[i] == True:
        desired_thrust_final[i] = desired_a[i]
      else:
        desired_thrust_final[i] = desired_p[i]

    #calculate thrust
    pwm_values = c.calculate(desired_thrust_final, disabled_list, False)
    ui8_values = np.uint8(np.asarray(pwm_values, dtype=np.float32) * 255)
    #invert relevant values
    for i in range(8):
      if inverted_list[i] == 1:
        pwm_values[i] = pwm_values[i] * (-1)

    #assign values to publisher messages for thurst control and status
    tcm = thrust_control_msg()
    tcm.hfl = ui8_values[0]
    tcm.hfr = ui8_values[1]
    tcm.hbl = ui8_values[2]
    tcm.hbr = ui8_values[3]
    tcm.vfl = ui8_values[4]
    tcm.vfr = ui8_values[5]
    tcm.vbl = ui8_values[6]
    tcm.vbr = ui8_values[7]

    tsm = thrust_status_msg()
    tsm.status = pwm_values

    #publish data
    thrust_pub.publish(tcm)
    status_pub.publish(tsm)
    rate.sleep()
