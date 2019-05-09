#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import time, msvcrt
import json, csv
import sys
import os

# either 1 or 2
# 1: timing experiment
# 2: detection experiment
EXPERIMENT = 1
SUBJECT_NAME = "Sepand"

DISTANCE_THRESHOLD = 0.5
MOTOR_INPUT = 80
N_TEST = 3

with_connection = True  

if with_connection:
    print("Establishing the connection to the BBG device...")
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

motorsIndexes = {  "frontObstacle" : 4,
                    "backObstacle" : 3,
                    "upObstacle" : 9,
                    "downObstacle" : 1,
                    "leftObstacle" : 0,
                    "rightObstacle" : 5 }
motor_list = [0,1,3,4,5,9]


# timing experiment
if EXPERIMENT == 1:
    # array containing the reaction times
    times = []

    for i in range(N_TEST):
        motor = random.choice(motor_list)
        # sleep a certain amount of time (randomized)
        time.sleep(random.uniform(0.200,5))

        c.sendMessages([json.dumps({"dim":  motor, "value": MOTOR_INPUT, "type": "Set", "name": I2C_interface})])
        beg = time.time()

        # wait the key pressing
        key = msvcrt.getch()

        elapsed = time.time() - beg
        times.append(elapsed)

        c.sendMessages([json.dumps({"dim":  motor, "value": 0, "type": "Set", "name": I2C_interface})])
        print("Finished run", i+1, "over", N_TEST)
    
    with open("results_1/results_"+SUBJECT_NAME+".csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(times)

    # to make time to the queries for stopping the motors to arrive
    time.sleep(3)

# detection experiment
elif EXPERIMENT == 2:
    print("dessu")

else:
    print("Not a valid experiment")
    exit(0)


