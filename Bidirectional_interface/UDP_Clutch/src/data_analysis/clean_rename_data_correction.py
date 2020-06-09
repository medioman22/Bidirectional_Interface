#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 19:44:07 2019

@author: lis
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 13:02:17 2018

@author: macchini
"""

import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import utils

folder = '/Volumes/GoogleDrive/My Drive/Matteo/EPFL/LIS/PhD/Natural_Mapping/DATA/Unity_data/remote_simple'

wrong = '_31'
correct = '_32'


files = utils.listdir_fullpath(folder)

for file in files:
    new_name = file[:]
    
    new_name = new_name.replace(wrong, correct)
    
    os.rename(file, new_name)
    