#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial('COM9', 9600) #COMx correspond to the bluetooth port that is used by the RN42 bluetooth transmitter

def sendIntensities(intens1, intens2, intens3, intens4):
    intensityValues = bytearray([ord('S'), intens1, intens2, intens3, intens4, ord('E')])
    ser.write(intensityValues)

intens = 100

while True :
    sendIntensities( 0, intens, 0, 0)
    time.sleep(0.5)
    sendIntensities(0,0, 0, 0)
    time.sleep(2)
    print("Sent")