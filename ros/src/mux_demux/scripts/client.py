# test client for mux_demux.py
import socketio
import time
import json

sio = socketio.Client()

@sio.on('connect')
def on_connect():
  print('connected to server')

@sio.on('my_reponse')
def my_response(json):
  print(json)

if __name__ == '__main__':

  with open ('../../../../surface/frontend/src/packets.json') as json_data:
    data = json.load(json_data,)

  dearFlask = data['dearflask']
  print(dearFlask)

  sio.connect('http://localhost:5001')
  sio.emit('dearflask', dearFlask)
  sio.disconnect()

