#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 01:58:42 2019

@author: lis
"""

import HRI
from  pilot_analysis_utils import *
import pilots_plot_errors

with_outlier = True

if with_outlier:

    list_l = ['pilot_x1_motive',
              'pilot_x2_motive',
              'pilot_x3_motive',
              'pilot_x4_motive',
              'pilot_x1_hand_motive']
    
    list_nl = ['pilot_x1_motive_NL',
              'pilot_x2_motive_NL',
              'pilot_x3_motive_NL',
              'pilot_x4_motive_NL',
              'pilot_x1_hand_motive_NL']

else:

    list_l = ['pilot_x1_motive',
              'pilot_x2_motive',
              'pilot_x3_motive',
              'pilot_x4_motive']
    
    list_nl = ['pilot_x1_motive_NL',
              'pilot_x2_motive_NL',
              'pilot_x3_motive_NL',
              'pilot_x4_motive_NL']
    


l = []
nl = []

for i in list_l:
    
    l.append(HRI.load_obj(i))
    
for i in list_nl:
    
    nl.append(HRI.load_obj(i))
    
nl_p = [x.test_results[0]['mse'] for x in nl]

l_p = [x.test_results[0]['mse'] for x in l]


l_np = test_nonpers(l,lin = True)
nl_np = test_nonpers(nl,lin = False)

#l_np = l_np_mse
#nl_np = nl_np_mse

errors = {'l_p' : l_p, 'nl_p' : nl_p, 'l_np' : l_np, 'nl_np' : nl_np }

HRI.save_obj(errors, 'errors_new_outliers')


err = HRI.load_obj('errors')
err1 = HRI.load_obj('errors_new_outliers')

pilots_plot_errors.main(err1)