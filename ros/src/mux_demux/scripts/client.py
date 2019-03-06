import socket
import json
import os
from StringIO import StringIO

with open ('../../../../surface/frontend/src/packets.json') as json_data:
  dearflask = json.load(json_data,)
#dearflask = { 'data': 1, 'meme': { 'lol': 'hehexd' } }
#dearflask = {'youngsik': 'meme', 'tobi': 'peen', 'jeremy': {'sheen': 'leen', 'dean': 'fiend'} }

s = None

# posts dearflask as a client
def talk():
  global dearflask
  global s
  encode = serialize(dearflask)
  head = str(len(encode))

  for x in range(10 - len(head)):
    head = '0' + head

  encode = head + encode
  s.send(encode)

  length = s.recv(10)

  try:
    length = int(length)
  except:
    return

  get = deserialize(s.recv(length))
  return get

def serialize(data):
  io = StringIO()
  json.dump(data, io)
  return unicode(io.getvalue(), 'utf-8')

def deserialize(data):
  io = StringIO(data)
  return json.load(io)

def init_client():
  #create an INET, STREAMing socket
  global s

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((socket.gethostname(), 5001))
  print('connected')
 
if __name__ == '__main__':
  init_client()
  get = talk()
  print(get)
