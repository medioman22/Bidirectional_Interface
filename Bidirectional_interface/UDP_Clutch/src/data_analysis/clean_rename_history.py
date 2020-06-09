#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 15:55:02 2019

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

folder = '/Volumes/GoogleDrive/My Drive/Matteo/EPFL/LIS/PhD/Natural_Mapping/DATA/Unity_data/experiments/history_files'

#info = 'interface_motive_method_maxmin'

#useful_file_size_min = 900

control_history_folder = os.path.join(folder, 'control_history')
history_raw_folder = os.path.join(folder, 'history_raw')
unity_history_folder = os.path.join(folder, 'unity_history')

utils.create_dir_safe(control_history_folder)
utils.create_dir_safe(history_raw_folder)
utils.create_dir_safe(unity_history_folder)


files = utils.listdir_fullpath(folder)

for file in files:
    new_name = file[:]
    
    new_name = new_name.replace('torso', info)
    
    if 'user' not in new_name:
        new_name = new_name.replace('unity_history', info+'_user_unity_history')
        new_name = new_name.replace('control_history', info+'_user_control_history')
    
    if 'inst' not in new_name:
        new_name = new_name.replace('_1_', '_inst_1_')
        new_name = new_name.replace('_2_', '_inst_2_')
        new_name = new_name.replace('_3_', '_inst_3_')
        new_name = new_name.replace('_4_', '_inst_4_')
        new_name = new_name.replace('_5_', '_inst_5_')
        new_name = new_name.replace('_6_', '_inst_6_')
        new_name = new_name.replace('_7_', '_inst_7_')
        
    if '_inst_4_' or '_inst_5_' or '_inst_6_' in new_name:
        new_name = new_name.replace('_inst_4_', '_inst_1_baseline_')
        new_name = new_name.replace('_inst_5_', '_inst_2_baseline_')
        new_name = new_name.replace('_inst_6_', '_inst_3_baseline_')
        
    
    os.rename(file, new_name)
    
    if 'file_garbage' in new_name:
        os.rename(new_name, os.path.join(garbage_folder, os.path.basename(new_name)))
    elif 'file_maneuvers' in new_name:
        os.rename(new_name, os.path.join(maneuvers_folder, os.path.basename(new_name)))
    elif '_baseline' in new_name:
        os.rename(new_name, os.path.join(baseline_folder, os.path.basename(new_name)))
    elif os.path.getsize(new_name) <  useful_file_size_min:
        os.rename(new_name, os.path.join(useless_folder, os.path.basename(new_name)))
        
        