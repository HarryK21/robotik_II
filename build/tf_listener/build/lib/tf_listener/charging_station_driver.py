#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

import tf2_ros

from geometry_msgs.msg import Twist


class ChargingStationDriver(Node):

    def __init__(self):
        super().__init__('charging_station_driver')

        # Parameters
        self.declare_parameter('marker_frame', 'marker_19')
        self.declare_parameter('base_frame', 'base_link')

        # Distance at which the robot stops
        self.declare_parameter('target_distance', 0.30)

        # Maximum velocities
        self.declare_parameter('max_linear_speed', 0.08)
        self.declare_parameter('max_angular_speed', 0.25)

        # Controller gains
        self.declare_parameter('linear_gain', 0.3)
        self.declare_parameter('angular_gain', 1.0)

        self.marker_frame = self.get_parameter(
            'marker_frame').value

        self.base_frame = self.get_parameter(
            'base_frame').value

        self.target_distance = self.get_parameter(
            'target_distance').value

        self.max_linear_speed = self.get_parameter(
            'max_linear_speed').value

        self.max_angular_speed = self.get_parameter(
            'max_angular_speed').value

        self.linear_gain = self.get_parameter(
            'linear_gain').value

        self.angular_gain = self.get_parameter(
            'angular_gain').value

        # TF2
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

        # Control loop: 10 Hz
        self.timer = self.create_timer(
            0.1,
            self.control_loop
        )

        self.get_logger().info(
            'Charging Station Driver started!'
        )

    def stop_robot(self):
        cmd = Twist()
        self.cmd_pub.publish(cmd)

    def clamp(self, value, minimum, maximum):
        return max(minimum, min(value, maximum))

    def control_loop(self):

        try:
            # Get transform from marker to robot base
            trans = self.tf_buffer.lookup_transform(
                self.base_frame,
                self.marker_frame,
                rclpy.time.Time()
            )

            # Marker position relative to robot
            x = trans.transform.translation.x
            y = trans.transform.translation.y

            # Calculate distance and bearing
            distance = math.sqrt(x**2 + y**2)
            angle = math.atan2(y, x)

            self.get_logger().info(
                f'Distance: {distance:.2f} m | '
                f'Angle: {math.degrees(angle):.1f} deg'
            )

            cmd = Twist()

            # Check whether the marker is in front
            if x <= 0.0:
                self.stop_robot()
                return

            # Check docking distance
            if x <= self.target_distance:
                self.stop_robot()

                self.get_logger().info(
                    'Target distance reached. Robot stopped.'
                )
                return

            # Calculate angular velocity
            cmd.angular.z = self.clamp(
                self.angular_gain * angle,
                -self.max_angular_speed,
                self.max_angular_speed
            )

            # Only drive forward when sufficiently aligned
            if abs(angle) < 0.15:

                cmd.linear.x = self.clamp(
                    self.linear_gain *
                    (x - self.target_distance),
                    0.0,
                    self.max_linear_speed
                )

            else:
                cmd.linear.x = 0.0

            # Publish velocity
            self.cmd_pub.publish(cmd)

        except tf2_ros.TransformException as ex:

            self.get_logger().warning(
                f'Marker transform unavailable: {ex}'
            )

            # Safety: stop if marker disappears
            self.stop_robot()


def main(args=None):

    rclpy.init(args=args)

    node = ChargingStationDriver()

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
