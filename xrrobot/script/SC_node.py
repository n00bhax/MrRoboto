#!/usr/bin/env python
#coding=utf-8

import time
import threading
import socket
import json
import uuid
import copy

import rospy
from riki_msgs.msg import Speed_compensation


def sc_callback(msg):
    """SC_SUB callback"""

    global slave_alive_verification
    global app_is_begin

    if speed_is_init:
        try:
            SLAVE_SCC.k = msg.k
            SLAVE_SCC.scc = msg.scc
            sc_data = {'scc': SLAVE_SCC.scc, 'k': SLAVE_SCC.k}
            # rospy.loginfo('get data')

            with open(sc_json_url, "w") as f:
                json.dump(sc_data, f)
                slave_alive_verification = str(time.time())
                # rospy.loginfo("get!!  " + slave_alive_verification)

        except Exception:
            pass

    else:
        app_is_begin = True
        rospy.loginfo('app is begin')


def master_data_read():
    """read master sc data"""
    """sock msg form(json): {'k':'xx', 'scc':'xxx'}"""

    while app_is_run:

        j = i + 0
        # print(app_is_run)
        try:
            SC_SOCK_RECVE.connect(serverIP)
            SC_SOCK_RECVE.settimeout(3)
        except  Exception:
            continue

        try:
            sec = time.time()

            while app_is_run:

                # read sc data
                xrJson = {
                    "version": "b0.0",
                    "keep_alive": True,
                    "url": "/sc",
                    "method": "get",
                    "data": {},
                }

                tem_data = json.dumps(xrJson).encode("utf-8")
                
                # try to process data 
                try:
                    SC_SOCK_RECVE.send(tem_data)
                    data_raw = SC_SOCK_RECVE.recv(200)

                    js_response = json.loads(data_raw)

                    # print(data)

                    # Authentication and data check
                    if "data" in js_response:
                        data = js_response["data"]

                        if 'sc' in data:

                            # try data conversion and publish data
                            try:

                                Sc_msg = Speed_compensation()
                                if 'k' in data:
                                    Sc_msg.k = int(data['k'])
                                else:
                                    Sc_msg.k = SLAVE_SCC.k

                                Sc_msg.scc = int(data['sc'])
                                # print (Sc_msg)

                                SC_PUB.publish(Sc_msg)

                            except ValueError:
                                continue

                except socket.error:
                    break
                except ValueError:
                    continue

                if (time.time() - sec) > 0.5:
                    slave_data = {
                        "sc": SLAVE_SCC.scc,
                        "k": SLAVE_SCC.k,
                        "sc_slave_is_alive": slave_is_alive,
                        "is_update": True
                    }

                    # post sc data
                    xrJson = {
                        "version": "b0.0",
                        "keep_alive": True,
                        "url": "/sc",
                        "method": "post",
                        "data": slave_data,
                    }

                    tem_data = json.dumps(xrJson).encode("utf-8")
                    SC_SOCK_RECVE.send(tem_data)

                    data_raw = SC_SOCK_RECVE.recv(200)
                    sec = time.time()

                time.sleep(0.1)
                # rospy.loginfo(sec)

        except KeyboardInterrupt:
            
            # close connection
            SC_SOCK_RECVE.close()
            break


def slave_alive_verify():

    global last_slave_alive_verification
    global slave_is_alive

    while app_is_run:

        try:
        
            if last_slave_alive_verification == slave_alive_verification:
                slave_is_alive = False
            else:
                slave_is_alive = True
                rospy.loginfo('last_slave_alive_verification:%s' % last_slave_alive_verification)
                rospy.loginfo('slave_alive_verification:%s' % slave_alive_verification)
            
            rospy.loginfo('slave_is_alive:%d' % slave_is_alive)

            last_slave_alive_verification = copy.deepcopy(slave_alive_verification)
            
            time.sleep(1)
        
        except KeyboardInterrupt:
            break


def close_app():

    print("over")
    global app_is_run
    app_is_run = False
    rospy.signal_shutdown("sc stop")
    time.sleep(0.1)
    # SC_SOCK_RECV.close()
    # SC_SOCK_SEND.close()
    # time.sleep(0.1)


lock = threading.Lock()

SC_SOCK_RECVE = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SC_SOCK_RECVE.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

MASTER_SOCKS = [threading.Thread(target=master_data_read)]
MASTER_SOCKS += [threading.Thread(target=slave_alive_verify)]

SLAVE_SCC = Speed_compensation()
speed_is_init = False
# serverIP = ("192.168.3.116", 11322)
serverIP = ("127.0.0.1", 11322)


SC_SUB = rospy.Subscriber('SC_slave', Speed_compensation, sc_callback)
SC_PUB = rospy.Publisher('SC_master', Speed_compensation, queue_size=10)
sc_json_url = "/home/xrrobot/catkin_ws/src/xrrobot_project/xrrobot/param/sc/sc.json"

app_is_begin = False
app_is_run = True
slave_is_alive = False
slave_alive_verification = str(time.time())
last_slave_alive_verification = copy.deepcopy(slave_alive_verification)

with open(sc_json_url, 'r') as f:
    try:
        print(f)
        h_scc = json.load(f)
        print(h_scc)
        SLAVE_SCC.k = h_scc['k']
        SLAVE_SCC.scc = h_scc['scc']
    except Exception as e:
        print("sc json read error", e)
        SLAVE_SCC.k = 100
        SLAVE_SCC.scc = 0

rospy.init_node('speed_compensation')

rospy.loginfo('sc node is running!')

i = 0
for sock in MASTER_SOCKS:
    i += 1
    print(i)
    sock.start()

i = 0
while app_is_run:
    try:
        if app_is_begin:
            SC_PUB.publish(SLAVE_SCC)
            i += 1
        rospy.loginfo("speed_isn't init")
        time.sleep(0.2)
        if i > 10:
            speed_is_init = True
            rospy.loginfo('speed_is_init')
            break

    except KeyboardInterrupt:
        break

rospy.spin()

app_is_run = False

for sock in MASTER_SOCKS:
    sock.join()
SC_SOCK_RECVE.close()



