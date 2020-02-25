# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 10:33:57 2019

@author: Hugo
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json
import sys
import os


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
time.sleep(3)
c.sendMessages([json.dumps({"type": "Settings", "name": I2C_interface, "dutyFrequency": '50 Hz'})])

    
start_time = time.time();    
    
# MAIN LOOP
for key in motorsIndexes:
    # had to sleep otherwise hardware overwhelmed
    c.sendMessages([json.dumps({"dim":  motorsIndexes[key], "value": 80, "type": "Set", "name": I2C_interface})])
    time.sleep(0.2)
    c.sendMessages([json.dumps({"dim":  motorsIndexes[key], "value": 00, "type": "Set", "name": I2C_interface})])
    time.sleep(0.2)
