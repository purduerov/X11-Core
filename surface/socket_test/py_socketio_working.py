import engineio
import eventlet
import socketio
import json
import random

with open('../frontend/src/packets.json') as json_file:
    base_packet = json.load(json_file)

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

@sio.on('dearRos')
def dearflask(sid, data):
    # base_packet["dearclient"]["manipulator"]["power"] = base_packet["dearclient"]["manipulator"]["power"] + 1
    base_packet["dearclient"]["sensors"]["esc"]["temperatures"][0] += 1
    base_packet["dearclient"]["sensors"]["esc"]["currents"][0] += 1
    print('message ', data)
    print(base_packet["dearclient"])
    print("\n")
    sio.emit('dearclient-response', base_packet["dearclient"])

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5001)), app)
