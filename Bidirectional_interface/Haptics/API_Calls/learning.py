# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:44:18 2019

@author: hkohli
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json
import sys
import os
import serial
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import threading
import mouse
import yaml
import signal

DISTANCE_THRESHOLD = 0.5
MAXIMUM_MOTOR_INPUT = 99
with_connection = True
NB_OF_DRONES = 5
NB_OF_INFORMATION = 10
DESIRED_HEIGHT = 1.0
LOWEST_INTENSITY_GLOVE = 30
HIGHEST_INTENSITY_GLOVE = 99

LOWEST_INTENSITY_BRACELET = 40
HIGHEST_INTENSITY_BRACELET = 250


MARGIN = 0.1

REACHING_HEIGHT = 2;
GO_TO_FIRST_WAYPOINT = 5;
EXTENSION = 6;
WAYPOINT_NAV = 7;
CONTRACTION = 8;

GLOVE = "Glove"
BRACELETS = "Bracelets"

positions_dict = {}

information_dict = {}
allIndexes = ["up", "back", "right", "front", "left", "down"]

motorsIndexes = {  "up" : 4,
                    "down" : 8,
                    "back" : 5,
                    "front" : 6,
                    "right" : 7,
                    "left" : 9, 
                    "extensionRight" : 7,
                    "extensionLeft" : 9
                    }

#The first number defines the bracelet, the second the motor(s)
motorsIndexesBracelet = {"up" : [2,0],
                    "down" : [2,2],
                    "back" : [1,0],
                    "front" : [1,2],
                    "right" : [1,3],
                    "left" : [1,1],
                    "extensionRight" : [2,3],
                    "extensionLeft" : [2,1]
        }


intensitiesMotorsBracelet = {1 : [0,0,0,0], 2 : [0,0,0,0]}
I2C_interface = ""

#haptic_device = BRACELETS
    
##Setup communication with glove (and BBGW)
def connect():
    global ser, c, I2C_interface
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
    elif haptic_device == BRACELETS : 
        get_bracelet_param()

def get_bracelet_param():
    global HIGHEST_INTENSITY_BRACELET, LOWEST_INTENSITY_BRACELET, correction_factor, ser
    with open(r'param_bracelets.yaml') as file:
        param_bracelets = yaml.load(file, Loader=yaml.FullLoader)
        correction_factor = param_bracelets['correction_factor']
        LOWEST_INTENSITY_BRACELET = param_bracelets["lowest_intensity"]
        HIGHEST_INTENSITY_BRACELET = param_bracelets["highest_intensity"]
        ser = [serial.Serial('COM' + str(param_bracelets['COM']['arm']), 9600) , serial.Serial('COM' +  str(param_bracelets['COM']['forearm']), 9600)]    
        
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
    global HIGHEST_INTENSITY_BRACELET, LOWEST_INTENSITY_BRACELET
    if abs(error) < 0.1*max_error : error = 0
    if haptic_device == BRACELETS : 
        if key_motor == "front" or key_motor == "back" or key_motor == "up" or key_motor == "down" :
            highest_intensity = HIGHEST_INTENSITY_BRACELET
            lowest_intensity = HIGHEST_INTENSITY_BRACELET- (1-correction_factor)*(HIGHEST_INTENSITY_BRACELET-LOWEST_INTENSITY_BRACELET)
        elif key_motor == "left" or key_motor == "right":
            highest_intensity =  + correction_factor *  (HIGHEST_INTENSITY_BRACELET-LOWEST_INTENSITY_BRACELET)       
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

    
def sendCueThread():
    global direction, intensity 
    error_distance = 2
    max_error_distance = 4

    extension_error = 0.5
    max_extension_error = 1
    
    while(True):
        print(direction)
        shutDownAllMotors()
        if direction != "extend" and direction != "contract" and direction !="" :
            turnOnMotors([direction], error_distance, max_error_distance)
            time.sleep(0.3)
            turnOnMotors([direction], 0, max_error_distance)
        elif direction == 'extend':
            print("Tryng to send extend cue")
            turnOnMotors(["up"], extension_error, max_extension_error)
            time.sleep(3/10)
            turnOnMotors(["up"], 0,max_extension_error)
            turnOnMotors(["extensionLeft", "extensionRight"], extension_error, max_extension_error)
            time.sleep(3/10)
            turnOnMotors(["extensionLeft", "extensionRight"], 0, max_extension_error)
        elif direction == 'contract':
            turnOnMotors(["extensionLeft", "extensionRight"], extension_error, max_extension_error)
            time.sleep(3/10)
            turnOnMotors(["extensionLeft", "extensionRight"], 0, max_extension_error)
            turnOnMotors(["up"], extension_error, max_extension_error)
            time.sleep(3/10)
            turnOnMotors(["up"], 0, max_extension_error) 
        else :
            shutDownAllMotors()
        time.sleep(1)
    
def comboCallback(event):
    global haptic_device
    haptic_device =str(comboDevice.get())
     #connect to the chosen haptic_device       
    next_img()
    comboDevice.destroy()
    #btn.pack()
    connect()
    t = threading.Thread(name = "sendCue", target = sendCueThread)
    t.start()

def next_img():
    global intensity
    # load the image and display it
    global direction
    try:
        img = next(images)  # get the next image from the iterator
        direction = img
        img = Image.open(folder + img+extension)
        img = ImageTk.PhotoImage(img)
        panel.img = img  
        # keep a reference so it's not garbage collected
        panel['image'] = img   
    except StopIteration:
#        btn.destroy()
        shutDownAllMotors()
        intensity = 0;
        return  # if there are no more images, do nothing
       

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
    win.destroy()
        
signal.signal(signal.SIGINT, signal_handler)   
    
def on_closing():
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
    win.destroy()


#for the training, the intensity is 2/3 of the max power


win = tk.Tk()
win.geometry('1000x1000')  # set window size
win.resizable(0, 0)  # fix window

panel = tk.Label(win)
panel.pack()
folder = "experiment_pictures/"
images = ['up', 'down', 'left', 'right', 'front' , 'back', 'extend', 'contract']
extension = '.png'
images = iter(images)  # make an iterator

direction = ""

comboDevice = ttk.Combobox(win, 
                            values=[
                                    GLOVE, 
                                    BRACELETS])
    
connect_to_device = False



comboDevice.current()
comboDevice.pack()
comboDevice.bind("<<ComboboxSelected>>",comboCallback )


#btn = tk.Button(text='Next image', command=next_img)
mouse.on_right_click(next_img, args=())



# show the first image
#next_img()


win.protocol("WM_DELETE_WINDOW", on_closing)

win.mainloop()
