#! /usr/bin/python
import rospy
from shared_msgs.msg import auto_control_msg, final_thrust_msg, thrust_status_msg, thrust_command_msg
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32
import numpy as np
from Simple_1 import calculateSimple

desired_a = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
desired_p = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
desired_p_unramped = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
locked_dims_list = [False, False, False, False, False, False]
disabled_list = [False, False, False, False, False, False, False, False]
inverted_list = [0, 0, 0, 0, 0, 0, 0, 0]
MAX_CHANGE = .1
#watch dog stuff
last_packet_time = 0.0
is_timed_out = False
#flags to prevent old data
new_auto_data = False
new_pilot_data = False
# timout in ms
WATCHDOG_TIMEOUT = 10

def _auto_command(msg):
  global desired_a #desired thrust from automatic control
  global locked_dims_list #locked dimensions
  global new_auto_data
  print 'new_auto_data'
  desired_a = msg.thrust_vec
  locked_dims_list = msg.dims_locked
  new_auto_data = True
  on_loop()

def _pilot_command(comm):
  global desired_p #desired thrust from pilot
  global disabled_list #disabled thrusters
  global inverted_list #inverted thrusters
  global new_pilot_data
  global desired_p_unramped
  print 'new_pilot_data'
  desired_p_unramped = comm.desired_thrust
  for i in range(0,6):
      ramp(i)
  disabled_list = comm.disable_thrusters
  inverted_list = comm.inverted
  new_pilot_data = True
  on_loop()


def ramp(index):
    if (abs(desired_p_unramped[index] - desired_p[index]) > MAX_CHANGE):
        if (desired_p_unramped[index] - desired_p[index] > 0):
            desired_p[index] += MAX_CHANGE
        else:
            desired_p[index] -= MAX_CHANGE
        return
    else:
        desired_p[index] = desired_p_unramped[index]
        
def on_loop():
    global new_pilot_data
    global new_auto_data
    global is_timed_out
    global last_packet_time

    #check to see if you have new data
    if(not (new_pilot_data and new_auto_data) and not is_timed_out):
        return
    #reset flags and execute
    if new_pilot_data and new_auto_data:
        is_timed_out = False
    print "on_loop p=" + str(new_pilot_data) + " a=" + str(new_auto_data) + " t=" + str(is_timed_out)
    new_auto_data = False
    new_pilot_data = False
    if(not is_timed_out):
        #reset the watchdog timer
        curr_time = rospy.get_rostime()
        last_packet_time = curr_time.secs + curr_time.nsecs * 10 ** -9

    for i in range(6):
      if(is_timed_out):
          desired_thrust_final[i] = 0.0
      else:
          #if dimension locked, set desired thrust to auto; else set to pilot controls
          if locked_dims_list[i] == True:
            desired_thrust_final[i] = desired_a[i]
          else:
            desired_thrust_final[i] = desired_p[i]

    #calculate thrust
    pwm_values = calculateSimple(desired_thrust_final)
    #invert relevant values
    for i in range(8):
      if inverted_list[i] == 1:
        pwm_values[i] = pwm_values[i] * (-1)

    #assign values to publisher messages for thurst control and status
    tcm = final_thrust_msg()
    # val = float of range(-1, 1)
    # if int8: (val * 127.5) - 0.5 will give range -128 to 127
    # if uint8: (val + 1) * 127.5 will give 0 to 255
    tcm.hfl = int((pwm_values[0] + 1) * 127.5)
    tcm.hfr = int((pwm_values[1] + 1) * 127.5)
    tcm.hbr = int((pwm_values[2] + 1) * 127.5)
    tcm.hbl = int((pwm_values[3] + 1) * 127.5)
    tcm.vfl = int((pwm_values[4] + 1) * 127.5)
    tcm.vfr = int((pwm_values[5] + 1) * 127.5)
    tcm.vbr = int((pwm_values[6] + 1) * 127.5)
    tcm.vbl = int((pwm_values[7] + 1) * 127.5)

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
  thrust_pub = rospy.Publisher('final_thrust',
      final_thrust_msg, queue_size=10)
  status_pub = rospy.Publisher('thrust_status',
      thrust_status_msg, queue_size=10)

  #define variable for class Complex to allow calculation of thruster pwm values
  # c = Complex_1.Complex()
  desired_thrust_final = [0, 0, 0, 0, 0, 0]

  while not rospy.is_shutdown():
    compare_time = rospy.get_rostime()
    compare_time = compare_time.secs + compare_time.nsecs * 10 ** -9
    print str(compare_time) + " : "  + str(last_packet_time)
    if(compare_time - last_packet_time > WATCHDOG_TIMEOUT):
        is_timed_out = True
    if(is_timed_out):
        #global disabled_list
        #disabled_list = [True, True, True, True, True, True, True, True]
        on_loop()
        curr_time = rospy.get_rostime()
        last_packet_time = curr_time.secs + curr_time.nsecs * 10 ** -9
        is_timed_out = False

    rate.sleep()
