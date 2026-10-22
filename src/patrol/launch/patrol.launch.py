from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    arg_ns = DeclareLaunchArgument('namespace', default_value='robot_a')
    ns = LaunchConfiguration('namespace')

    patrol_node = Node(
        package='patrol',
        executable='patrol',
        name='patrol',
        namespace=ns,
        output='screen',
    )

    return LaunchDescription([arg_ns, patrol_node])