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


DISTANCE_THRESHOLD = 0.5
MAXIMUM_MOTOR_INPUT = 99
with_connection = True
NB_OF_DRONES = 5
NB_OF_INFORMATION = 10
DESIRED_HEIGHT = 1.0
LOWEST_INTENSITY_GLOVE = 30
HIGHEST_INTENSITY_GLOVE = 99

LOWEST_INTENSITY_BRACELET = 25
HIGHEST_INTENSITY_BRACELET = 220


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
haptic_device = GLOVE
    

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

        time.sleep(3)
        c.sendMessages([json.dumps({"type": "Settings", "name": I2C_interface, "scan": False})])
        c.sendMessages([json.dumps({"type": "Settings", "name": I2C_interface, "dutyFrequency": '50 Hz'})])
#        c.sendMessages([json.dumps({"type": "Settings", "name": I2C_interface, "Frequency": '100 Hz'})])
        #####################################
# configure the bluetooth serial connections 
elif haptic_device == BRACELET : 
    ser = [serial.Serial('COM15', 9600) ,serial.Serial('COM16', 9600)]#, serial.Serial('COM16', 9600)] #COMx correspond to the bluetooth port that is used by the RN42 bluetooth transmitter

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
motorsIndexesBracelet = {"up" : [2,2],
                    "down" : [2,0],
                    "back" : [1,0],
                    "front" : [1,2],
                    "right" : [1,3],
                    "left" : [1,1],
                    "extensionRight" : [2,3],
                    "extensionLeft" : [2,1]
        }


intensitiesMotorsBracelet = {1 : [0,0,0,0], 2 : [0,0,0,0]}


def shutDownAllMotors():
    turnOnMotors(allIndexes,0)
    
def turnOnMotors(list_of_motors, intensity):
    for key in motorsIndexes:
        if key in list_of_motors:
            
            if haptic_device == GLOVE: 
                if motorsIndexes[key] == 6 :  intensity *=0.65
                c.sendMessages([json.dumps({"dim":  motorsIndexes[key], "value": intensity, "type": "Set", "name": I2C_interface})])
#                time.sleep(0.005)
            elif haptic_device == BRACELET: 
                intensitiesMotorsBracelet[motorsIndexesBracelet[key][0]] [motorsIndexesBracelet[key][1]] = intensity
    if haptic_device == BRACELET:
        print("sending intensity")
        sendIntensitiesToBracelet()
            
def getMotorIntensity( error, max_error):
    if abs(error) < 0.1*max_error : error = 0
    if haptic_device == BRACELET : 
        highest_intensity = HIGHEST_INTENSITY_BRACELET
        lowest_intensity = LOWEST_INTENSITY_BRACELET
    elif haptic_device == GLOVE :
        highest_intensity = HIGHEST_INTENSITY_GLOVE
        lowest_intensity = LOWEST_INTENSITY_GLOVE
    motor_intensity = round(abs(error*(highest_intensity - lowest_intensity)/max_error) + lowest_intensity)
    if motor_intensity <= lowest_intensity: motor_intensity = 0
    if motor_intensity >= highest_intensity: motor_intensity = highest_intensity
    return motor_intensity


##Haptic feedback with bracelet 
def sendIntensitiesToBracelet():
    intensityValues1 = bytearray([ord('S'), intensitiesMotorsBracelet[1][0], intensitiesMotorsBracelet[1][1], intensitiesMotorsBracelet[1][2], intensitiesMotorsBracelet[1][3], ord('E')])
    intensityValues2 = bytearray([ord('S'), intensitiesMotorsBracelet[2][0], intensitiesMotorsBracelet[2][1], intensitiesMotorsBracelet[2][2], intensitiesMotorsBracelet[2][3], ord('E')])
    ser[0].write(intensityValues1)
    ser[1].write(intensityValues2)


    
print("Start scanning for information")
# MAIN LOOP

direction_dict = {}

if haptic_device == GLOVE:
    direction_dict = motorsIndexes
else :
    direction_dict = motorsIndexesBracelet

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
                                    "Glove", 
                                    "Bracelets"])

def sendCueThread():
    global direction
    intensity = getMotorIntensity(100,150)
    while(True):
        print(direction)
        shutDownAllMotors()
        if direction != "extend" and direction != "contract" :
            turnOnMotors([direction], intensity)
            time.sleep(2)
            turnOnMotors([direction], 0)
        elif direction == 'extend':
            print("Tryng to send extend cue")
            turnOnMotors(["up"], intensity)
            time.sleep(3/10)
            turnOnMotors(["up"], 0)
            turnOnMotors(["extensionLeft", "extensionRight"], intensity)
            time.sleep(3/10)
            turnOnMotors(["extensionLeft", "extensionRight"], 0)
        elif direction == 'contract':
            turnOnMotors(["extensionLeft", "extensionRight"], intensity)
            time.sleep(3/10)
            turnOnMotors(["extensionLeft", "extensionRight"], 0)
            turnOnMotors(["up"], intensity)
            time.sleep(3/10)
            turnOnMotors(["up"], 0) 
        else :
            shutDownAllMotors()
        time.sleep(1)
    
def comboCallback(event):
    print("Device chosen")
    next_img()
    comboDevice.destroy()
    btn.pack()
    t = threading.Thread(name = "sendCue", target = sendCueThread)
    t.start()
    

comboDevice.current()
comboDevice.pack()
comboDevice.bind("<<ComboboxSelected>>",comboCallback )


def next_img():
    # load the image and display it
    global direction
    try:
        img = next(images)  # get the next image from the iterator
    except StopIteration:
        return  # if there are no more images, do nothing
    direction = img
    img = Image.open(folder + img+extension)
    img = ImageTk.PhotoImage(img)
    panel.img = img  
    # keep a reference so it's not garbage collected
    panel['image'] = img
    
    

btn = tk.Button(text='Next image', command=next_img)

# show the first image
#next_img()


win.mainloop()

