#! /bin/bash

export ROS_IP=10.42.0.1
export ROS_MASTER_URI=http://10.42.0.204:11311
source devel/setup.bash

echo "|$0| |$1|"

if [ "$1" == "mock" ] || [ "$1" == "Mock" ]
then
	roslaunch launch/run_msurface.launch
else
	roslaunch launch/run_surface.launch
fi

