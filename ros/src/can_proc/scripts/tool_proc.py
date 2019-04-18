#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg

TOOLS_BOARD_ID = 0x204

MANIPULATOR_BIT = 0b0
GROUT_TROUT_BIT = 0b0
LIFT_BAG_BIT = 0b0
MARKER_BIT = 0b0

pub = None
sub = None

def message_received(msg):
  data_list = [0] * 8

  data_list[-1] = data_list[-1] | (msg.manipulator * MANIPULATOR_BIT)
  data_list[-1] = data_list[-1] | (msg.groutTrout * GROUT_TROUT_BIT)
  data_list[-1] = data_list[-1] | (msg.liftBag * LIFT_BAG_BIT)
  data_list[-1] = data_list[-1] | (msg.marker * MARKER_BIT)
  data = bytearray(data_list)

  cmsg = can_msg()
  cmsg.id = TOOLS_BOARD_ID
  cmsg.data = data
  pub.publish(cmsg)
    
  pass

if __name__ == "__main__":
  rospy.init_node('tool_proc', anonymous=True)
  
  # Publish to the CAN hardware transmitter
  pub = rospy.Publisher('can_tx', can_msg,
      queue_size= 100)

  sub = rospy.Subscriber('tool_control', can_msg,
      message_received)

  while not rospy.is_shutdown():
      rospy.spin()
    

