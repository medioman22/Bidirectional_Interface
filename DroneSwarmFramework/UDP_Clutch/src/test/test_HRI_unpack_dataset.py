# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 10:53:32 2018

@author: macchini
"""

# needed to use modules/scripts from parent folder


import matplotlib.pyplot as plt

import context 

import dataset_handling.CalibrationDataset as CalibrationDataset
from settings.settings import get_settings

settings = get_settings()

if settings['input_device']=='motive':
    cal = CalibrationDataset.MotiveDataset()
elif settings['input_device']=='remote':
    cal = CalibrationDataset.RemoteDataset()
elif settings['input_device']=='imu':
    cal = CalibrationDataset.ImuDataset()
elif settings['input_device']=='imus':
    cal = CalibrationDataset.ImusDataset()
    
#    cal.folder = folder
    
cal.import_data()

cal.extract_from_mixed()

plt.plot(cal.data['roll'])
plt.plot(cal.data['pitch'])

plt.show()