#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg, final_thrust_msg

#TODO Get the ID and position of the thrusters
# Currently testing values are put in such that there are two boards each with four thrusters
global can_pub
can_ids = [0x201, 0x201, 0x203, 0x202, 0x202, 0x203, 0x203, 0x202] # can IDs
can_pos = [5, 6, 7, 0, 3, 4, 5, 2] # positions in data packet

can_pow = [] # power of thrusters

def message_received(msg):
  global can_pub
  global can_ids
  global can_pos
  global can_pow

  rospy.loginfo('message received')

  # Seperate final_thrust_msg
  del can_pow[:]
  can_pow.append(msg.hfl)
  can_pow.append(msg.hfr)
  can_pow.append(msg.hbr)
  can_pow.append(msg.hbl)
  can_pow.append(msg.vfl)
  can_pow.append(msg.vfr)
  can_pow.append(msg.vbr)
  can_pow.append(msg.vbl)


  base_board = min(can_ids)
  max_board = max(can_ids)

  for cid in range(base_board, max_board + 1):
    data_list = [0] * 8
    for i in range(8):
      if can_ids[i] == cid:
        data_list[can_pos[i]] = can_pow[i]
    #print str(cid) + ' : ' + str(data_list)
    data = bytearray(data_list)

    # Publish Message
    new_msg = can_msg()
    new_msg.id = cid
    new_msg.data = data
    can_pub.publish(new_msg)

  #TODO Translate message to esc_single_msg
  #sample_message = esc_single_msg()
  #esc_pub.publish(sample_message)
  pass

if __name__ == "__main__":
  rospy.init_node('thrust_proc')

  # Publishers to the CAN hardware transmitter
  can_pub = rospy.Publisher('can_tx', can_msg,
      queue_size = 10)
  #esc_pub = rospy.Publisher('esc_single', esc_single_msg,
  #    queue_size = 10)


  # Subscribe to final_thrust and start callback function
  sub = rospy.Subscriber('final_thrust', final_thrust_msg,
      message_received)

  rospy.loginfo('thrust_proc started')

  # Keeps from exiting until node is stopped
  while not rospy.is_shutdown():
    rospy.spin()
