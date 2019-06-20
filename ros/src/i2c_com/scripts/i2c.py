#! /usr/bin/python
import rospy
import time
import smbus
from BNO055 import BNO055
from TYS01 import TSYS01
from ms5837 import MS5837
from shared_msgs.msg import imu_msg, temp_msg, depth_msg
IMU_PUB_RATE = 50

def message_received(msg):
  # This runs on a seperate thread from the pub
  pass

if __name__ == "__main__":
    rospy.init_node('i2c_node')
    imu_pub = rospy.Publisher('imu_data', imu_msg, queue_size = 1)
    rate = rospy.Rate(IMU_PUB_RATE)
    temp_pub = rospy.Publisher('temp_data', temp_msg, queue_size = 1)
    depth_pub = rospy.Publisher('depth_data', depth_msg, queue_size = 1)
    try:
        imu_sens = BNO055()
        temp_sens = TSYS01()
        depth_sens = MS5837()
        temp_sens.init()
    except:
        #add mock classes to return 0 and continue and alert pilots
        pass
    while not rospy.is_shutdown():
        # using imu rate to poll the temp sensor as well beacuse IMU updates faster
        if imu_sens.update():

            # imu sensor update

            out_message = imu_msg()
            out_message.gyro = [imu_sens.pitch(), imu_sens.yaw(), imu_sens.roll()]
            out_message.accel = [imu_sens.acceleration_x(), imu_sens.acceleration_y(), imu_sens.acceleration_z()]
            imu_pub.publish(out_message)

            # read the temp in C and send it to a ros

            temp_message = temp_msg()
            temp_message.temperature = {temp_sens.temperature()}
            temp_pub.publish(temp_message)

            #depth sensor updating

           # depth_sense.update()
            #depth_message = depth_msg()
            #depth_message.depth = {depth_sense.depth()}
           # depth_pub.publish(depth_message)
        rate.sleep()
