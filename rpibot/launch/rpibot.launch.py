from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    pkg_share = FindPackageShare(package='rpibot')

    # Get the URDF/XACRO file path
    robot_description_file = PathJoinSubstitution([
        pkg_share, 'urdf', 'rpibot.urdf.xacro'
    ])

    # Use xacro to generate the robot description string
    robot_description = Command([
        FindExecutable(name='xacro'),
        ' ',
        robot_description_file
    ])

    # Nodes for robot_state_publisher and RViz
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}]
    )

    return LaunchDescription(
        [
            robot_state_publisher_node
        ]
    )
