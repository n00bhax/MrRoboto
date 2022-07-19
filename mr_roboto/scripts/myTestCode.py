#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

def talker():
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=2)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # 1hz
    vel_msg = Twist()
    speed = 0

    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    while not rospy.is_shutdown() and speed < 100:
        speed += 10
        vel_msg.linear.x = speed
        rospy.loginfo(vel_msg)
        pub.publish(vel_msg)
        rate.sleep()

    vel_msg.linear.x = 0
    pub.publish(vel_msg)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass