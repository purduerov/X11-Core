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

#watch dog stuff
last_packet_time = 0.0
is_timed_out = False
#flags to prevent old data
new_auto_data = False
new_pilot_data = False
# timout in ms
WATCHDOG_TIMEOUT = 100

def _auto_command(msg):
  global desired_a #desired thrust from automatic control
  global locked_dims_list #locked dimensions
  desired_a = msg.thrust_vec
  locked_dims_list = msg.dims_locked
  new_auto_data = True
  on_loop()

def _pilot_command(comm):
  global desired_p #desired thrust from pilot
  global disabled_list #disabled thrusters
  global inverted_list #inverted thrusters
  desired_p = comm.desired_thrust
  disabled_list = comm.disable_thrusters
  inverted_list = comm.inverted
  curr_time = rospy.get_rostime()
  on_loop()

def on_loop():
    #check to see if you have new data
    if(!(new_pilot_data && new_auto_data)):
        return
    #reset flags and execute
    new_auto_data = False
    new_pilot_data = False
    #reset the watchdog timer
    curr_time = rospy.get_rostime()
    last_packet_time = curr_time.secs + curr_time.secs * 10 ** -9;
    for i in range(6):
      #if dimension locked, set desired thrust to auto; else set to pilot controls
      if locked_dims_list[i] == True:
        desired_thrust_final[i] = desired_a[i]
      else:
        desired_thrust_final[i] = desired_p[i]

    #calculate thrust
    pwm_values = c.calculate(desired_thrust_final, disabled_list, False)
    #invert relevant values
    for i in range(8):
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

    #publish data
    thrust_pub.publish(tcm)
    status_pub.publish(tsm)

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
    if(is_timed_out):
        global disabled_list
        disabled_list = [True, True, True, True, True, True, True, True]
        on_loop()
    #ask about syntax

    if(compare_time - last_packet_time > WATCHDOG_TIMEOUT):
        is_timed_out = True
    rate.sleep()
