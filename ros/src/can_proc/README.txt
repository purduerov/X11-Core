Welcome to can_proc, the CAN processing package

This package groups all 3 can nodes so that any kind of can decoding code that is
written can be re-used in all 3 of these nodes. If you think some other functionality
belongs in this package please add it to the ROS channel on Slack.

Currently this package hosts 3 ros nodes
  * thruster_proc
    -subs: rx_can
    -pubs: thruster_proc

  * sensing_proc
    -subs: rx_can
    -pubs: current_sense

  * imu_proc
    -subs: rx_can
    -pubs: imu_data
