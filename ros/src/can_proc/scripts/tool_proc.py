#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg, tools_command_msg


TOOLS_BOARD_ID = 0x204

MANIPULATOR_OPEN_BIT =    0x04
MANIPULATOR_CLOSE_BIT =   0x40
MARKER_OPEN_BIT =         0x80
MARKER_CLOSE_BIT =        0x08
GROUT_TROUT_OPEN_BIT =    0x10
GROUT_TROUT_CLOSE_BIT =   0x01
LIFT_BAG_OPEN_BIT =       0x02
LIFT_BAG_CLOSE_BIT =      0x20

cmsg = can_msg()
cmsg_pm = can_msg()
cmsg_gt = can_msg()
cmsg_lb = can_msg()
cmsg_mk = can_msg()

cmsg_pm.id = TOOLS_BOARD_ID
cmsg_gt.id = TOOLS_BOARD_ID
cmsg_lb.id = TOOLS_BOARD_ID
cmsg_mk.id = TOOLS_BOARD_ID

changed = False
pseudo_lock = False

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
    global cmsg_pm, cmsg_gt, cmsg_lb, cmsg_mk
    # data_list = [0] * 8

    pm = (msg.manipulator * MANIPULATOR_OPEN_BIT) | ((not msg.manipulator) * MANIPULATOR_CLOSE_BIT)
    gt = (msg.groutTrout * GROUT_TROUT_OPEN_BIT) | ((not msg.groutTrout) * GROUT_TROUT_CLOSE_BIT)
    lb = (msg.liftBag * LIFT_BAG_OPEN_BIT) | ((not msg.liftBag) * LIFT_BAG_CLOSE_BIT)
    mk = (msg.marker * MARKER_OPEN_BIT) | ((not msg.marker) * MARKER_CLOSE_BIT)

    # If we're doing this, we're getting rid of the rate
    # Pilots likely have a hard time beating 5 to 10 Hz...
    # We'll deal with spamming later
    if cmsg_pm.data != pm:
        cmsg_pm.data = pm
        pub.publish(cmsg_pm)
    
    if cmsg_gt.data != gt:
        cmsg_gt.data = gt
        pub.publish(cmsg_gt)
    
    if cmsg_lb.data != lb:
        cmsg_lb.data = lb
        pub.publish(cmsg_lb)
    
    if cmsg_mk.data != mk:
        cmsg_mk.data = mk
        pub.publish(cmsg_mk)

    #data_list[-1] = data_list[-1] | (msg.manipulator * MANIPULATOR_OPEN_BIT)
    #data_list[-1] = data_list[-1] | ((not msg.manipulator) * MANIPULATOR_CLOSE_BIT)
    #data_list[-1] = data_list[-1] | (msg.groutTrout * GROUT_TROUT_OPEN_BIT)
    #data_list[-1] = data_list[-1] | ((not msg.groutTrout) * GROUT_TROUT_CLOSE_BIT)
    #data_list[-1] = data_list[-1] | (msg.liftBag * LIFT_BAG_OPEN_BIT)
    #data_list[-1] = data_list[-1] | ((not msg.liftBag) * LIFT_BAG_CLOSE_BIT)
    #data_list[-1] = data_list[-1] | (msg.marker * MARKER_OPEN_BIT)
    #data_list[-1] = data_list[-1] | ((not msg.marker) * MARKER_CLOSE_BIT)
    # data = bytearray(data_list)

    #print data_list

    #cmsg.data = data_list[-1]
      

if __name__ == "__main__":
  rospy.init_node('tool_proc', anonymous=True)
  
  # Publish to the CAN hardware transmitter
  pub = rospy.Publisher('can_tx', can_msg,
      queue_size= 100)

  sub = rospy.Subscriber('/surface/tools_command', tools_command_msg,
      message_received)

  #rate = rospy.Rate(5) # 5hz

  while not rospy.is_shutdown():
      #rate.sleep()
      rospy.spin()
    

