#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


class GamepadReader(Node):
    def __init__(self):
        super().__init__('gamepad_reader')

        # Subscribing to the gamepad output
        self.subscription = self.create_subscription(
            Joy, 'joy', self.joy_callback, 10)
        
        # Publishing the robot commands
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.get_logger().info('Gamepad Reader Node has been started.')
    
    def joy_callback(self, msg):
        twist = Twist()
        
        # 1. Base Joystick Logic
        # Upper left joystick forward-backward motion scaled at 1m/s
        forward_speed = msg.axes[1] * 1.0 
        # Lower right joystick left-right motion scaled at 0.5 rad/s
        turning_speed = msg.axes[2] * 0.5 
        
        # 2. Button Modifiers Logic (Must happen BEFORE writing to twist)
        
        # Check if indices exist to avoid index out of range crashes
        if len(msg.buttons) > 7:
            # When R2 is pressed (increase speed)
            if msg.buttons[7] == 1: 
                forward_speed *= 1.10
                
            # When L2 is pressed (decrease speed)
            if msg.buttons[5] == 1: 
                forward_speed *= 0.90  
                
            # Stop button 3 (Circle button on PS4 controller is pressed)
            if msg.buttons[2] == 1:
                self.get_logger().warn('EMERGENCY STOP PRESSED')
                forward_speed = 0.0
                turning_speed = 0.0

        # 3. Populate and Publish the Twist Message
        twist.linear.x = float(forward_speed)
        twist.angular.z = float(turning_speed)
        
        self.publisher.publish(twist)

def main():
    rclpy.init()
    gamepad_node = GamepadReader()

    try:
        rclpy.spin(gamepad_node)
    except KeyboardInterrupt:
        pass
        
    gamepad_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()