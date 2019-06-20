#! /usr/bin/python
import sys
import time
import subprocess


if __name__ == "__main__":
    #rospy.init_node('reset_can_node')

    #rate = rospy.Rate(0.010) # 10s
    # Performs publishing on can bus read
    #while not rospy.is_shutdown():
        #for can_rx in can_bus:
        #    rospy.loginfo("Please help")
        #    bus_message_received(can_rx)
        #rospy.loginfo("Helped")
    while True:

        subprocess.call(['sudo', 'ip', 'link', 'set', 'can0', 'down'])
        subprocess.call(['sudo', 'ip', 'link', 'set', 'can0', 'up', 'type', 'can', 'bitrate', '125000'])
        print '=========================== RESET CAN ==========================='
        time.sleep(10)
