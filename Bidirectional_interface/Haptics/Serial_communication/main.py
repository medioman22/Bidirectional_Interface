#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial('COM12', 9600) #COMx correspond to the bluetooth port that is used by the RN42 bluetooth transmitter (15-16 on alienware)

def sendIntensities(intens1, intens2, intens3, intens4):
    intensityValues = bytearray([ord('S'), intens1, intens2, intens3, intens4, ord('E')])
    ser.write(intensityValues)

intens = 100

print("sending intensities")
while True :
    sendIntensities( 0, intens, 0, intens)
    time.sleep(0.2)
    sendIntensities( 0, 0, 0, 0)
    time.sleep(0.1)
    sendIntensities( intens, 0, intens, 0)
    time.sleep(0.2)
    sendIntensities( 0, 0, 0, 0)
    time.sleep(0.5)