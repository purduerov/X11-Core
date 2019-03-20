import engineio
import eventlet
import socketio
import json

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
    print('message ', data)
    print(base_packet["dearclient"])
    print("\n")
    sio.emit('dearclient-response', base_packet["dearclient"])

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5001)), app)
