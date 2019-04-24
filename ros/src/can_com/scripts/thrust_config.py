#! /usr/bin/python
import sys
import can
import time

IDS = [513, 514, 515]
POS_RANGE = 4
DEFAULT_POWER = 140
POWER_DELTA = 30
ZERO_POWER = 127
DELAY=5


# This is a test script intended to simplify identification of hardware thruster
# configuration by sending commands to each possible thruster position one at a time.


if __name__ == "__main__":
    channel = 'can0'
    if len(sys.argv) == 2:
        channel = sys.argv[1]
    can_bus = can.interface.Bus(channel=channel, bustype='socketcan')

    # initialize the thrusters
    #data=bytearray([0]*8);
    #IDS = [514]
    #for i in IDS:
    #    can_tx = can.Message(arbitration_id=i, data=data, extended_id=False)
    #    can_bus.send(can_tx)
    #    time.sleep(DELAY)

    for i in IDS:
        for p in range(POS_RANGE):
            # first go backwards
            data_list = list()
            data_list = [0,0,0,0]                             # adds zeros to last 4 unused positions
            [data_list.append(ZERO_POWER) for _ in range(p)]                          # adds ZERO POWER buffers before target pos
            data_list.append(ZERO_POWER-POWER_DELTA)                                     # adds DEFAULT POWER at target pos
            [data_list.append(ZERO_POWER) for _ in range(POS_RANGE - p - 1)]    # adds ZERO POWER buffers after target pos
            data = bytearray(data_list)
            print str(i) + ' : ' + str(list(data))

            can_tx = can.Message(arbitration_id=i, data=data, extended_id=False)
            can_bus.send(can_tx)

            time.sleep(DELAY)

            # then stop
            data_list = list()
            [data_list.append(0) for _ in range(4)]
            [data_list.append(ZERO_POWER) for _ in range(4, 8)]
            data = bytearray(data_list)
            print str(i) + ' : ' + str(list(data)) + ' STOP'
            can_tx = can.Message(arbitration_id=i, data=data, extended_id=False)
            can_bus.send(can_tx)
            
            time.sleep(DELAY)
#
#            # then forwards
#            data_list = list()
#            data_list = [0,0,0,0]                             # adds zeros to last 4 unused positions
#            [data_list.append(ZERO_POWER) for _ in range(p)]                          # adds ZERO POWER buffers before target pos
#            data_list.append(ZERO_POWER+POWER_DELTA)                                     # adds DEFAULT POWER at target pos
#            [data_list.append(ZERO_POWER) for _ in range(POS_RANGE - p - 1)]    # adds ZERO POWER buffers after target pos
#            data = bytearray(data_list)
#            print str(i) + ' : ' + str(list(data))
#
#            can_tx = can.Message(arbitration_id=i, data=data, extended_id=False)
#            can_bus.send(can_tx)
#
#            time.sleep(DELAY)

        data_list = list()
        [data_list.append(0) for _ in range(4)]
        [data_list.append(ZERO_POWER) for _ in range(4, 8)]
        data = bytearray(data_list)
        print str(i) + ' : ' + str(list(data)) + ' STOP'

        can_tx = can.Message(arbitration_id=i, data=data, extended_id=False)
        can_bus.send(can_tx)

        time.sleep(DELAY)

