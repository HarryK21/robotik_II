#!/usr/bin/env python3

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String

class MyPublisherClass(Node):

    def __init__(self):
        super().__init__('myfirstpublisher')
        self.mypub = self.create_publisher(String, 'myfirsttopic', 1)
        self.create_timer(0.1, self.mytimercallback)

    def mytimercallback(self):
        mymsg = String()
        mymsg.data = 'Hello ROS2 Communication'
        self.mypub.publish(mymsg)

def main():
    rclpy.init()
    publishernode = MyPublisherClass()
    try:
        rclpy.spin(publishernode)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    publishernode.destroy_node()
    rclpy.try_shutdown()

if __name__ == '__main__':
    main()
