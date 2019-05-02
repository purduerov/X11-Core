#! /usr/bin/python
import sys
import can
import time

IDS = [0x201, 0x202, 0x203]
ZERO_POWER = 127
MIN_POWER = 7
MAX_POWER = 247
power_dir = 1
power_delta = 5
DELAY= .5
TX_DELAY = 0.05 # up to 50 messages/second
cur_power = ZERO_POWER

if __name__ == "__main__":
	channel = 'can0'
	can_bus = can.interface.Bus(channel=channel, bustype='socketcan')
        for _ in range(10):
            v = 0	
            board_id = 0x204 # solenoid board
            for i in range(8):
                    v |= 1 << i
                    v &= ~(1 << (i+4)%8)
                    data_array = [0]*8
                    data_array[-1] = v
                    data = bytearray(data_array)
                    can_tx = can.Message(arbitration_id=0x204, data=data, extended_id=False)
                    can_bus.send(can_tx)
                    time.sleep(TX_DELAY)

                    cur_power += power_dir * power_delta
                    if cur_power > MAX_POWER:
                            cur_power = MAX_POWER
                            power_dir *= -1
                    elif cur_power < MIN_POWER:
                            cur_power = MIN_POWER
                            power_dir *= -1
                    data_array = [0]*4
                    data_array.extend([cur_power]*4)
                    data = bytearray(data_array)
                    for board_id in IDS:
                            can_tx = can.Message(arbitration_id=board_id, data=data, extended_id=False)
                            can_bus.send(can_tx)
                            time.sleep(TX_DELAY)
                    time.sleep(DELAY)

        data_array = [0]*4
        data_array.extend([ZERO_POWER]*4)
        data = bytearray(data_array)
        for board_id in IDS:
                can_tx = can.Message(arbitration_id=board_id, data=data, extended_id=False)
                can_bus.send(can_tx)
                time.sleep(TX_DELAY)
        time.sleep(DELAY)
