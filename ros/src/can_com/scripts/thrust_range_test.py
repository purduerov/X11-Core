#! /usr/bin/python

import sys
import can
import time
import signal

def getSignal(bus):
    def signal_handler(sig, frame):
        print("CTRL+C detected")
        zeroOutThrusters(bus=bus)
        print("Thrusters zero-ed out")
        sys.exit(0)

    return signal_handler

def zeroOutThrusters(bus=None):
    a = mapThrusters([127] * 8)

    writeToCan(a, timesleep=0.0, bus=bus, printOut=True)

def mapThrusters(can_pow, can_map=None, printOut=False):
    if can_map is None:
        can_map = {
            0x201: [None, 0, 1, None],
            0x202: [None, 3, 4, 7],
            0x203: [5, 6, None, 2]
        }
    
    can_out = {}
    
    for cid in can_map:
        data = [0, 0, 0, 0] 
        cur = can_map[cid]

        for el in cur:
            if el is not None:
                data.append(can_pow[el])
            else:
                data.append(127)


        if printOut:
            print("|{}|".format(cid))
            for el in data:
                print("{}".format(el))
            print("----")

        can_out[cid] = data

    return can_out

def writeToCan(packet, timesleep=1, bus=None, printOut=False):
    if bus is None:
        bus = can.interface.Bus(channel='can0', bustype='socketcan')

    for cid in packet:
        # print(packet[cid])
        data = bytearray(packet[cid])

        can_tx = can.Message(arbitration_id=cid, data=data, extended_id=False)

        bus.send(can_tx)
        
        if printOut:
            tst = "    {}:".format(cid)
            for el in data:
                tst += " {0:03}".format(int(el))
            
            print(tst)


def mainLoop(timesleep=1, bound=5, increment=1, mid=127, channel='can0', bustype='socketcan'):
    can_bus = can.interface.Bus(channel=channel, bustype=bustype)

    signal.signal(signal.SIGINT, getSignal(can_bus))

    inc = increment
    offset = 0
    while True:
        num = 127+offset
        print("Thrusters setting to {}".format(num))

        base = [num]*8

        thrusts = mapThrusters(base)

        writeToCan(thrusts, timesleep=timesleep, bus=can_bus, printOut=True)

        if offset >= bound:
            inc = -increment
        elif offset <= -bound:
            inc = increment
        
        offset += inc
        
        time.sleep(timesleep)

    zeroOutThrusters(bus=can_bus)


if __name__ == "__main__":
    bound = 10 * 5
    inc = 1 
    print(mainLoop(bound=bound, increment=inc, timesleep=.04))
    
