#! /usr/bin/python
import rospy
import json
import socket
import packet_mapper
from shared_msgs.msg import can_msg, auto_command_msg, thrust_status_msg, thrust_command_msg, esc_single_msg
from sensor_msgs.msg import Imu, Temperature
from std_msgs.msg import Float32
from StringIO import StringIO

with open ('../../../../surface/frontend/src/packets.json') as json_data:
  data = json.load(json_data,)

dearflask = data['dearflask']
dearclient = data['dearclient']
flask_mapper = packet_mapper.packet_mapper(dearflask)
client_mapper = packet_mapper.packet_mapper(dearclient)
thrust_pub = None
auto_pub = None
serversocket = None
clientsocket = None

def serialize(data):
  io = StringIO()
  json.dump(data, io)
  return io.getvalue()

def deserialize(data):
  io = StringIO(data)
  return json.load(io)

def init_server():
  global serversocket
  serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  serversocket.bind((socket.gethostname(), 8000))
  print('server started')
  serversocket.listen(5)

def listen():
  global serversocket
  global clientsocket

  #listen for client
  (clientsocket, address) = serversocket.accept()
  print('client connected')

def accept():
  global serversocket
  global clientsocket
  global dearflask
  global dearclient

  length = clientsocket.recv(10)

  try:
    length = int(length)
  except:
    raise Exception()

  dearflask = deserialize(clientsocket.recv(length))

  #pass back dearclient
  encode = serialize(dearclient)
  head = str(len(encode))

  for x in range(10 - len(head)):
    head = '0' + head

  encode = head + encode
  clientsocket.send(encode)

  #update thrust and auto
  #flask_mapper.pam(thrust_command_msg(), dearflask)
  #flask_mapper.pam(auto_command_msg(), dearflask)
  #thrust_pub.publish(thrust_command_msg())
  #auto_pub.publish(auto_command_msg())

  return dearflask

def name_received(msg):
  names = client_mapper.get_msg_vars(msg)
  for name in names:
    client_mapper.map(name, getattr(msg, name), dearclient)

if __name__ == "__main__":
  global clientsocket

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

  ph_sub = rospy.Subscriber('/rov/ph',Float32,
    name_received);

  depth_sub = rospy.Subscriber('/rov/depth', Float32,
    name_received);

  # Publishers out onto the ROS System
  thrust_pub = rospy.Publisher(ns + 'thrust_command',
    thrust_command_msg, queue_size=10);

  auto_pub = rospy.Publisher(ns +'auto_command',
    auto_command_msg, queue_size=10);

  init_server()
  rate = rospy.Rate(10)
  while not rospy.is_shutdown():
    try:
      data = accept()
      print data
    except:
      print('no client connected')
      listen()
    rate.sleep()
