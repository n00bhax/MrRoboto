#!/usr/bin/env python

# This script is used to make the robot run into an object at an increasing speed to do a stifness measurement. 
# 

import rospy
from geometry_msgs.msg import Twist
import time

def talker():
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(5) # Hz
    vel_msg = Twist()

    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = -0.1

    while not rospy.is_shutdown() and vel_msg.angular.z > -0.9:
        vel_msg.linear.x += 0.005
        vel_msg.angular.z -= 0.02
        rospy.loginfo(vel_msg)
        pub.publish(vel_msg)
        rate.sleep()

    vel_msg.linear.x = 0
    rospy.loginfo(vel_msg)
    pub.publish(vel_msg)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass