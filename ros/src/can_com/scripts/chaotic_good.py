#! /usr/bin/python
import sys
import can
import time

IDS = [513, 514, 515]
POS_RANGE = 4
DEFAULT_POWER = 146
ZERO_POWER = 127


# This is a test script intended to simplify identification of hardware thruster
# configuration by sending commands to each possible thruster position one at a time.


if __name__ == "__main__":
    channel = 'can0'
    I = IDS[0]
    if len(sys.argv) == 2:
        channel = sys.argv[1]
    can_bus = can.interface.Bus(channel=channel, bustype='socketcan')

    for i in range(8):
        data_list = list()
        [data_list.append(0) for _ in range(i)]
        data_list.append(DEFAULT_POWER)
        [data_list.append(0) for _ in range(i + 1, 8)]

        #[data_list.append(DEFAULT_POWER) for _ in range(8)]
        data = bytearray(data_list)
        print str(I) + ' : ' + str(list(data))

        can_tx = can.Message(arbitration_id=I, data=data, extended_id=False)
        can_bus.send(can_tx)

        time.sleep(2)

    #data_list = list()
    #[data_list.append(ZERO_POWER) for _ in range(8)]
    #data = bytearray(data_list)
    #print str(i) + ' : ' + str(list(data)) + ' STOP'

    #can_tx = can.Message(arbitration_id=i, data=data, extended_id=False)
    #can_bus.send(can_tx)


