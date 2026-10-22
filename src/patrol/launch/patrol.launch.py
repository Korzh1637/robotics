
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    arg_ns = DeclareLaunchArgument(
        'namespace', default_value='robot_a')

    arg_sub_rel = DeclareLaunchArgument(
        'subscriber_reliability', default_value='best_effort')

    ns = LaunchConfiguration('namespace')
    sub_rel = LaunchConfiguration('subscriber_reliability')

    patrol_node = Node(
        package='patrol',
        executable='patrol',
        name='patrol',
        namespace=ns,
        output='screen',
        parameters=[{
            'subscriber_reliability': sub_rel
        }],
        remappings=[
            ('/robot_a/pose',
             PathJoinSubstitution(['/', ns, 'sensor_pose'])),
            ('cmd_vel', '/turtle1/cmd_vel'),
        ],
    )

    return LaunchDescription([
        arg_ns,
        arg_sub_rel,
        patrol_node,
    ])
