from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([

        Node(
            package='tf_listener',
            executable='tf_listener',
            name='tf_listener',
            output='screen'
        ),

        Node(
            package='tf_listener',
            executable='charging_driver',
            name='ChargingStationDriver',
            output='screen'
        ),

    ])
