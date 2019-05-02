#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket, struct
import select
import time
import json
import sys
import os

DISTANCE_THRESHOLD = 0.5
MAXIMUM_MOTOR_INPUT = 99
with_connection = True
if with_connection:
    print("Establishing the connection to the BBG device...")
else:
    print("Ignoring the connection...")


if with_connection:
    sys.path.insert(1, os.path.join(sys.path[0], '../Interface/src'))
    from connections.beagleboneGreenWirelessConnection import BeagleboneGreenWirelessConnection

    ######## Setup BBG connection #######
    c = BeagleboneGreenWirelessConnection()
    I2C_interface = "PCA9685@I2C[1]"
    c.connect()
    print('Status: {}'.format(c.getState()))
    c.sendMessages([json.dumps({"type": "Settings", "name": I2C_interface, "dutyFrequency": '50 Hz'})])
    time.sleep(3)
    c.sendMessages([json.dumps({"type": "Settings", "name": I2C_interface, "scan": False})])
    #####################################

############# setup UDP communication #############
# function to get the data from Unity
def get_data(my_socket):
    data = []
    # read data as long as packets are coming
    data_ready = False
    data_ready = select.select([my_socket],[],[],0)[0]
    
    while data_ready:
        t, _ = my_socket.recvfrom(1024) # buffer size is 1024 bytes
        data.append(t)
        data_ready = False
        data_ready = select.select([my_socket],[],[],0)[0]
    return data 

# local IP. Do not change that
UDP_IP = "127.0.0.1"
# socket to which data is being received
UDP_PORT_DISTANCES = 8051
# open the receiving socket
distances_socket = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
distances_socket.bind((UDP_IP, UDP_PORT_DISTANCES))
##################################################


distances_dict = {  "frontObstacle" : 0,
                    "backObstacle" : 0,
                    "upObstacle" : 0,
                    "downObstacle" : 0,
                    "leftObstacle" : 0,
                    "rightObstacle" : 0 }

motorsIndexes = {  "frontObstacle" : 0,
                    "backObstacle" : 9,
                    "upObstacle" : 1,
                    "downObstacle" : 3,
                    "leftObstacle" : 4,
                    "rightObstacle" : 5 }

def fillDict(current_data):
    distances_dict["frontObstacle"] = current_data[0]
    distances_dict["backObstacle"] = current_data[1]
    distances_dict["upObstacle"] = current_data[2]
    distances_dict["downObstacle"] = current_data[3]
    distances_dict["leftObstacle"] = current_data[4]
    distances_dict["rightObstacle"] = current_data[5]


# MAIN LOOP
while(True):
    distances = get_data(distances_socket)
    if len(distances):
        print("acquired distances, total number = ", len(distances))
        for packet in distances:
            # 6 floats
            strs = 'ffffff'
            # unpack.
            unpacked = struct.unpack(strs, packet)
            # parse the data
            fillDict(unpacked)
	
            for orientation in distances_dict.keys():
                if with_connection:
                    # if close enough to a wall
                    if (distances_dict[orientation] < DISTANCE_THRESHOLD):
                        # make the motors vibrate
                        value = distances_dict[orientation] * (-MAXIMUM_MOTOR_INPUT/DISTANCE_THRESHOLD) + MAXIMUM_MOTOR_INPUT # affine transformation
                        c.sendMessages([json.dumps({"dim":  motorsIndexes[orientation], "value": value, "type": "Set", "name": I2C_interface})])
                    else:
                        # reset motors
                        c.sendMessages([json.dumps({"dim":  motorsIndexes[orientation], "value": 0, "type": "Set", "name": I2C_interface})])
