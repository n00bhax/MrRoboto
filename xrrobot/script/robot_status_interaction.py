#!/usr/bin/env python
#coding=utf-8


import socket
import json
import time
import threading
from math import pi

import rospy
from riki_msgs.msg import Battery
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState


def send_msg():
    while app_is_run:
        robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            robot_socket.connect(("127.0.0.1", 11322))

            xrJson = {
                "version": "b0.0",
                "keep_alive": True,
                "url": "/servo/arm",
                "method": "post",
                "data": {"servo": ['30', '150', '0', '-30']},
            }

            tem_data = json.dumps(xrJson).encode("utf-8")
            print(tem_data)
            robot_socket.send(tem_data)
            time.sleep(0.5)

            xrJson = {
                "version": "b0.0",
                "keep_alive": True,
                "url": "/servo/tilt",
                "method": "post",
                "data": {"servo": ['90', '90']},
            }

            tem_data = json.dumps(xrJson).encode("utf-8")
            print(tem_data)
            robot_socket.send(tem_data)
            time.sleep(2)
            break
        except Exception:
            time.sleep(2)
            continue

    while app_is_run:
        print("init socket")
        robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        robot_socket.settimeout(5)

        try:
            try:
                time.sleep(1)
                robot_socket.connect(("127.0.0.1", 11322))
                
            except Exception:
                continue

            while app_is_run:

                try:
                    if send_bytes:
                        robot_socket.send(send_bytes.pop())
                        recv = robot_socket.recv(200)
                        time.sleep(0.01)

                    # read move command
                    xrJson = {
                        "version": "b0.0",
                        "keep_alive": True,
                        "url": "/movement",
                        "method": "get",
                        "data": {},
                    }

                    tem_data = json.dumps(xrJson).encode("utf-8")
                    robot_socket.send(tem_data)

                    recv = robot_socket.recv(200)
                    # print(recv)
                    try:
                        recv = json.loads(recv)
                        # print(recv)
                        if "direction" in recv["data"]:
                            # print("data got")
                            pub_movement(recv["data"]["direction"].encode("utf-8"))
                    except ValueError:
                        continue
                    
                    time.sleep(0.01)

                    # read arm servo command
                    xrJson = {
                        "version": "b0.0",
                        "keep_alive": True,
                        "url": "/servo/arm",
                        "method": "get",
                        "data": {},
                    }

                    tem_data = json.dumps(xrJson).encode("utf-8")
                    robot_socket.send(tem_data)
                    arm_recv = robot_socket.recv(200)
                    # print(recv)
                    try:
                        arm_recv = json.loads(arm_recv)
                        # print(recv)
                        if "servo" in arm_recv["data"]:
                            for i in range(4):
                                global servos_is_update

                                temp_servo = float(arm_recv["data"]["servo"][i])/180.0 * pi
                                if not temp_servo == servos[i]:
                                    servos_is_update = True
                                    servos[i] = temp_servo
        
                    except ValueError:
                        continue

                    time.sleep(0.01)

                    # read tilt servo command
                    xrJson = {
                        "version": "b0.0",
                        "keep_alive": True,
                        "url": "/servo/tilt",
                        "method": "get",
                        "data": {},
                    }

                    tem_data = json.dumps(xrJson).encode("utf-8")
                    robot_socket.send(tem_data)
                    tilt_recv = robot_socket.recv(200)
                    # print(recv)
                    try:
                        tilt_recv = json.loads(tilt_recv)
                        if "servo" in recv["data"]:
                            for i in range(2):
                                global servos_is_update

                                temp_servo = (float(recv["data"]["servo"][i]) -90) / 180.0 * pi
                                if not temp_servo == servos[i+4]:
                                    servos[i+4] = temp_servo
                                    servos_is_update = True

                    except ValueError:
                        continue

                    if servos_is_update:
                        global servos_is_update
                        servo.position = servos
                        servo_pub.publish(servo)
                        rospy.loginfo("servo pub")
                        servos_is_update = False

                    time.sleep(0.1)

                except socket.error:
                    robot_socket.close()
                    break

        except KeyboardInterrupt:
            robot_socket.close()
            break
        finally:
            robot_socket.close()


def pub_movement(movement):
    global robot_is_stop
    # print(type(movement), type(""))
    if not isinstance(movement, type("")):
        # print("break")
        return False

    move_msg = Twist()
    if movement == "stop":
        if robot_is_stop:
            return None
        rospy.loginfo("stop")
        # move_msg.angular.z = 0.0
        # move_msg.linear.x = 0.0
        robot_is_stop = True

    elif movement == "left":
        rospy.loginfo("turn left")
        move_msg.angular.z = 2.5*robot_speed
        move_msg.linear.x = 0.0
        robot_is_stop = False

    elif movement == "right":
        rospy.loginfo("turn right")
        move_msg.angular.z = -2.5*robot_speed
        move_msg.linear.x = 0.0
        robot_is_stop = False

    elif movement == "forward":
        rospy.loginfo("forward")
        move_msg.angular.z = 0.0
        move_msg.linear.x = 1.2*robot_speed
        robot_is_stop = False

    elif movement == "backward":
        rospy.loginfo("backward")
        move_msg.angular.z = 0.0
        move_msg.linear.x = -0.5*robot_speed
        robot_is_stop = False

    movement_pub.publish(move_msg)


def battery_callback(msg):
    global send_bytes
    remaining_electricity = msg.battery
    rospy.loginfo(msg.battery)

    xrJson = {
        "version": "b0.0",
        "keep_alive": True,
        "url": "/xrrobot/battery",
        "method": "post",
        "data": {"remaining_electricity": float(remaining_electricity)},
    }

    send_bytes.append(json.dumps(xrJson).encode("utf-8"))


send_bytes = []

robot_speed = 1.5

servos = [0.0 for i in range(6)]

robot_thread = threading.Thread(target=send_msg)

battery_msg = Battery()
POWER_SUB = rospy.Subscriber('battery', Battery, battery_callback)

servo = JointState()
servo.name = ['a', 'b', 'c', 'd', 'x', 'y']
servo_pub = rospy.Publisher('joint_states', JointState, queue_size=10)
movement_pub = rospy.Publisher('cmd_vel', Twist, queue_size=0)

rospy.init_node('robot_status_interaction')

rospy.loginfo('robot_status_interaction node is running!')

app_is_run = True
robot_is_stop = True
servos_is_update = False
robot_thread.start()

rospy.spin()

app_is_run = False
robot_thread.join()
