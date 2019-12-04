#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket, struct
import select
import time
import json
import sys
import os
import serial
import yaml
import signal
import keyboard

DISTANCE_THRESHOLD = 0.5
MAXIMUM_MOTOR_INPUT = 99
with_connection = True
NB_OF_DRONES = 5
NB_OF_INFORMATION = 11
DESIRED_HEIGHT = 1.0
LOWEST_INTENSITY_GLOVE = 30
HIGHEST_INTENSITY_GLOVE = 99

LOWEST_INTENSITY_BRACELET = 40
HIGHEST_INTENSITY_BRACELET = 220


MARGIN = 0.1

REACHING_HEIGHT = 2;
GO_TO_FIRST_WAYPOINT = 5;
EXTENSION = 6;
WAYPOINT_NAV = 7;
CONTRACTION = 8;

GLOVE ="glove"
BRACELETS = "bracelets"


emergency_stop = False;

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
information_socket = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
information_socket.bind((UDP_IP, UDP_PORT_DISTANCES))
##################################################
haptic_device = ''

information_dict = {}
allIndexes = ["up", "back", "right", "front", "left", "down"]

motorsIndexes = {  "up" : 4,
                    "back" : 5,
                    "front" : 6,
                    "right" : 7,
                    "down" : 8,
                    "left" : 9, 
                    "extensionLeft" : 9,
                    "extensionRight" : 7}

#The first number defines the bracelet, the second the motor(s)
motorsIndexesBracelet = {"up" : [2,0],
                    "back" : [1,0],
                    "front" : [1,2],
                    "right" : [1,3],
                    "down" : [2,2],
                    "left" : [1,1],
                    "extensionLeft" : [2,1],
                    "extensionRight" : [2,3]
        }

intensitiesMotorsBracelet = {1 : [0,0,0,0], 2 : [0,0,0,0]}

def sendHeightCue(error):
    if error < 0 :
        turnOnMotors(["up"], error, information_dict["max_height_error"])
        turnOnMotors(["down"], 0, information_dict["max_height_error"])
    else :
        turnOnMotors(["down"], error, information_dict["max_height_error"])
        turnOnMotors(["up"], 0, information_dict["max_height_error"])
    
#    turnOnMotors(["front","back"],0, information_dict["max_distance_error"])
#    turnOnMotors(["left", "right"], 0, information_dict["max_distance_error"])  

def sendDirectionalCue(distanceToWaypoint):
    x_distance = distanceToWaypoint[0]
    y_distance = distanceToWaypoint[2]
    send1DirectionalCue(x_distance, "front", "back")
    send1DirectionalCue(y_distance, "left", "right")    
#    turnOnMotors(["up","down"],0,information_dict["max_height_error"])

def send1DirectionalCue(distance, direction, negative_direction):
    if distance < 0:
        turnOnMotors([negative_direction], distance, information_dict["max_distance_error"])
        turnOnMotors([direction], 0, information_dict["max_distance_error"])
    elif distance > 0:
        turnOnMotors([direction], distance, information_dict["max_distance_error"])
        turnOnMotors([negative_direction], 0, information_dict["max_distance_error"])

def shutDownAllMotors():
    turnOnMotors(allIndexes,0,1)
    
       
def turnOnMotors(list_of_motors, error, max_error):
    global I2C_interface,c
    for key in list_of_motors:
        if haptic_device == GLOVE: 
#                if motorsIndexes[key] == 6 :  intensity *=0.65
            c.sendMessages([json.dumps({"dim":  motorsIndexes[key], "value": getMotorIntensity(error, max_error, ''), "type": "Set", "name": I2C_interface})])
#                time.sleep(0.005)
        elif haptic_device == BRACELETS:    
            intensitiesMotorsBracelet[motorsIndexesBracelet[key][0]] [motorsIndexesBracelet[key][1]] = getMotorIntensity(error, max_error, key)
    if haptic_device == BRACELETS: sendIntensitiesToBracelet()   
            

def getMotorIntensity( error, max_error, key_motor):
    if abs(error) < 0.1*max_error : error = 0
    if haptic_device == BRACELETS : 
        if key_motor == "front" or key_motor == "back" :
            highest_intensity = HIGHEST_INTENSITY_BRACELET
            lowest_intensity = HIGHEST_INTENSITY_BRACELET- (1-correction_factor)*(HIGHEST_INTENSITY_BRACELET-LOWEST_INTENSITY_BRACELET)
        elif key_motor == "left" or key_motor == "right":
            highest_intensity = LOWEST_INTENSITY_BRACELET + correction_factor *  (HIGHEST_INTENSITY_BRACELET-LOWEST_INTENSITY_BRACELET)       
            lowest_intensity = LOWEST_INTENSITY_BRACELET
        else:
            highest_intensity = HIGHEST_INTENSITY_BRACELET
            lowest_intensity = LOWEST_INTENSITY_BRACELET
    elif haptic_device == GLOVE :
        highest_intensity = HIGHEST_INTENSITY_GLOVE
        lowest_intensity = LOWEST_INTENSITY_GLOVE
    
    motor_intensity = abs(error*(highest_intensity - lowest_intensity)/max_error) + lowest_intensity
    if motor_intensity <= lowest_intensity: motor_intensity = 0
    if motor_intensity >= highest_intensity: motor_intensity = highest_intensity
    return round(motor_intensity)    

