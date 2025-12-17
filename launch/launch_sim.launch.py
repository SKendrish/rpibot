import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

import xacro

package_name = "rpibot"

def generate_launch_description():

    package_name = "rpibot"
    gazebo_pkg = "ros_gz_sim"
    gazebo_brdige_pkg = "ros_gz_bridge"
    world_path = PathJoinSubstitution([
        FindPackageShare(package_name),
        "worlds",
        "default_world.sdf"
    ])
    gz_bridge_config_path = PathJoinSubstitution([
        FindPackageShare(package_name),
        "config",
        "gz_bridge.yaml"
    ])

    # Include roboty state publisher launch file and urdf
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare(package_name),
                "launch",
                "rsp.launch.py"
            ])
        ]),
        launch_arguments={"use_sim_time": "true"}.items()
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare(gazebo_pkg),
                "launch",
                "gz_sim.launch.py"
            ])
        ]),
        launch_arguments={
            "gz_args": ["-r -v v4 empty.sdf"],
            "use_sim_time": "True",
            "on_exit_shutdown": "True"
        }.items()
    )

    gazebo_bridge = Node(
        package=gazebo_brdige_pkg,
        executable="parameter_bridge",
        output="screen",
        parameters=[{
            "config_file": gz_bridge_config_path
        }]
    )

    spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=["-name", "rpibot",
                   "-topic", "/robot_description",
                   "-x", "0.0",
                   "-y", "0.0",
                   "-z", "1.0"
    ])
    
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        gazebo_bridge
    ])