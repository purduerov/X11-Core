#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg, auto_command_msg, thrust_status_msg, thrust_command_msg, esc_single_msg
from sensor_msgs.msg import Imu, Temperature
from std_msgs.msg import Float32

from inputs import get_gamepad, devices, iter_unpack
import os

def thrust_status_received(msg):
  pass # This runs on a seperate thread
def esc_single_received(msg):
  pass # This runs on a seperate thread

def temp_received(msg):
  pass # This runs on a seperate thread
def imu_received(msg):
  pass # This runs on a seperate thread
def ph_received(msg):
  pass # This runs on a seperate thread
def depth_received(msg):
  pass # This runs on a seperate thread

if __name__ == "__main__":

    rospy.init_node('driver_mocker')
    ns = rospy.get_namespace() # This should return /surface
    

    # Retrieve data from the ROS System
    esc_sub = rospy.Subscriber('/rov/esc_single', 
        esc_single_msg, esc_single_received)

    status_sub = rospy.Subscriber('/rov/thrust_status',thrust_status_msg,
        thrust_status_received)

    temp_sub = rospy.Subscriber('/rov/temp', Temperature,
        temp_received)

    imu_sub = rospy.Subscriber('/rov/imu', Imu,
        imu_received)

    ph_sub = rospy.Subscriber('/rov/ph',Float32,
        ph_received)

    depth_sub = rospy.Subscriber('/rov/depth', Float32,
        depth_received)

    # Publishers out onto the ROS System
    thrust_pub = rospy.Publisher(ns + 'thrust_mock',
        thrust_command_msg, queue_size=10)

    auto_pub= rospy.Publisher(ns +'auto_command',
        auto_command_msg, queue_size=10)
    
    out = thrust_command_msg()
    
    keys = {
            'BTN_TR': {"indx": 3, "weight": .5, "scale": 1.0},
            'BTN_TL': {"indx": 3, "weight": -.5, "scale": 1.0},
            'ABS_RY': {"indx": 4, "weight": .5, "scale": 32768.0},
            'ABS_RX': {"indx": 5, "weight": .5, "scale": 32768.0},
            'ABS_RZ': {"indx": 2, "weight": .5, "scale": 1024.0},
            'ABS_X': {"indx": 0, "weight": .5, "scale": 32768.0},
            'ABS_Y': {"indx": 1, "weight": .5, "scale": 32768.0},
            'ABS_Z': {"indx": 2, "weight": -.5, "scale": 1024.0}
    }

    rate = rospy.Rate(10) # 10hz

    # TODO: I2C related activities
    while not rospy.is_shutdown():
        ## I tried to make this dynamic and read only if there was information
        ## present, but through the nature of the underlying C(?) code it was
        ## not possible
        # catch up on events since last run, update the desired thrust values
        gamepad = get_gamepad()
        for event in gamepad:
            press = event.code

            if press in keys:
                alt = keys[press]

                val = event.state / alt["scale"]
                if press == "BTN_TR":
                    print(val)
                    if not event.state and out.desired_thrust[alt["indx"]] < 0:
                        val = out.desired_thrust[alt["indx"]]
                elif press == "BTN_TL":
                    print(val)
                    if not event.state and out.desired_thrust[alt["indx"]] > 0:
                        val = out.desired_thrust[alt["indx"]]
                
                if abs(val) < 0.1:
                    val = 0

                out.desired_thrust[alt["indx"]] = alt["weight"] * val

        print(out.desired_thrust)

        thrust_pub.publish(out)
        auto_pub.publish(auto_command_msg())
        rate.sleep()
