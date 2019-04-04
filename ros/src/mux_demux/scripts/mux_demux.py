#! /usr/bin/python
import rospy
import json
import socketio
import engineio
import eventlet
import packet_mapper
import sys
import copy
#from threading import Thread, Lock
from threading import Lock
import thread
from shared_msgs.msg import can_msg, auto_command_msg, thrust_status_msg, thrust_command_msg, esc_single_msg
from sensor_msgs.msg import Imu, Temperature
from std_msgs.msg import Float32

with open ('../../../../surface/frontend/src/packets.json') as json_data:
  data = json.load(json_data,)

dearflask = data['dearflask']
dearclient = data['dearclient']
flask_mapper = packet_mapper.packet_mapper(dearflask)
client_mapper = packet_mapper.packet_mapper(dearclient)
thrust_pub = None
auto_pub = None

lock = Lock()
kill = None

sio = socketio.Server()

@sio.on('dearRos')
def accept(data):
  global dearflask
  global dearclient

  if not kill:
    lock.acquire()

    dearflask = copy.deepcopy(data)

    #pass back dearclient
    sio.emit('dearclient-response', dearclient)

    #update thrust and auto
    thrust = thrust_command_msg()
    auto = auto_commmand_msg()
    flask_mapper.pam(thrust, dearflask)
    flask_mapper.pam(auto, dearflask)
    thrust_pub.publish(thrust)
    auto_pub.publish(auto)

    lock.release()

#  return dearflask

def name_received(msg):
  global dearclient

  if not kill:
    lock.acquire()

    names = client_mapper.get_msg_vars(msg)
    for name in names:
      client_mapper.map(name, getattr(msg, name), dearclient)
    print(dearclient)

    lock.release()

def start_server(lol, meme, yeet):
  app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
  })

  eventlet.wsgi.server(eventlet.listen(('', 5001)), app)

if __name__ == "__main__":
  rospy.init_node('mux_demux')
  ns = rospy.get_namespace() # This should return /surface
  
  # Retrieve data from the ROS System
  esc_sub = rospy.Subscriber('/rov/esc_single',
      esc_single_msg, name_received)

  status_sub = rospy.Subscriber('/rov/thrust_status', thrust_status_msg,
    name_received);

  temp_sub = rospy.Subscriber('/rov/temp', Temperature,
    name_received);

  imu_sub = rospy.Subscriber('/rov/imu', Imu,
    name_received);

  ph_sub = rospy.Subscriber('/rov/ph', Float32,
    name_received);

  depth_sub = rospy.Subscriber('/rov/depth', Float32,
    name_received);

  # Publishers out onto the ROS System
  thrust_pub = rospy.Publisher(ns + 'thrust_command',
    thrust_command_msg, queue_size=10);

  auto_pub = rospy.Publisher(ns +'auto_command',
    auto_command_msg, queue_size=10);

  t = thread.start_new_thread(start_server, (1,2,3))
  print t

  while not rospy.is_shutdown():
    pass

  kill = True
  exit()
