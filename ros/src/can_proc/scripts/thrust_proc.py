#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg, thrust_control_msg, esc_single_msg

can_data = []

def message_received(msg):
  # This runs on a seperate thread from the pub
  can_data[0] = msg.hfl
  can_data[1] = msg.hfr
  can_data[2] = msg.hbl
  can_data[3] = msg.hbr
  can_data[4] = msg.vfl
  can_data[5] = msg.vfr
  can_data[6] = msg.vbl
  can_data[7] = msg.vbr
  pass

if __name__ == "__main__":
  rospy.init_node('thrust_proc')
  
  # Publish to the CAN hardware transmitter
  can_pub = rospy.Publisher('can_tx', can_msg,
      queue_size= 10)
  esc_pub = rospy.Publisher('esc_single', esc_single_msg,
      queue_size= 10)

  sub = rospy.Subscriber('final_thrust', final_thrust_msg,
      message_received)

  rate = rospy.Rate(10) # 10hz
  # TODO: I2C related activities
  while not rospy.is_shutdown():
    for i in range(0, len(can_data)):
      msg = can_msg()
      msg.id = i
      msg.data = can_data[i]
      can_pub.publish(msg)
    sample_message = esc_single_msg()
    esc_pub.publish(sample_message)
    rate.sleep()
