#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg, final_thrust_msg

VALUE_DIFF = 1

# Currently testing values are put in such that there are two boards each with four thrusters
global can_pub
can_ids = [0x201, 0x201, 0x203, 0x202, 0x202, 0x203, 0x203, 0x202] # can IDs
can_pos = [    5,     6,     7,     5,     6,     4,     5,     7] # positions in data packet

can_better_map = {
        0x201: [None, 0, 1, None],
        0x202: [None, 3, 4, 7],
        0x203: [5, 6, None, 2]
        }

can_pow = [] # power of thrusters
can_last = {
        0x201: None,
        0x202: None,
        0x203: None
        }

def message_received(msg):
  global can_pub
  global can_ids
  global can_pos
  global can_pow
  global can_last
  global can_better_map

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
    data_list = 0
    cur = can_better_map[cid]

    for el in cur:
        if el is not None:
            data_list += can_pow[el]
        else:
            data_list += 127

        data_list = data_list << 8
    data_list = data_list >> 8
    
    """
    print("|{}|".format(cid))
    for i in range(8):
        print("{}".format((data_list >> 8*i) & 0xff))
    print("----")
    """

    # Publish Message
    new_msg = can_msg()
    new_msg.id = cid
    new_msg.data = data_list

    if checkChange(new_msg):
        can_pub.publish(new_msg)
    

  #TODO Translate message to esc_single_msg
  #sample_message = esc_single_msg()
  #esc_pub.publish(sample_message)
  pass

def checkChange(new_msg):
    global can_last

    print("{}:".format(new_msg.id))
    if can_last[new_msg.id] is None:
        print("New message, true")
        can_last[new_msg.id] = new_msg
        return True

    else:
        test = new_msg.data
        comp = can_last[new_msg.id].data
        for i in range(4):
            a = abs( ((test >> 8*i) & 0xff) - ((comp >> 8*i) & 0xff) )
           
            if a > VALUE_DIFF:
                can_last[new_msg.id] = new_msg
                print("  changed")
                return True

        print("  not changed")
        return False

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
