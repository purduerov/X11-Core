#! /usr/bin/python
#https://wiki.ros.org/rospy_message_converter ??
import shared_msgs.msg
import json
import os

class packet_mapper:

    topic_paths = {}

    def __init__(self, packet):
        names = list()
        msgs = dict([(name, cls) for name, cls in shared_msgs.msg.__dict__.items() if isinstance(cls, type)])
        for msg in msgs.keys():
            #print msg
            for key,value in getattr(shared_msgs.msg, msg).__dict__.iteritems():
                if type(value).__name__ == 'member_descriptor':
                    names.append(key)

        #print 'names: ', names

        for name in names:
            path = self._build_path(packet, name)
            if path:
                self.topic_paths[name] = path

        #print 'paths: ', self.topic_paths

    # update packet[path] = value
    def map(self, var, value, packet):
        path = self._build_path(packet, var)
        #path = self.topic_paths[var]
        split = path.split('.')
        p = packet
        for e in split[:-1]:
            p = p[e]
        p[split[-1]] = value

    # update msg[path] = packet[path]
    def pam(self, msg, packet):
        names = self.get_msg_vars(msg)
        for name in names:
            path = self._build_path(packet, name)
            #path = self.topic_paths[name]
            split = path.split('.')
            p = packet
            for e in split[:-1]:
                p = p[e]
            setattr(msg, name, p[split[-1]])

    def get_msg_vars(self, msg):
        names = []
        #for key,value in getattr(shared_msgs.msg, type(msg).__name__).__dict__.iteritems():
        #    if type(value).__name__ == 'member_descriptor':
        #        names.append(key)
        #return names
        for name, var_type in zip(msg.__slots__, msg._slot_types):
            names.append(name)
        return names

    def _build_path(self, d, name):
        for key,value in d.items():
            if type(value) == dict:
                ret = self._build_path(value, name)
                if ret != "":
                    return key + '.' + ret
            if key == name:
                return key
        return ""

if __name__ == "__main__":
    #with open ('../../../../surface/frontend/src/packets.json') as json_data:
    #  packet = json.load(json_data,)
    packet = { 'lol': 1, 'meme': { 'id':'1', 'asdf': '3', 'data': '2' } }
    #json = { 'one' : { 'two':2, 'three':3}}
    mapper = packet_mapper(packet)

    #for data in json['one']:
    #  print data

    # This code changes variables within a packet
    mapper.map('lol', '6581', packet)
    print packet
    #mapper.map('data', '0', packet)

    #This code gives you a list of the names of the variables in a message object

    #msg = shared_msgs.msg.thrust_command_msg()
    #print
    #lol = zip(msg.__slots__, msg._slot_types)
    #print lol
    #print
    #print packet

    #names = mapper.get_msg_vars(msg)
    #for name in names:
    #  mapper.map(name, getattr(msg, name), packet)
    #print packet

    #packet = { 'lol': 1, 'meme': { 'id':'1', 'lol': '3', 'data': '2' } }

    #mapper.pam(msg, packet)
    #print packet
    #print msg
