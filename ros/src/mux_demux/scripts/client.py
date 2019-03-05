import socket
import json
import os
from StringIO import StringIO

with open ('packet.json') as json_data:
  dearflask = json.load(json_data,)

# posts dearflask as a client
def post():
  global dearflask
  global s
  encode = serialize(dearflask)
  head = str(len(encode))

  for x in range(10 - len(head)):
    head = '0' + head

  encode = head + encode
  s.send(encode)

def serialize(data):
  io = StringIO()
  json.dump(data, io)
  return unicode(io.getvalue(), 'utf-8')

def deserialize(data):
  io = StringIO(data)
  return json.load(io)

def client():
  #create an INET, STREAMing socket
  global s
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((socket.gethostname(), 5001))
 
if __name__ == '__main__':
  client()
  post()
