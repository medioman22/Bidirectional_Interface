#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket, struct
import select
import time
import json
import sys
import os
import numpy as np

DISTANCE_THRESHOLD = 0.5
MAXIMUM_MOTOR_INPUT = 99
with_connection = True
NB_OF_DRONES = 5
NB_OF_INFORMATION = 8
DESIRED_HEIGHT = 1.0
LOWEST_INTENSITY = 40
HIGHEST_INTENSITY = 99
MAX_ERROR = DESIRED_HEIGHT
MARGIN = 0.1

LANDED = 0
TAKING_OFF = 1
REACHING_HEIGHT = 2
FLYING = 3
LANDING  = 4;

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
positions_socket = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
positions_socket.bind((UDP_IP, UDP_PORT_DISTANCES))
##################################################

positions_dict = {}

information_dict = {}

motorsIndexes = {  "up" : 4,
                    "downback" : 5,
                    "upfront" : 6,
                    "right" : 7,
                    "down" : 8,
                    "left" : 9 }

def sendHeightFeedback(current_height):
    height_error = current_height - DESIRED_HEIGHT
    intensity = abs(height_error * (HIGHEST_INTENSITY-LOWEST_INTENSITY)/MAX_ERROR)+LOWEST_INTENSITY
    if intensity < LOWEST_INTENSITY: intensity = 0
    if intensity > HIGHEST_INTENSITY: intensity = HIGHEST_INTENSITY
    
    if height_error < -MARGIN :
        if height_error < -DESIRED_HEIGHT/2:
            c.sendMessages([json.dumps({"dim":  motorsIndexes["up"], "value": intensity, "type": "Set", "name": I2C_interface})])
            c.sendMessages([json.dumps({"dim":  motorsIndexes["upfront"], "value": intensity, "type": "Set", "name": I2C_interface})])
        else : 
            c.sendMessages([json.dumps({"dim":  motorsIndexes["up"], "value": intensity, "type": "Set", "name": I2C_interface})])
            c.sendMessages([json.dumps({"dim":  motorsIndexes["upfront"], "value": 0, "type": "Set", "name": I2C_interface})])
    elif height_error > MARGIN :
        if height_error > DESIRED_HEIGHT/2:
            c.sendMessages([json.dumps({"dim":  motorsIndexes["down"], "value": intensity, "type": "Set", "name": I2C_interface})])
            c.sendMessages([json.dumps({"dim":  motorsIndexes["downback"], "value": intensity, "type": "Set", "name": I2C_interface})])
        else : 
            c.sendMessages([json.dumps({"dim":  motorsIndexes["down"], "value": intensity, "type": "Set", "name": I2C_interface})])
            c.sendMessages([json.dumps({"dim":  motorsIndexes["downback"], "value": 0, "type": "Set", "name": I2C_interface})])
    else :
        c.sendMessages([json.dumps({"dim":  motorsIndexes["down"], "value": 0, "type": "Set", "name": I2C_interface})])
        c.sendMessages([json.dumps({"dim":  motorsIndexes["up"], "value": 0, "type": "Set", "name": I2C_interface})])
        
def calculateMaxRadius(positionList):
    maxRadius = 0.0
    CoG = averagePosition(positionList)
    horizCoG = np.array([CoG[0],CoG[2]])
    for position in positionList:
        horizPos = np.array([position[0], position[2]])
        radius = np.linalg.norm(horizPos - horizCoG)
        if radius > maxRadius : maxRadius = radius
    return maxRadius

def calculateDistCoGWaypoint(positionList, waypointPos):
    CoG = averagePosition(positionList)
    return objectPos - CoG

    
        
        
        
            
def fillInfoDict(current_data):
    i = 0
    information_dict["height_error"] = current_data[i]
    i+=1
    information_dict["max_radius"] = current_data[i]
    i+=1
    information_dict["next_waypoint_direction"] = [current_data[i], current_data[i+1], current_data[i+2]]
    i+=3
    information_dict["pilot_direction"] = [current_data[i], current_data[i+1], current_data[i+2]]

def fillPositionsDict(current_data):
    global droneState
    for i in range(0,NB_OF_DRONES):
        positions_dict[str(i+1)] = [current_data[i*3], current_data[i*3 + 1], current_data[i*3 + 2]]
    droneState = int(current_data[NB_OF_DRONES])
    
    
    
def averageHeight(positionList):
    positionList = list(positions_dict.values())
    height = []
    for position in positionList:
        height.append(position[1]) 
    return sum(height)/len(height)

def averagePosition(positionList):
    CoG = [0,0,0]
    for position in positionList:
        for i in range(0,3):
            CoG[i] = position[i]
    return [x /len(positionList)  for x in CoG]




# MAIN LOOP
while(True):
    positions = get_data(positions_socket)
    # had to sleep otherwise hardware overwhelmed
    time.sleep(0.05)
    if len(positions):
        print("acquired positions, total number = ", len(positions))

        # send only the last packet otherwise too many packets sent too fast
        packet = positions[-1]
        
        strs = 'f'
        # 15 floats (5 drones and 3 positions each) + 1 for dronestate
        for i in range(0, NB_OF_DRONES):
                strs += 'fff'
#        for i in range(0, NB_OF_INFORMATION):
#            strs += 'f'
        # unpack.
        posUnpacked = struct.unpack(strs, packet)
        # parse the data
        fillPositionsDict(posUnpacked)
        positionList = list(positions_dict.values())
#        fillInfoDict(infoUnpacked)
#        print(positions_dict)
#        print(droneState)
        averageHeight = averageHeight(positionList)
        maxRadius = calculateMaxRadius(positionList)
        print(maxRadius)
#        sendHeightFeedback(averageHeight)   
#        print(CoG)
#        for orientation in positions_dict.keys():
#            if with_connection:
#                # if close enough to a wall
#                if (positions_dict[orientation] < DISTANCE_THRESHOLD):
#                    if(positions_dict[opposites[orientation]] < DISTANCE_THRESHOLD):
#
#                        # take difference. Ignore if negative
#                        value = (positions_dict[orientation] * (-MAXIMUM_MOTOR_INPUT/DISTANCE_THRESHOLD) + MAXIMUM_MOTOR_INPUT) \
#                                    - (positions_dict[opposites[orientation]] * (-MAXIMUM_MOTOR_INPUT/DISTANCE_THRESHOLD) + MAXIMUM_MOTOR_INPUT)
#                        if (value < 0):
#                            continue
#                        else:
#                            c.sendMessages([json.dumps({"dim":  motorsIndexes[orientation], "value": value, "type": "Set", "name": I2C_interface})])
#
#                    else:
#                        # make the motors vibrate
#                        value = positions_dict[orientation] * (-MAXIMUM_MOTOR_INPUT/DISTANCE_THRESHOLD) + MAXIMUM_MOTOR_INPUT # affine transformation
#                        c.sendMessages([json.dumps({"dim":  motorsIndexes[orientation], "value": value, "type": "Set", "name": I2C_interface})])
#                else:
#                    # reset motors
#                    c.sendMessages([json.dumps({"dim":  motorsIndexes[orientation], "value": 0, "type": "Set", "name": I2C_interface})])
