# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 19:25:27 2019

@author: hkohli
"""
import yaml

with open(r'param_bracelets.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    COM_number = yaml.load(file, Loader=yaml.FullLoader)
    
    print(COM_number['COM']['forearm'])
    print(COM_number['COM']['arm'])
    print(COM_number['correction_factor'])