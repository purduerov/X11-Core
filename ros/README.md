`ROS_MASTER_URI` and `ROS_IP` both need to be set on the surface laptop at runtime, while the `ros/src/can_com/scripts/` folder must have either the virtual or real CAN startup scripts run to allow the `can_proc` nodes to run and not fail.

`ROS_IP` is the IP address of the laptop's ethernet port connection, which you should be able to find using `ifconfig` on a terminal on Ubuntu/Linux

`ROS_MASTER_URI` needs to be set using the export command that shows when you first boot into one of the pre-flashed SD cards (1 or 2, NOT 3), though roscore should have the URI print out during its process if you run it manually.

If it's not, and you use the command that forwards the text printout to a log file (has `&`'s in it, will print when you log into the Pi if ROSCORE isn't already running), view the log file for the command. It should be of a format of `http://<pi's address>:11311`

You may also find it's slightly more reliable to get ROS launched first on the Pi, and then on the laptop, but difinitive testing on that hasn't been made/consistent just yet. Try that if you have issues.