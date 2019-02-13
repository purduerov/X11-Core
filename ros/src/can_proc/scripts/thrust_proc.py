#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg, thrust_control_msg, esc_single_msg

def message_received(msg):
  # Publish to the CAN hardware transmitter
  can_pub = rospy.Publisher('can_tx', can_msg,
      queue_size= 10)
  esc_pub = rospy.Publisher('esc_single', esc_single_msg,
      queue_size= 10) # This runs on a seperate thread from the pub
  
  # Seperate final_thrust_msg
  can_data = []
  can_data.append(msg.hfl)
  can_data.append(msg.hfr)
  can_data.append(msg.hbl)
  can_data.append(msg.hbr)
  can_data.append(msg.vfl)
  can_data.append(msg.vfr)
  can_data.append(msg.vbl)
  can_data.append(msg.vbr)

  # TODO: I2C related activities 
  for i in range(0, len(can_data)):
    msg = can_msg()
    msg.id = i
    msg.data = can_data[i]
    can_pub.publish(msg)
  
  #TODO Translate message to esc_single_msg
  sample_message = esc_single_msg()
  esc_pub.publish(sample_message)
  pass

if __name__ == "__main__":
  rospy.init_node('thrust_proc')

  # Subscribe to final_thrust and start callback function
  sub = rospy.Subscriber('final_thrust', final_thrust_msg,
      message_received)

  # Keeps from exiting until node is stopped
  rospy.spin()
