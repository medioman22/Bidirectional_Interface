#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 13:02:00 2019

@author: lis
"""

import context

if 'comm' in locals():
   comm.close_sockets()
   
import HRI_communication as comm

comm.run(mode = 'acquisition')