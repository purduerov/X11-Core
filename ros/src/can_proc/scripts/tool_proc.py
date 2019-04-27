#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg, tools_command_msg


TOOLS_BOARD_ID = 0x204

MANIPULATOR_OPEN_BIT = 0b1
MANIPULATOR_CLOSE_BIT = 0b1000000
GROUT_TROUT_OPEN_BIT = 0b10000
GROUT_TROUT_CLOSE_BIT = 0b10
LIFT_BAG_OPEN_BIT = 0b100
LIFT_BAG_CLOSE_BIT = 0b100000
MARKER_OPEN_BIT = 0b10000000
MARKER_CLOSE_BIT = 0b1000

cmsg = can_msg()
cmsg.id = TOOLS_BOARD_ID

# Scott switched hoses, since only PM wasn't working
"""
MANIPULATOR_OPEN_BIT = 0b100
MANIPULATOR_CLOSE_BIT = 0b100000
LIFT_BAG_OPEN_BIT = 0b1
LIFT_BAG_CLOSE_BIT = 0b1000000
"""

pub = None
sub = None

def message_received(msg):
    global cmsg
    data_list = [0] * 8

    data_list[-1] = data_list[-1] | (msg.manipulator * MANIPULATOR_OPEN_BIT)
    data_list[-1] = data_list[-1] | ((not msg.manipulator) * MANIPULATOR_CLOSE_BIT)
    data_list[-1] = data_list[-1] | (msg.groutTrout * GROUT_TROUT_OPEN_BIT)
    data_list[-1] = data_list[-1] | ((not msg.groutTrout) * GROUT_TROUT_CLOSE_BIT)
    data_list[-1] = data_list[-1] | (msg.liftBag * LIFT_BAG_OPEN_BIT)
    data_list[-1] = data_list[-1] | ((not msg.liftBag) * LIFT_BAG_CLOSE_BIT)
    data_list[-1] = data_list[-1] | (msg.marker * MARKER_OPEN_BIT)
    data_list[-1] = data_list[-1] | ((not msg.marker) * MARKER_CLOSE_BIT)
    data = bytearray(data_list)

    print data_list

    cmsg.data = data_list[-1]
      
    return cmsg

if __name__ == "__main__":
  rospy.init_node('tool_proc', anonymous=True)
  
  # Publish to the CAN hardware transmitter
  pub = rospy.Publisher('can_tx', can_msg,
      queue_size= 100)

  sub = rospy.Subscriber('/surface/tools_command', tools_command_msg,
      message_received)

  rate = rospy.Rate(20) # 20hz

  while not rospy.is_shutdown():
      pub.publish(cmsg)
      rate.sleep()
      #rospy.spin()
    

