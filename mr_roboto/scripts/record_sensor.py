#!/usr/bin/env python2
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3
from rosserial_arduino.msg import Adc
from rosgraph_msgs.msg import Clock

import numpy as np

acc= np.empty(shape=[4, 0])

adc = []

clock = 0

def acc_callback(msg):
    global acc

    xyz = np.array([ msg.linear_acceleration.x,  msg.linear_acceleration.y,  msg.linear_acceleration.z])
    xyz = np.append(xyz, clock)
    acc = np.append(acc, xyz.reshape(4,1), axis=1)

    np.savetxt('/home/willem/catkin_ws/src/mr_roboto/scripts/acc.csv', acc.T, fmt='%.18e %.18e %.18e %d', delimiter=';')

def adc_callback(msg):

    adc.append((msg.adc0, clock))
    np.savetxt('/home/willem/catkin_ws/src/mr_roboto/scripts/adc.csv', np.asarray(adc), fmt='%d', delimiter=';')

def clock_callback(msg):
    global clock

    clock = msg.clock.secs - 1661503362 + msg.clock.nsecs*10^(-9)
    print("Time:" + str(clock)) #for debugging purposes
    
def listener():

    rospy.init_node('Sensor_recorder', anonymous=True)
    rospy.Subscriber("/clock", Clock, clock_callback)
    rospy.Subscriber("/camera/imu", Imu, acc_callback)
    rospy.Subscriber("/adc", Adc, adc_callback)
    

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass