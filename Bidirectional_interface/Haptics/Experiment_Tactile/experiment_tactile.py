#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
#####################################################################
#####################################################################
#####################################################################
###################### ONLY WORKS ON WINDOWS ########################
#####################################################################
#####################################################################
#####################################################################
import time, msvcrt
import json, csv
import sys
import os

# either 1 or 2
# 1: timing experiment
# 2: detection experiment
EXPERIMENT = 2
SUBJECT_NAME = "Matteo"

MOTOR_INPUT = 80
N_TEST = 10
with_connection = True

MEAN_TIME = 0.45
TIME_OFFSET = 3

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

motorsIndexes = {  4 : "frontObstacle",
                   3 : "backObstacle",
                   9 : "upObstacle",
                   1 : "downObstacle",
                   0 : "leftObstacle",
                   5 : "rightObstacle"}

motor_list = [0,1,3,4,5,9]

motor_mapping = {"w" : "frontObstacle",
                 "s" : "backObstacle",
                 "o" : "upObstacle",
                 "l" : "downObstacle",
                 "a" : "leftObstacle",
                 "d" : "rightObstacle"}


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
    sent_motor = []
    identified_motors = []

    for i in range(N_TEST):
        motor = random.choice(motor_list)
        sent_motor.append(motorsIndexes[motor])

        # just to put a difference between the runs
        time.sleep(2)

        c.sendMessages([json.dumps({"dim":  motor, "value": MOTOR_INPUT, "type": "Set", "name": I2C_interface})])
        time.sleep(MEAN_TIME)
        c.sendMessages([json.dumps({"dim":  motor, "value": 0, "type": "Set", "name": I2C_interface})])

        # added an offset
        # if key pressed within the time, outputs what has been pressed. Else
        # outputs a space.
        time.sleep(TIME_OFFSET)
        print("Timeout")
        if msvcrt.kbhit():
            key_pressed = msvcrt.getch().decode("utf-8")
            identified_motors.append(motor_mapping[key_pressed])
        else:
            identified_motors.append(" ")

        # just to put a difference between the runs
        time.sleep(1)
        print("Finished run", i+1, "over", N_TEST, " You answered : ", motor_mapping[key_pressed])

    with open("results_2/results_"+SUBJECT_NAME+".csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(sent_motor)
        wr.writerow(identified_motors)

    # to make time to the queries for stopping the motors to arrive
    time.sleep(3)

else:
    print("Not a valid experiment")
    exit(0)
