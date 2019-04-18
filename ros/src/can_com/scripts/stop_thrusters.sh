#! /bin/bash
#sudo ip link set can0 up type can bitrate 125000 
cansend can0 201#000000007F7F7F7F
#cansend can0 202#000000007F7F7F7F
cansend can0 203#000000007F7F7F7F
#sudo ip link set can0 down
#sudo ip link set can0 type can restart-ms 100
