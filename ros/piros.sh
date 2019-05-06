#! /bin/bash

source ~/X11-Core/ros/devel/setup.bash

~/X11-Core/ros/src/can_com/scripts/start_can.sh

mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so -fps 30" > ~/mjpeg.log &

# ./reset_can.py &

roslaunch ~/X11-Core/ros/launch/run_rov.launch 
# killall reset_can.py
