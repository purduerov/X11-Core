#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg, final_thrust_msg

# Publishers to the CAN hardware transmitter
can_pub = rospy.Publisher('can_tx', can_msg,
    queue_size = 10)
#esc_pub = rospy.Publisher('esc_single', esc_single_msg,
#    queue_size = 10)

#TODO Get the ID and position of the thrusters
# Currently testing values are put in such that there are two boards each with four thrusters
can_ids = [0, 0, 0, 0, 1, 1, 1, 1] # can IDs
can_pos = [0, 1, 2, 3, 0, 1, 2, 3] # positions in data packet

can_pow = [] # power of thrusters

def message_received(msg):
  global can_pub
  global can_ids
  global can_pos
  global can_pow

  # Seperate final_thrust_msg
  can_pow.append(msg.hfl)
  can_pow.append(msg.hfr)
  can_pow.append(msg.hbl)
  can_pow.append(msg.hbr)
  can_pow.append(msg.vfl)
  can_pow.append(msg.vfr)
  can_pow.append(msg.vbl)
  can_pow.append(msg.vbr)

  # Place thrusters into boards
  boards = list(set(can_ids))
  for curr_id in boards:
    # Get indices of thrusters with ID, boards[i]
    indices = [i for i, x in enumerate(can_ids) if x == curr_id]

    # Make list of the thruster's positions
    curr_pos = []
    for i in indices:
        curr_pos.append(can_pos[i])

    # Sort indices of thrusters based on position
    zipped_pairs = zip(curr_pos, indices)
    sortedIndices = [a for _, a in sorted(zipped_pairs)]

    # Make list of the thruster's power in order of position
    curr_pow = []
    for i in sortedIndices:
        curr_pow.append(can_pow[i])
    
    # Make 64 bit data message
    curr_data = 0
    for x in curr_pow:
        curr_data = curr_data << 8
        curr_data = curr_data | x
    for x in range(8 - len(curr_pow)):
        curr_data = curr_data << 8

    # Publish Message
    new_msg = can_msg()
    new_msg.id = curr_id
    new_msg.data = curr_data
    can_pub.publish(msg)
 
  #TODO Translate message to esc_single_msg
  #sample_message = esc_single_msg()
  #esc_pub.publish(sample_message)
  pass

if __name__ == "__main__":
  rospy.init_node('thrust_proc')

  # Subscribe to final_thrust and start callback function
  sub = rospy.Subscriber('final_thrust', final_thrust_msg,
      message_received)

  # Keeps from exiting until node is stopped
  rospy.spin()