##Haptic feedback with bracelet 
def sendIntensitiesToBracelet():
    intensityValues1 = bytearray([ord('S'), intensitiesMotorsBracelet[1][0], intensitiesMotorsBracelet[1][1], intensitiesMotorsBracelet[1][2], intensitiesMotorsBracelet[1][3], ord('E')])
    intensityValues2 = bytearray([ord('S'), intensitiesMotorsBracelet[2][0], intensitiesMotorsBracelet[2][1], intensitiesMotorsBracelet[2][2], intensitiesMotorsBracelet[2][3], ord('E')])
    ser[0].write(intensityValues1)
    ser[1].write(intensityValues2)


def fillInfoDict(current_data):
    i = 0
    information_dict["height_error"] = current_data[i]
    i+=1
    information_dict["extension_error"] = current_data[i]
    i+=1
    information_dict["next_waypoint_direction"] = [current_data[i], current_data[i+1], current_data[i+2]]
    i+=3
    information_dict["experiment_state"] = round(current_data[i])
    i+=1
    information_dict["max_distance_error"] = current_data[i]
    i+=1
    information_dict["max_height_error"] = current_data[i]
    i+=1
    information_dict["max_extension_error"] = current_data[i]
    i+=1
    information_dict["emergency_stop"] = round(current_data[i])
    i+=1
    print(current_data[i])
    if round(current_data[i] == 0): device = "bracelets"
    else: device = "glove"
    
    information_dict["haptic_device"] = device
    
def connect_to_feedback_system():
    global ser, correction_factor, I2C_interface, c
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
    
            time.sleep(3)
            c.sendMessages([json.dumps({"type": "Settings", "name": I2C_interface, "scan": False})])
            c.sendMessages([json.dumps({"type": "Settings", "name": I2C_interface, "dutyFrequency": '50 Hz'})])
    #        c.sendMessages([json.dumps({"type": "Settings", "name": I2C_interface, "Frequency": '100 Hz'})])
            #####################################
    # configure the bluetooth serial connections 
    elif(haptic_device == BRACELETS) : 
        with open(r'com_port.yaml') as file:
            param_bracelets = yaml.load(file, Loader=yaml.FullLoader)
            correction_factor = param_bracelets['correction_factor']
        ser = [serial.Serial('COM' + str(param_bracelets['COM']['arm']), 9600) , serial.Serial('COM' +  str(param_bracelets['COM']['forearm']), 9600)]    
    
#Function to close the serial port if the application is shutdown
def signal_handler(sig, frame):
        
        try :
            print('Shutting down motors and exiting!')
            shutDownAllMotors()
            time.sleep(0.5)
            ser[0].close()
            ser[1].close()
            sys.exit(0)
        except :
            print("Connection not established")
            sys.exit(0)
        
signal.signal(signal.SIGINT, signal_handler)     
    
print("Start scanning for information")



information = get_data(information_socket)
while not len(information):
    information = get_data(information_socket)
    time.sleep(0.1)
    
if len(information):
    # send only the last packet otherwise too many packets sent too fast
    packet = information[-1]    
    strs = ''
    for i in range(0, NB_OF_INFORMATION):
        strs += 'f'
    # unpack.
    infoUnpacked = struct.unpack(strs, packet)
    # parse the data
    fillInfoDict(infoUnpacked)

print(information_dict)

haptic_device = information_dict["haptic_device"]
##Setup communication with glove (and BBGW)

connect_to_feedback_system()

# MAIN LOOP
while(True):
    information = get_data(information_socket)
    # had to sleep otherwise hardware overwhelmed
    time.sleep(0.05)
    if len(information):
        
        # send only the last packet otherwise too many packets sent too fast
        packet = information[-1]
        strs = ''
        for i in range(0, NB_OF_INFORMATION):
            strs += 'f'
        # unpack.
        infoUnpacked = struct.unpack(strs, packet)
        # parse the data
        fillInfoDict(infoUnpacked)

        print(information_dict)
  
        if information_dict["emergency_stop"] == 0:
            experiment_state = information_dict["experiment_state"]
            if experiment_state == EXTENSION or experiment_state == CONTRACTION:
                error = information_dict["extension_error"]
                motor_intensity = getMotorIntensity(error, information_dict["max_extension_error"])
                up_time = 3/10
                if error > 0 :
                    turnOnMotors(["up"], error, information_dict["max_extension_error"])
                    time.sleep(up_time)
                    turnOnMotors(["up"], 0,information_dict["max_extension_error"])
                    turnOnMotors(["extensionLeft", "extensionRight"], error, information_dict["max_extension_error"])
                    time.sleep(up_time)
                    turnOnMotors(["extensionLeft", "extensionRight"], 0,information_dict["max_extension_error"])
                else :
                    turnOnMotors(["extensionLeft", "extensionRight"], error, information_dict["max_extension_error"])
                    time.sleep(up_time)
                    turnOnMotors(["extensionLeft", "extensionRight"], 0,information_dict["max_extension_error"])
                    turnOnMotors(["up"], error, information_dict["max_extension_error"])
                    time.sleep(up_time)
                    turnOnMotors(["up"], 0,information_dict["max_extension_error"])
                time.sleep(0.5)
            elif experiment_state == GO_TO_FIRST_WAYPOINT or experiment_state == WAYPOINT_NAV:
                if abs( information_dict["height_error"]) > 0.1*information_dict["max_height_error"] : 
                    sendHeightCue(information_dict["height_error"])
                else:
                    sendDirectionalCue(information_dict["next_waypoint_direction"])
        else :
            shutDownAllMotors()
            ser[0].close()
            ser[1].close()
ser[0].close()
ser[1].close()