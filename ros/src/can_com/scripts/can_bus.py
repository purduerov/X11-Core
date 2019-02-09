#! /usr/bin/python
import can
import rospy
from shared_msgs.msg import msg_can

global can_bus
global pub
global sub

# Subscriber: Called when topic message is received
def topic_message_received(msg):
    # This runs on a seperate thread from the pub
    global can_bus
    data_list = list()
    shift = 64
    for i in range(0,8):
        shift -= 8
        data_list.append((msg.data >> shift) % 256)
    data = bytearray(data_list)
    rospy.loginfo('Topic Message Received: ' + str(msg.id) + ':' + str(list(data)))
    can_tx = can.Message(arbitration_id=msg.id, data=data, extended_id=False)
    can_bus.send(can_tx)

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
    can_rx = msg_can(can_rx.arbitration_id, data)
    pub.publish(can_rx)

if __name__ == "__main__":
    global can_bus
    rospy.init_node('can_node')

    can_bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
    pub = rospy.Publisher('can_rx', msg_can,
            queue_size= 100)
    sub = rospy.Subscriber('can_tx', msg_can,
            topic_message_received)

    # Performs publishing on can bus read
    while True:
        for can_rx in can_bus:
            bus_message_received(can_rx)
        rospy.loginfo('Done')
