#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3
import numpy as np

acc_x= []

def callback(msg):
    print(msg.linear_acceleration.x)
    acc_x.append(msg.linear_acceleration.x)
    
def listener():

    rospy.init_node('Sensor_recorder', anonymous=True)
    rospy.Subscriber("/camera/imu", Imu, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass