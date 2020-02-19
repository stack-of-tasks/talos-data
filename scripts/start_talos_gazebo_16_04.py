#!/usr/bin/env python
# O. Stasse 17/01/2020
# LAAS, CNRS

# This file is a temporary fix for the ubuntu version 16.04 of the script start_talos_gazebo.py
# The path to talos_data cannot be retreive using the rospkg.RosPack() and get_path('talos_data') in 16.04.
# This should be investigated (see issue #4 "Hardcoded talos_data path for 16.04 in script start_talos_gazebo_16_04.py")

import os
import rospy
import time
import roslaunch
from std_srvs.srv import Empty

# Start roscore
import subprocess
roscore = subprocess.Popen('roscore')
time.sleep(1)

# Start talos_gazebo
rospy.init_node('starting_talos_gazebo', anonymous=True)
uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
roslaunch.configure_logging(uuid)

launch_gazebo_alone = roslaunch.parent.ROSLaunchParent(uuid, ["/opt/openrobots/share/talos_data/launch/talos_gazebo_alone.launch"])
launch_gazebo_alone.start()
rospy.loginfo("talos_gazebo_alone started")

rospy.wait_for_service("/gazebo/pause_physics")
gazebo_pause_physics = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
gazebo_pause_physics()

time.sleep(3)
# Spawn talos model in gazebo
launch_gazebo_spawn_hs = roslaunch.parent.ROSLaunchParent(uuid, ["/opt/openrobots/share/talos_data/launch/talos_gazebo_spawn_hs.launch"])
launch_gazebo_spawn_hs.start()
rospy.loginfo("talos_gazebo_spawn_hs started")

rospy.wait_for_service("/gains/arm_left_1_joint/set_parameters")
time.sleep(3)
gazebo_unpause_physics = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)
gazebo_unpause_physics()

# Start roscontrol
launch_bringup = roslaunch.parent.ROSLaunchParent(uuid, ["/opt/openrobots/share/talos_bringup/launch/talos_bringup.launch"])
launch_bringup.start()
rospy.loginfo("talos_bringup started")

# # Start sot
# Start sot in another terminal with "roslaunch roscontrol_sot_talos sot_talos_controller_gazebo.launch"
# in order to have the logs saved. Otherwise the data are not correctly dumped when the process is killed.


rospy.spin()

