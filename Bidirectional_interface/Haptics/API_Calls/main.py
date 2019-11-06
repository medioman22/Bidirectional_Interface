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
NB_OF_DRONES = 5

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

positions_dict = {}


motorsIndexes = {  "up" : 4,
                    "back" : 5,
                    "front" : 6,
                    "right" : 7,
                    "down" : 8,
                    "left" : 9 }

def fillDict(current_data):
    for i in range(0,NB_OF_DRONES):
        positions_dict[str(i)] = [current_data[i*3], current_data[i*3 + 1], current_data[i*3 + 2]]

# MAIN LOOP
while(True):
    distances = get_data(distances_socket)
    # had to sleep otherwise hardware overwhelmed
    time.sleep(0.05)
    if len(distances):
        print("acquired distances, total number = ", len(distances))

        # send only the last packet otherwise too many packets sent too fast
        packet = distances[-1]
        # 15 floats (5 drones and 3 positions each)
        strs = ''
        for i in range(0, NB_OF_DRONES):
            strs += 'fff'
        # unpack.
        posUnpacked = struct.unpack(strs, packet)
        # parse the data
        fillDict(posUnpacked)
        print(positions_dict)
#        for orientation in distances_dict.keys():
#            if with_connection:
#                # if close enough to a wall
#                if (distances_dict[orientation] < DISTANCE_THRESHOLD):
#                    if(distances_dict[opposites[orientation]] < DISTANCE_THRESHOLD):
#
#                        # take difference. Ignore if negative
#                        value = (distances_dict[orientation] * (-MAXIMUM_MOTOR_INPUT/DISTANCE_THRESHOLD) + MAXIMUM_MOTOR_INPUT) \
#                                    - (distances_dict[opposites[orientation]] * (-MAXIMUM_MOTOR_INPUT/DISTANCE_THRESHOLD) + MAXIMUM_MOTOR_INPUT)
#                        if (value < 0):
#                            continue
#                        else:
#                            c.sendMessages([json.dumps({"dim":  motorsIndexes[orientation], "value": value, "type": "Set", "name": I2C_interface})])
#
#                    else:
#                        # make the motors vibrate
#                        value = distances_dict[orientation] * (-MAXIMUM_MOTOR_INPUT/DISTANCE_THRESHOLD) + MAXIMUM_MOTOR_INPUT # affine transformation
#                        c.sendMessages([json.dumps({"dim":  motorsIndexes[orientation], "value": value, "type": "Set", "name": I2C_interface})])
#                else:
#                    # reset motors
#                    c.sendMessages([json.dumps({"dim":  motorsIndexes[orientation], "value": 0, "type": "Set", "name": I2C_interface})])
