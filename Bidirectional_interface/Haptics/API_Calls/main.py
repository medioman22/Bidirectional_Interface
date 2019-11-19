#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket, struct
import select
import time
import json
import sys
import os
import serial
import numpy as np



DISTANCE_THRESHOLD = 0.5
MAXIMUM_MOTOR_INPUT = 99
with_connection = True
NB_OF_DRONES = 5
NB_OF_INFORMATION = 7
DESIRED_HEIGHT = 1.0
LOWEST_INTENSITY_GLOVE = 40
HIGHEST_INTENSITY_GLOVE = 99

LOWEST_INTENSITY_BRACELET = 32
HIGHEST_INTENSITY_BRACELET = 255

MAX_ERROR = DESIRED_HEIGHT
MAX_DISTANCE = 4.0
MAX_EXTENSION_ERROR = 1.0
MARGIN = 0.1

REACHING_HEIGHT = 2;
GO_TO_FIRST_WAYPOINT = 5;
EXTENSION = 6;
WAYPOINT_NAV = 7;
CONTRACTION = 8;

GLOVE = 10
BRACELET = 20


emergency_stop = False;
#
haptic_device = BRACELET

##Setup communication with glove (and BBGW)
if (haptic_device == GLOVE) :
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

# configure the bluetooth serial connections 
if haptic_device == BRACELET : 
    ser = serial.Serial('COM9', 9600) #COMx correspond to the bluetooth port that is used by the RN42 bluetooth transmitter


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

##Haptic feedback with glove :

def sendHeightCue(error, type_of_device):
    motor_intensity = getMotorIntensity(haptic_device, error, MAX_DISTANCE)
    
    if error < 0 :
        turnOnGloveMotors(["down"], motor_intensity)
    else :
        turnOnGloveMotors(["up"], motor_intensity)

def sendExtensionCue(error):
    motor_intensity = getMotorIntensity(haptic_device, error, MAX_EXTENSION_ERROR)

    if error < 0 :
        turnOnGloveMotors(["left", "right"], motor_intensity)
    else :
        turnOnGloveMotors(["up", "down"], motor_intensity)          

def sendDirectionalCue(distanceToWaypoint):
    x_distance = distanceToWaypoint[0]
    y_distance = distanceToWaypoint[2]
    send1DirectionalCue(x_distance, "right", "left")
    send1DirectionalCue(y_distance, "upfront", "downback")    
    
def send1DirectionalCue(distance, direction, negative_direction):
    motor_intensity = getMotorIntensity(haptic_device, distance, MAX_DISTANCE)
  
    if distance < - MARGIN:
        turnOnGloveMotors([negative_direction], motor_intensity)
    elif distance > MARGIN :
        turnOnGloveMotors([direction], motor_intensity)
    else:
       shutDownAllMotors()

def shutDownAllMotors():
    for key, motor in motorsIndexes.items() :
        c.sendMessages([json.dumps({"dim":  motor, "value": 0, "type": "Set", "name": I2C_interface})])
             
def turnOnGloveMotors(list_of_motors, intensity):
    for key in motorsIndexes:
        if key in list_of_motors:
            c.sendMessages([json.dumps({"dim":  motorsIndexes[key], "value": intensity, "type": "Set", "name": I2C_interface})])
        else:
            c.sendMessages([json.dumps({"dim":  motorsIndexes[key], "value": 0, "type": "Set", "name": I2C_interface})])
        

def turnOnBraceletMotors()

                
def getMotorIntensity(haptic_device, error, max_error):
    if haptic_device == BRACELET : 
        highest_intensity = HIGHEST_INTENSITY_BRACELET
        lowest_intensity = LOWEST_INTENSITY_BRACELET
    elif haptic_device == GLOVE :
        highest_intensity = HIGHEST_INTENSITY_GLOVE
        lowest_intensity = LOWEST_INTENSITY_GLOVE
        motor_intensity = abs(error*(highest_intensity - lowest_intensity)/max_error) + lowest_intensity
    if motor_intensity < lowest_intensity: motor_intensity = 0
    if motor_intensity > highest_intensity: motor_intensity = highest_intensity
    return motor_intensity


##Haptic feedback with bracelet 
def sendIntensitiesToBracelet(intens1, intens2, intens3, intens4):
    intensityValues = bytearray([ord('S'), intens1, intens2, intens3, intens4, ord('E')])
    ser.write(intensityValues)




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
    return waypointPos - CoG
       
        

    
def fillInfoDict(current_data):
    i = 0
    information_dict["height_error"] = current_data[i]
    i+=1
    information_dict["extension_error"] = current_data[i]
    i+=1
    information_dict["contraction_error"] = current_data[i]
    i+=1
    information_dict["next_waypoint_direction"] = [current_data[i], current_data[i+1], current_data[i+2]]
    i+=3
    information_dict["experiment_state"] = round(current_data[i])

    
    
    
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
        
        strs = ''
        # 15 floats (5 drones and 3 positions each) + 1 for dronestate
#        for i in range(0, NB_OF_DRONES):
#                strs += 'fff'
        for i in range(0, NB_OF_INFORMATION):
            strs += 'f'
        # unpack.
        infoUnpacked = struct.unpack(strs, packet)
        # parse the data
        #fillPositionsDict(posUnpacked)
        #positionList = list(positions_dict.values())
        fillInfoDict(infoUnpacked)

        print(information_dict)
        
        experiment_state = information_dict["experiment_state"]
        if experiment_state == REACHING_HEIGHT:
            sendHeightCue(information_dict["height_error"])
        elif experiment_state == GO_TO_FIRST_WAYPOINT:
            sendDirectionalCue(information_dict["next_waypoint_direction"])
#            sendHeightCue(information_dict["height_error"])
        elif experiment_state == EXTENSION:
            sendExtensionCue(information_dict["extension_error"])
        elif experiment_state == WAYPOINT_NAV:
            sendDirectionalCue(information_dict["next_waypoint_direction"])
#            sendHeightCue(information_dict["height_error"])            
        elif experiment_state == CONTRACTION:
            sendExtensionCue(information_dict["contraction_error"])
        else :
            shutDownAllMotors()
    
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
