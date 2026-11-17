from geometry_msgs.msg import Twist
import math

self.cmd_pub = self.create_publisher(
    Twist,
    '/cmd_vel',
    10
)

x = trans.transform.translation.x
y = trans.transform.translation.y

distance = math.sqrt(x**2 + y**2)
angle = math.atan2(y, x)

cmd = Twist()

target_distance = 0.25

if distance > target_distance:

    cmd.angular.z = 1.0 * angle

    if abs(angle) < 0.2:
        cmd.linear.x = min(0.2, 0.5 * (distance - target_distance))

else:
    cmd.linear.x = 0.0
    cmd.angular.z = 0.0

self.cmd_pub.publish(cmd)
