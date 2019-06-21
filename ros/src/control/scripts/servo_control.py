#!/usr/bin/python
import rospy
from std_msgs.msg import String
from shared_msgs.msg import servo_command_msg

import subprocess
import time

cur = 0
prev = 0
i = 3
v = [150, 160, 170, 180, 190, 200, 210, 220, 230]

def callback(data):
    global cur, prev, i, v
    prev = cur
    cur = data
    if(prev == 0 and cur != 0):
        if 8 >= (i + data) >= 0:
            i = i + data
            sh.stdin.write("gpio pwm 1 {}\n".format(v[i]))
            print("gpio pwm 1 {}\n".format(v[i]))

def listener():
    rospy.init_node('servo_control')
    rospy.Subscriber("/rov/servo_data", servo_command_msg, callback)
    #rospy.Timer(rospy.Duration(4), callback)

    rate = rospy.Rate(100) #100 hz

    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    sh = subprocess.Popen("/bin/bash -i".split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    sh.stdin.write("gpio mode 1 pwm\n")
    sh.stdin.write("gpio pwm-ms\n")
    sh.stdin.write("gpio pwmc 192\n")
    sh.stdin.write("gpio pwmr 2000\n")

    listener()

    sh.stdin.write("gpio mode 1 in\n")
    sh.terminate()
#power cycle after 255 changes