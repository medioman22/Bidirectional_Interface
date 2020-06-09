#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 19:12:38 2019

@author: lis
"""

###############################################################################

list_files = ['pilot_x1_motive_mixed_period_10_amplitude_50_inst_10_2018_Oct_26_12_33_18PM.txt',
              'pilot_x2_motive_mixed_period_10_amplitude_50_inst_10_2018_Oct_25_07_16_32PM.txt',
              'pilot_x3_motive_mixed_period_10_amplitude_50_inst_10_2018_Oct_26_02_07_35PM.txt',
              'pilot_x4_motive_mixed_period_10_amplitude_50_inst_10_2018_Oct_26_03_02_50PM.txt',
              'pilot_x1_hand_motive_mixed_period_10_amplitude_50_inst_10_2018_Oct_26_12_46_09PM.txt']

list_subjects = ['pilot_x2_motive']#,
#                 'pilot_x2_motive',
#                 'pilot_x3_motive',
#                 'pilot_x4_motive',
#                 'pilot_x1_hand_motive']

#list_files = ['pilot_x4_motive_mixed_period_10_amplitude_50_inst_10_2018_Oct_26_03_02_50PM.txt']
#list_subjects = ['subject_29']

import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.insert(1, os.path.join(sys.path[0], '../../scriptz'))

import HRI

from  builtins import any as b_any
import numpy as np
import pandas as pd
import socket
import struct
import time
import utils

import CalibrationDataset_TEST
import HRI_mapping_test

import basic_settings as settings

os.chdir(os.path.join(os.getcwd(), 'pilot_data'))
#os.chdir(os.path.join('/Volumes/GoogleDrive/My Drive/Matteo/EPFL/LIS/PhD/Natural_Mapping/DATA/acquired_data/Non_experimental/mixed_unpacked/')


list_files = [x for x in os.listdir()[1:] if '_mixed' in x]

for idx,i in enumerate(list_files):
    
    if i in os.listdir():
        CalibrationDataset_TEST.extract_dataset(i, 'motive', fol = os.getcwd(), fix_name = list_subjects[idx])
    
objects = os.listdir()

for i in objects:
    if 'straight' in i:
        os.remove(i)
        

os.chdir('..')
        

for i in list_subjects:
    
    os.chdir(os.path.join(os.getcwd(), 'pilot_data'))
    settings.store = False   
    settings.data_folder = os.path.join(os.getcwd())
 
    settings.subject_name = i
    settings.control_style = 'maxmin'
    
    mapping_l = HRI_mapping_test.mapping_procedure(settings)
    
    
    settings.control_style = 'new'
    settings.data_folder = os.getcwd()
    
    mapping_nl = HRI_mapping_test.mapping_procedure(settings)
    
    os.chdir('..')
    utils.save_obj(mapping_l, i)
    utils.save_obj(mapping_nl, i+'_NL')

