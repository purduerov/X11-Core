#! /usr/bin/python
import sys
import can
import rospy
from shared_msgs.msg import can_msg

from collections import deque

# can_bus - This is a ROS node that handles all CAN hardware communication
#           Arguments: can_bus.py accepts one optional argument: the CAN interface name. Usually can0 or vcan0.
#
#           can_bus reads on the can_tx topic and writes contents to pi CAN line (or vcan)
#           can_bus reads the pi CAN line (or vcan) and writes contents to can_rx topic.

global can_bus
global can_queue
global pub
global sub

can_queue = deque() # slightly more efficient than list append/pop

# Subscriber: Called when topic message is received
def topic_message_received(msg):
    # This runs on a seperate thread from the pub
    global can_queue
    data_list = list()
    shift = 64
    for i in range(0,8):
        shift -= 8
        data_list.append((msg.data >> shift) % 256)
    data = bytearray(data_list)
    #rospy.loginfo('Topic Message Received: ' + str(msg.id) + ':' + str(list(data)))
    can_tx = can.Message(arbitration_id=msg.id, data=data, extended_id=False)
    
    can_queue.append(can_tx) # append to right/end of queue
    rospy.loginfo("Queue grew, to {} items long".format(len(can_queue)))

# Publisher: Called when can bus message is received
def bus_message_received(can_rx):
    global can_bus
    global pub
    data_list = list(can_rx.data)
    data = 0l
    shift = len(data_list) * 8
    for i in data_list:
        shift -= 8
        data = data + (i << shift)
    rospy.loginfo('Can Message Received: ' + str(can_rx.arbitration_id) + ':' + str(list(can_rx.data)))
    can_rx = can_msg(can_rx.arbitration_id, data)
    pub.publish(can_rx)

if __name__ == "__main__":
    global can_bus
    rospy.init_node('can_node')

    channel = 'can0'
    if len(sys.argv) == 2:
        channel = sys.argv[1]
    can_bus = can.interface.Bus(channel=channel, bustype='socketcan')

    pub = rospy.Publisher('can_rx', can_msg,
            queue_size= 100)
    sub = rospy.Subscriber('can_tx', can_msg,
            topic_message_received)

    rospy.loginfo('Started \'can_node\' on channel: ' + channel)


    rate = rospy.Rate(40) # 40hz
    # Performs publishing on can bus read
    while not rospy.is_shutdown():
        for can_rx in can_bus:
            rospy.loginfo("Please help")
            bus_message_received(can_rx)
        rospy.loginfo("Helped")
        
        try: # pop from left/beginning of queue
            rospy.loginfo("Can queue members: {}".format(len(can_queue)))
            if len(can_queue):
                out = can_queue.popleft()
                rospy.loginfo(out)
                can_bus.send(out, timeout=0.00001)
        except can.CanError as cerr:
            rospy.loginfo("There was a CAN sending error")
            pass

        rate.sleep()
