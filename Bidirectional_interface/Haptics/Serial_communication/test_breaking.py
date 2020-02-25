# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 10:13:59 2019

@author: hkohli
"""

import time
import serial
import sys,os
import signal
import keyboard

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial('COM8', 9600) #COMx correspond to the bluetooth port that is used by the RN42 bluetooth transmitter (15-16 on alienware)

def sendIntensities(intens1, intens2, intens3, intens4):
    intensityValues = bytearray([ord('S'), intens1, intens2, intens3, intens4, ord('E')])
    ser.write(intensityValues)

intens = 100

print("sending intensities")

def signal_handler(sig, frame):
    sendIntensities( 0, 0, 0, 0)
    time.sleep(0.5)
    ser.close()
    print('You pressed Ctrl+C!')
    sys.exit(0)
  
        
signal.signal(signal.SIGINT, signal_handler)

def main():
    i = 0
    while i<10:
        sendIntensities( 0, intens, 0, intens)
        time.sleep(0.2)
        sendIntensities( 0, 0, 0, 0)
        time.sleep(0.1)
        sendIntensities( intens, 0, intens, 0)
        time.sleep(0.2)
        sendIntensities( 0, 0, 0, 0)
        time.sleep(0.5)
        i+=1

try:
    main()
except KeyboardInterrupt:
    print('Interrupted')
    try:
        sendIntensities( 0, 0, 0, 0)
        time.sleep(0.1)
        ser.close()
        sys.exit(0)
    except SystemExit:
        os._exit(0)
    
ser.close()    