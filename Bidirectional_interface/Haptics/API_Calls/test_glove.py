# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 16:56:45 2019

@author: hkohli
"""
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

motorsIndexes = {  "up" : 4,
                    "back" : 5,
                    "front" : 6,
                    "right" : 7,
                    "down" : 8,
                    "left" : 9, 
                    "extensionLeft" : 9,
                    "extensionRight" : 7}


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


for key in motorsIndexes :
    c.sendMessages([json.dumps({"dim":  motorsIndexes[key], "value": 90, "type": "Set", "name": I2C_interface})])
    time.sleep(1)
    c.sendMessages([json.dumps({"dim":  motorsIndexes[key], "value": 0, "type": "Set", "name": I2C_interface})])
    time.sleep(0.5)