
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    arg_ns = DeclareLaunchArgument(
        'namespace', default_value='robot_a')
    arg_record = DeclareLaunchArgument(
        'record', default_value='false')
    arg_bag_dir = DeclareLaunchArgument(
        'bag_dir', default_value='/tmp/pr05_bag')
    arg_sub_rel = DeclareLaunchArgument(
        'subscriber_reliability', default_value='best_effort')

    ns = LaunchConfiguration('namespace')
    record = LaunchConfiguration('record')
    bag_dir = LaunchConfiguration('bag_dir')
    sub_rel = LaunchConfiguration('subscriber_reliability')

    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim',
        output='screen',
    )

    patrol_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('patrol'),
                'launch',
                'patrol.launch.py'
            ])
        ),
        launch_arguments={
            'namespace': ns,
            'subscriber_reliability': sub_rel,
        }.items(),
    )

    pose_relay_node = Node(
        package='turtle_bringup',
        executable='pose_relay',
        name='pose_relay',
        namespace=ns,
        remappings=[
            ('/robot_a/pose', '/turtle1/pose'),
        ],
        output='screen',
    )

    recorder = ExecuteProcess(
        cmd=[
            'ros2', 'bag', 'record',
            '-s', 'mcap',
            '-o', bag_dir,
            '--topics', PathJoinSubstitution(['/', ns, 'sensor_pose']), '/turtle1/cmd_vel',
        ],
        output='screen',
        condition=IfCondition(record),
    )

    return LaunchDescription([
        arg_ns,
        arg_record,
        arg_bag_dir,
        arg_sub_rel,
        turtlesim_node,
        patrol_launch,
        pose_relay_node,
        recorder,
    ])
