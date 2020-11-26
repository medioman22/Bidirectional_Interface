# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 16:17:29 2019

@author: macchini
"""

import pandas as pd
import numpy as np

filename = 'file:///G:/My Drive/Matteo/EPFL/LIS/PhD/Natural_Mapping/DATA/Unity_data/exp/subject_12_interface_motive_method_new_file_performance_inst_2_20181212181603592.txt'

data = pd.read_csv(filename, sep='\t', index_col = False).iloc[:-1]

dist = 'dist2WPcenter'
time = 'time2prevWP'

d_m = np.mean(data[dist][-10:])
t_mtime = np.mean(data[time][-10:])