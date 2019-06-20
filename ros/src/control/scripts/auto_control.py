#! /usr/bin/python
import rospy
from shared_msgs.msg import can_msg, auto_control_msg, auto_command_msg

#TODO: UNCOMMENT BELOW WHEN THRUST_CONTROL BRANCH MERGED WITH I2C BRANCH
#from shared_msgs.msg import imu_msg

from std_msgs.msg import Float32

setpoints = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
imu_output = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
thrust_data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

#TODO: UNCOMMENT BELOW WHEN THRUST_CONTROL BRANCH MERGED WITH I2C BRANCH
#prev_time = 0
#locked = [False, False, False, False, False, False]
#initialize PID loops for each rotation vector with values for P and I of the PID
#pid_roll = pid_file.Position_Controller(P, I, roll)
#pid_pitch = pid_file.Position_Controller(P, I, pitch)
#pid_yaw = pid_file.Position_Controller(P, I, yaw)

def imu_received(msg):
  global imu_output
  #global prev_time
  #global locked
  #global pid_roll
  #global pid_pitch
  #global pid_yaw

  #TODO: UNCOMMENT BELOW WHEN THRUST_CONTROL BRANCH MERGED WITH I2C BRANCH
  #imu_output = [msg.gyro, msg.accel]

  #TODO: send data and setpoints to pid object 
  #thrust_roll = 0.0
  #thrust_pitch = 0.0
  #thrust_yaw = 0.0
  #time = rospy.get_rostime().secs - prev_time
  #if locked[3]:
    #thrust_roll = pid_roll.calculate(setpoints[3], imu_output, rospy.get_rostime().secs)
  #if locked[4]:
    #thrust_pitch = pid_pitch.calculate(setpoints[4], imu_output, rospy.get_rostime().secs)
  #if locked[5]:
    #thrust_yaw = pid_yaw.calculate(setpoints[5], imu_output, rospy.get_rostime().secs)
  #thrust_data = [0, 0, 0, thrust_roll, thrust_pitch, thrust_yaw]
  #output_msg = auto_control_msg()
  #output_msg.thrust_vec = thrust_data
  #output_msg.dims_locked = [False, False, False, False, False, False]
  #pub.publish(output_msg)

def depth_received(msg):
  # do nothing for now; only focusing on roll, pitch, and yaw first
  pass
  
def command_received(msg):
  #global locked
  #for i in range(0, 6):
    #if msg.stabilization_dim[i] == 1:
      #locked[i] = True
    #else:
      #locked[i] = False
  sample_message = auto_control_msg()
  sample_message.thrust_vec = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
  sample_message.dims_locked = [False, False, False, False, False, False]
  pub.publish(sample_message)
    

if __name__ == "__main__":
  rospy.init_node('auto_control')

  #receive data 
  #TODO: UNCOMMENT THIS; COMMENTED BECAUSE NOT USING STANDARD IMU MSG FILE SO Imu WILL CAUSE AN ERROR
  #imu_sub = rospy.Subscriber('imu', Imu,
  #    imu_received)
  depth_sub = rospy.Subscriber('depth', Float32,
      depth_received)
  command_sub = rospy.Subscriber('/surface/auto_command',
    auto_command_msg, command_received)

  #send data
  pub = rospy.Publisher('auto_control',
    auto_control_msg, queue_size=10)

  #TODO: initialize the pid object

  rate = rospy.Rate(10) # 10hz

  while not rospy.is_shutdown():
    sample_message = auto_control_msg()
    sample_message.thrust_vec = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    sample_message.dims_locked = [False, False, False, False, False, False]
    #TODO: set sample_message to thrust_data
    pub.publish(sample_message)
    rate.sleep()