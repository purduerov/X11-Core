#! /usr/bin/python
#from shared_msgs.msg import can_msg, auto_command_msg, thrust_status_msg, thrust_command_msg, esc_single_msg
#from sensor_msgs.msg import Imu, Temperature
#from std_msgs.msg import Float32
import shared_msgs.msg

def init(packet):
    names = list()
    msgs = dict([(name, cls) for name, cls in shared_msgs.msg.__dict__.items() if isinstance(cls, type)])
    for msg in msgs.keys():
        #print msg
        for key,value in getattr(shared_msgs.msg, msg).__dict__.iteritems():
            if type(value).__name__ == 'member_descriptor':
                names.append(key)

    print 'names: ', names

    for name in names:
        found = _match_variable(packet, name)
        if found:
            print found

def _match_variable(d, name):
    for key,value in d.items():
        if type(value) == dict:
            ret = _match_variable(value, name)
            if ret != "":
                return key + '.' + ret
        if key == name:
            return key
    return ""

def map(name):
    pass

if __name__ == "__main__":
    init({   'inside' : {   'addr' : 'hello', 'in2' : { 'data' : 1    } }   })
