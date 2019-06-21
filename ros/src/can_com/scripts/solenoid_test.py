#! /usr/bin/python
import sys
import can
import time

IDS = [516]
POS_RANGE = 4
DEFAULT_POWER = 200
ZERO_POWER = 127
DELAY= .5


# This is a test script intended to simplify identification of hardware thruster
# configuration by sending commands to each possible thruster position one at a time.


if __name__ == "__main__":
    channel = 'can0'
    if len(sys.argv) == 2:
        channel = sys.argv[1]
    can_bus = can.interface.Bus(channel=channel, bustype='socketcan')

    values = [0b1, 0b1000000, 0b10000, 0b10, 0b100, 0b100000, 0b10000000, 0b1000]
    #for _ in range(50): 
    for v in values:
        data_array = [0]*8;
        data_array[-1] = v
        data = bytearray(data_array)

        print("SOL: %s" % bin(v))
        can_tx = can.Message(arbitration_id=516, data=data, extended_id=False)
        can_bus.send(can_tx)

        time.sleep(DELAY)
