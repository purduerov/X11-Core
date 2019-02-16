#! /usr/bin/python
import rospy
import json
import packet_mapper
from shared_msgs.msg import can_msg, auto_command_msg, thrust_status_msg, thrust_command_msg, esc_single_msg
from sensor_msgs.msg import Imu, Temperature
from std_msgs.msg import Float32

from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, disconnect

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

with open ('../../../../surface/frontend/src/packets.json') as json_data:
  data = json.load(json_data,)

dearFlask = data['dearflask']
dearClient = data['dearclient']
flaskMapper = packet_mapper.packet_mapper(dearFlask)
clientMapper = packet_mapper.packet_mapper(dearClient)
thrust_pub = None
auto_pub = None

@socketio.on('dearflask')
def dearflask(json):
  print('received')
  dearFlask = json
  socketio.emit('my_response', dearClient)

  #for data in dearFlask["thrusters"]:
  #  setattr(thrust_command_msg(), data, dearFlask["thrusters"][data])
  #thrust_pub.publish(thrust_command_msg())

  #for data in dearFlask["auto"]:
  #  setattr(auto_command_msg(), data, dearFlask["auto"][data])
  #auto_pub.publish(auto_command_msg())

def name_received(msg):
  names = clientMapper.get_msg_vars(msg)
  for name in names:
    clientMapper.map(name, getattr(msg, name), dearClient)

if __name__ == "__main__":
  rospy.init_node('mux_demux')
  ns = rospy.get_namespace() # This should return /surface
  
  # Retrieve data from the ROS System
  esc_sub = rospy.Subscriber('/rov/esc_single', 
      esc_single_msg, name_received)

  status_sub = rospy.Subscriber('/rov/thrust_status',thrust_status_msg,
    name_received);

  temp_sub = rospy.Subscriber('/rov/temp', Temperature,
    name_received);

  imu_sub = rospy.Subscriber('/rov/imu', Imu,
    name_received);

  ph_sub = rospy.Subscriber('/rov/ph',Float32,
    name_received);

  depth_sub = rospy.Subscriber('/rov/depth', Float32,
    name_received);

  # Publishers out onto the ROS System
  thrust_pub = rospy.Publisher(ns + 'thrust_command',
    thrust_command_msg, queue_size=10);

  auto_pub = rospy.Publisher(ns +'auto_command',
    auto_command_msg, queue_size=10);

  # Start socketio
  socketio.run(app, port=5001, debug=True)

  rate = rospy.Rate(10) # 10hz

  rospy.spin()
