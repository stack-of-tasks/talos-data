#!/usr/bin/env python
# O. Stasse 17/01/2020
# LAAS, CNRS

import os
import rospy
import time
import roslaunch
import rospkg

from std_srvs.srv import Empty

# Start roscore
import subprocess
roscore = subprocess.Popen('roscore')
time.sleep(1)

# Get the path to talos_data
arospack = rospkg.RosPack()
talos_data_path = arospack.get_path('talos_data')

# Start talos_gazebo
rospy.init_node('starting_talos_gazebo', anonymous=True)
uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
roslaunch.configure_logging(uuid)

cli_args = [talos_data_path+'/launch/talos_gazebo_alone.launch',
            'world:=empty_forced',
            'enable_leg_passive:=false'
           ]
roslaunch_args = cli_args[1:]
roslaunch_file = [(roslaunch.rlutil.resolve_launch_arguments(cli_args)[0], roslaunch_args)]

launch_gazebo_alone = roslaunch.parent.ROSLaunchParent(uuid, roslaunch_file)
launch_gazebo_alone.start()
rospy.loginfo("talos_gazebo_alone started")

rospy.wait_for_service("/gazebo/pause_physics")
gazebo_pause_physics = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
gazebo_pause_physics()

time.sleep(5)
# Spawn talos model in gazebo
launch_gazebo_spawn_hs = roslaunch.parent.ROSLaunchParent(uuid,
                                                          [talos_data_path+'/launch/talos_gazebo_spawn_hs.launch'])
#launch_gazebo_spawn_hs = roslaunch.parent.ROSLaunchParent(uuid,
#                                                          [talos_data_path+'/launch/talos_gazebo_spawn_hs_wide.launch'])
launch_gazebo_spawn_hs.start()
rospy.loginfo("talos_gazebo_spawn_hs started")

rospy.wait_for_service("/gains/arm_left_1_joint/set_parameters")
time.sleep(5)
gazebo_unpause_physics = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)
gazebo_unpause_physics()

# Start roscontrol
launch_bringup = roslaunch.parent.ROSLaunchParent(uuid,
                                                  [talos_data_path+'/launch/talos_bringup.launch'])
launch_bringup.start()
rospy.loginfo("talos_bringup started")

# Start sot
roscontrol_sot_talos_path=arospack.get_path('roscontrol_sot_talos')
launch_roscontrol_sot_talos =roslaunch.parent.ROSLaunchParent(uuid,
                                                              [roscontrol_sot_talos_path+'/launch/sot_talos_controller_gazebo.launch'])
launch_roscontrol_sot_talos.start()
rospy.loginfo("roscontrol_sot_talos started")

rospy.spin()

