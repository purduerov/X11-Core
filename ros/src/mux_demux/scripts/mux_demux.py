#! /usr/bin/python
import rospy
import json
import socketio
import engineio
import eventlet
import packet_mapper
import sys
import copy
import os
#from threading import Thread, Lock
import thread
from shared_msgs.msg import can_msg, auto_command_msg, thrust_status_msg, thrust_command_msg, esc_single_msg, tools_command_msg
from sensor_msgs.msg import Imu, Temperature
from std_msgs.msg import Float32

print os.getcwd()

try:
  with open ('../../surface/frontend/src/packets.json') as json_data:
    data = json.load(json_data,)
except:
  try:
    with open ('../../../../surface/frontend/src/packets.json') as json_data:
      data = json.load(json_data,)
  except:
    with open ('../X11-Core/surface/frontend/src/packets.json') as json_data:
      data = json.load(json_data,)

  


dearflask = data['dearflask']
dearclient = data['dearclient']
flask_mapper = packet_mapper.packet_mapper(dearflask)
client_mapper = packet_mapper.packet_mapper(dearclient)
thrust_pub = None
auto_pub = None
tools_pub = None

lock = thread.allocate_lock()
kill = None

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
  '/': {'content_type': 'text/html', 'filename': 'index.html'}
})


@sio.on('dearRos')
def accept(sid, data):
    global dearflask
    global dearclient

    if not kill:
        lock.acquire()

        dearflask = copy.deepcopy(data)

        #pass back dearclient
        # print dearclient
        sio.emit('dearclient-response', dearclient)

        # print data
        #update thrust and auto
        thrust = thrust_command_msg()
        auto = auto_command_msg()
        tools = tools_command_msg()
        flask_mapper.pam(thrust, dearflask)
        flask_mapper.pam(auto, dearflask)
        flask_mapper.pam(tools, dearflask)
        # print("Publishing:\n{}".format(thrust))
        thrust_pub.publish(thrust)
        auto_pub.publish(auto)
        tools_pub.publish(tools)

        lock.release()
  
    else:
        raise eventlet.StopServe

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

def start_server():
    global app
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
        thrust_command_msg, queue_size=10)

    auto_pub = rospy.Publisher(ns +'auto_command',
        auto_command_msg, queue_size=10)

    tools_pub = rospy.Publisher(ns + 'tools_command',
        tools_command_msg, queue_size=10)

    t = thread.start_new_thread(start_server, ())

    while not rospy.is_shutdown():
        pass

    kill = True
    exit()
