#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import serial
import time

print("hello")

arduinoData = serial.Serial('com9', 9600)

while(True):
    arduinoData.write(2)
    time.sleep(1)