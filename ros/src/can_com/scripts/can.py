#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg
import can

global can_bus
global pub
global sub

def topic_message_received(msg):
    # This runs on a seperate thread from the pub
    global can_bus
    rospy.loginfo('Topic Message Received: ' + msg.id + ':' + msg.data)
    can_tx = can.Message(arbitration_id=msg.id, data=msg.data, extended_id=False)
    can_bus.send(can_msg2)

def bus_message_received(can_rx):
    global can_bus
    global pub
    rospy.loginfo('Can Message Received: ' + can_rx.id + ':' + can_rx.data)
    can_rx = can_msg(can_rx.id, can_rx.data)
    pub.publish(can_rx)

if __name__ == "__main__":
    rospy.init_node('can_node')

    can_bus = can.ThreadSafeBus()
    pub = rospy.Publisher('can_rx', can_msg,
            queue_size= 100)
    sub = rospy.Subscriber('can_tx', can_msg,
            topic_message_received)

    while True:
        for can_rx in can_bus:
            bus_message_received(can_rx)
        rospy.loginfo('Done')

    rospy.spin()
