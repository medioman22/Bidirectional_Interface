#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial('COM15', 9600) #COMx correspond to the bluetooth port that is used by the RN42 bluetooth transmitter (15-16 on alienware)

def sendIntensities(intens1, intens2, intens3, intens4):
    intensityValues = bytearray([ord('S'), intens1, intens2, intens3, intens4, ord('E')])
    ser.write(intensityValues)

intens = 0

while True :
    sendIntensities( intens, 0, 0, 0)
    time.sleep(0.1)
    intens+=1;
    if intens >= 200.:
        intens = 0
