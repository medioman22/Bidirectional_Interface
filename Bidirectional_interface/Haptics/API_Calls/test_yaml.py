# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 19:25:27 2019

@author: hkohli
"""
import yaml

with open(r'com_port.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    COM_number = yaml.load(file, Loader=yaml.FullLoader)
    
    print(COM_number['forearm'])
    print(COM_number['arm'])