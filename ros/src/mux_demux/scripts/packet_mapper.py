#! /usr/bin/python
import shared_msgs.msg
import json

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

        print 'names: ', names

        for name in names:
            path = self._build_path(packet, name)
            if path:
                self.topic_paths[name] = path

        print 'paths: ', self.topic_paths

    def map(self, var, value, packet):
        path = self.topic_paths[var]
        split = path.split('.')
        p = packet
        for e in split[:-1]:
            p = p[e]
        p[split[-1]] = value

    def get_msg_vars(self, msg):
        names = []
        for key,value in getattr(shared_msgs.msg, type(msg).__name__).__dict__.iteritems():
            if type(value).__name__ == 'member_descriptor':
                names.append(key)
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
    packet = { 'addr' : 'hello', 'in2' : { 'data' : 1    }   }
    json = { 'one' : { 'two':2, 'three':3}}
    mapper = packet_mapper(packet)

    for data in json['one']:
      print data

    # This code changes variables within a packet
    #mapper.map('addr', '6581', packet)
    mapper.map('data', '0', packet)
    #print packet["in2"]["data"]

    # This code gives you a list of the names of the variables in a message object

    #msg = shared_msgs.msg.can_msg()
    #print msg
    #print mapper.get_msg_vars(msg)
    #print getattr(msg, "id")
    #setattr(msg, "id", 1)
    #print getattr(msg, "id")
