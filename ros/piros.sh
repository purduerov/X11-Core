#! /bin/bash

source ~/X11-Core/ros/devel/setup.bash

src/can_com/scripts/start_can.sh
roslaunch ~/X11-Core/ros/launch/run_rov.launch
