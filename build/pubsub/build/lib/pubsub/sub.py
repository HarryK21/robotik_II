#!/usr/bin/env python3

import rclpy
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String

def main():
    rclpy.init()
    subscribernode = rclpy.create_node('myfirstsubscriber')
    subscribernode.create_subscription(String, 'myfirsttopic', mysubcallback, 10)
    try:
        rclpy.spin(subscribernode)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    subscribernode.destroy_node()
    rclpy.try_shutdown()

def mysubcallback(msg):
    print('You said: ', msg.data)

if __name__ == '__main__':
    main()