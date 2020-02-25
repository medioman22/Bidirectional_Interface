# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 10:13:59 2019

@author: hkohli
"""

import time
import serial
import sys,os
import signal


LOWEST_INTENSITY_GLOVE = 30
HIGHEST_INTENSITY_GLOVE = 99

LOWEST_INTENSITY_BRACELET = 40
HIGHEST_INTENSITY_BRACELET = 220
correction_factor = 0.7

information_dict = {}
information_dict["max_distance_error"] = 4


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

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial('COM6', 9600) #COMx correspond to the bluetooth port that is used by the RN42 bluetooth transmitter (15-16 on alienware)

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

def sendIntensitiesToBracelet():
    intensityValues1 = bytearray([ord('S'), intensitiesMotorsBracelet[1][0], intensitiesMotorsBracelet[1][1], intensitiesMotorsBracelet[1][2], intensitiesMotorsBracelet[1][3], ord('E')])
    ser.write(intensityValues1)

def sendIntensities(intens1, intens2, intens3, intens4):
    intensityValues = bytearray([ord('S'), intens1, intens2, intens3, intens4, ord('E')])
    ser.write(intensityValues)


def getMotorIntensity( error, max_error, key_motor):
    if abs(error) < 0.1*max_error : error = 0
#    if haptic_device == BRACELETS : 
    if key_motor == "front" or key_motor == "back" :
        highest_intensity = HIGHEST_INTENSITY_BRACELET
        lowest_intensity = HIGHEST_INTENSITY_BRACELET- (1-correction_factor)*(HIGHEST_INTENSITY_BRACELET-LOWEST_INTENSITY_BRACELET)
    elif key_motor == "left" or key_motor == "right":
        highest_intensity = LOWEST_INTENSITY_BRACELET + correction_factor *  (HIGHEST_INTENSITY_BRACELET-LOWEST_INTENSITY_BRACELET)       
        lowest_intensity = LOWEST_INTENSITY_BRACELET
    else:
        highest_intensity = HIGHEST_INTENSITY_BRACELET
        lowest_intensity = LOWEST_INTENSITY_BRACELET
#    elif haptic_device == GLOVE :
#        highest_intensity = HIGHEST_INTENSITY_GLOVE
#        lowest_intensity = LOWEST_INTENSITY_GLOVE
    
    motor_intensity = abs(error*(highest_intensity - lowest_intensity)/max_error) + lowest_intensity
    if motor_intensity <= lowest_intensity: motor_intensity = 0
    if motor_intensity >= highest_intensity: motor_intensity = highest_intensity
    return round(motor_intensity)
    
def turnOnMotors(list_of_motors, error, max_error):
    for key in list_of_motors:
        intensitiesMotorsBracelet[motorsIndexesBracelet[key][0]] [motorsIndexesBracelet[key][1]] = getMotorIntensity(error, max_error, key)
    sendIntensitiesToBracelet()    

intens = 100

print("sending intensities")

def signal_handler(sig, frame):
    sendIntensities( 0, 0, 0, 0)
    time.sleep(0.5)
    ser.close()
    print('You pressed Ctrl+C!')
    sys.exit(0)
  
correction = 0.7
max_intens = 255
min_intens = 40
        
signal.signal(signal.SIGINT, signal_handler)

def main():
    i = -8
    j = 8
    while i<8:
        sendDirectionalCue([i,0,j])
        j-=0.5
        i+=0.5
        time.sleep(1)
        sendIntensities( 0, 0, 0, 0) 
        time.sleep(0.1)


main()   
sendIntensities( 0, 0, 0, 0) 
ser.close()    