#!/usr/bin/env python3

import rclpy
from rclpy.executors import ExternalShutdownException
from time import sleep  

def main():
    rclpy.init()
    node = rclpy.create_node('firstnode')
    node.declare_parameter('my_param', 13)
    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=1.0)
            print(node.get_parameter('my_param').value)
            sleep(1.0)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    
    node.destroy_node()
    rclpy.try_shutdown()
    while rclpy.ok():
        sleep(1.0)

if __name__ == '__main__':
    main()
    