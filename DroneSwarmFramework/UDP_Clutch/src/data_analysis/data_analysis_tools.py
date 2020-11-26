#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 16:46:33 2019

@author: lis
"""
from utils import find_string

def find_subject_from_filename(filename):
    
    _subject = find_string(filename, 'subject_\d+')
    
    if _subject is not None:
        return int(_subject.replace('subject_', ''))
    else:
        return None
    
def find_file_type_from_filename(filename):
        
    if 'settings' in filename:
        return 'settings'
    elif 'performance' in filename:
        return 'performance'
    elif 'maneuvers' in filename:
        return 'maneuvers'
    elif 'unity_history' in filename:
        return 'unity_history'
    elif 'control_history' in filename:
        return 'control_history'
    elif 'control_history_raw' in filename:
        return 'control_history_raw'
    else:
        return None
    
    
def find_interface_from_filename(filename):
    
    if 'remote' in filename:
        return 'remote'
    elif 'motive' in filename:
        return 'motive'
    else:
        return None
            
        
def find_method_from_filename(filename):
    
        if 'simple' in filename:
            return 'simple'
        elif 'maxmin' in filename:
            return 'maxmin'
        elif 'new' in filename:
            return 'new'
        elif 'personal' in filename:
            return 'personal'
        else:
            return None