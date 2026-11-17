#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

import tf2_ros

from geometry_msgs.msg import Twist


class Follower(Node):

    def __init__(self):
        super().__init__('follower')

        # TF2 setup
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(
            self.tf_buffer, self
        )

        # Velocity publisher
        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Target settings
        self.target_distance = 0.1

        # Controller gains
        self.linear_gain = 0.5
        self.angular_gain = 1.0

        # Maximum speeds
        self.max_linear_speed = 0.10
        self.max_angular_speed = 0.30

        # TF frames
        self.base_frame = 'base_link'
        self.marker_frame = 'marker_18'

        # Control loop (10 Hz)
        self.timer = self.create_timer(
            0.1,
            self.follow_marker
        )

        self.get_logger().info(
            'Marker follower started. Following marker_18'
        )

    def clamp(self, value, minimum, maximum):
        return max(minimum, min(value, maximum))

    def stop_robot(self):
        self.cmd_pub.publish(Twist())

    def follow_marker(self):

        try:
            # Get marker position relative to robot
            trans = self.tf_buffer.lookup_transform(
                self.base_frame,
                self.marker_frame,
                rclpy.time.Time()
            )

            x = trans.transform.translation.x
            y = trans.transform.translation.y

            # Calculate distance and angle
            distance = math.sqrt(x**2 + y**2)
            angle = math.atan2(y, x)

            # Calculate distance error
            distance_error = distance - self.target_distance

            self.get_logger().info(
                f'Distance: {distance:.2f} m | '
                f'Angle: {math.degrees(angle):.1f} degrees'
            )

            cmd = Twist()

            # Angular control
            cmd.angular.z = self.clamp(
                self.angular_gain * angle,
                -self.max_angular_speed,
                self.max_angular_speed
            )

            # Linear control
            cmd.linear.x = self.clamp(
                self.linear_gain * distance_error,
                -self.max_linear_speed,
                self.max_linear_speed
            )

            # Stop forward/backward movement when aligned poorly
            if abs(angle) > 0.5:
                cmd.linear.x = 0.0

            # Stop when close enough to target distance
            if abs(distance_error) < 0.03:
                cmd.linear.x = 0.0

            # Publish velocity
            self.cmd_pub.publish(cmd)

        except tf2_ros.TransformException as ex:

            self.get_logger().warning(
                f'Marker not found: {ex}'
            )

            self.stop_robot()


def main(args=None):

    rclpy.init(args=args)

    node = Follower()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.stop_robot()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

