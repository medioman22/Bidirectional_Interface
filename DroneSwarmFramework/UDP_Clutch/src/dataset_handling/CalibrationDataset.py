# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 10:14:24 2018

@author: macchini
"""

import sys,os

from abc import ABC, abstractmethod
import numpy as np
import pandas as pd

import context

from utilities.utils import find_string
from utilities.utils import create_dir_safe

import utilities.HRI as HRI
from settings.settings import get_settings

settings = get_settings()

""" GLOBALS """
 
calib_maneuver_dict = {0 : 'straight', 
                            1 : 'just_left', 
                            2 : 'just_right', 
                            3 : 'just_up', 
                            4 : 'just_down', 
                            5 : 'up_right', 
                            6 : 'up_left', 
                            7 : 'down_right', 
                            8 : 'down_left'}

""" ABSTRACT CLASS """

class CalibrationDataset(ABC):
    
    """private variables"""
    
    # input
    _input = None
    # subject
    _subject = None
    # instance
    _instance = None
    # maneuver
    _maneuver = None
    # period
    _period = None
    # amplitude
    _amplitude = None
    # timestamp
    _timestamp = None
    # is processed
    _is_processed = None
    # is normalized
    _is_normalized = None
    
    """public variables"""
    
    # original file name
    filename = None               # example pilot_xx_remote_mixed_period_10_amplitude_50_inst_9_2018_Oct_24_01_01_28PM
    # original data folder
    folder = None
    # data
    data = None
    # fields
    fields = None
    # train or test 
    train_test = None               # options : 'train', 'test', 'generic'



    def __init__(self, filename = None):
        """Initialize the dataset."""
        
        self.folder = os.path.join(settings['data_folder'], HRI.file_name(settings))
            
        if filename is not None:
            
            self.filename = filename
            
        else:
            files = os.listdir(self.folder)
            
            files = [x for x in files if 'mixed' in x and 'unpacked' not in x]

            if len(files) == 1:
                self.filename = files[0]
            elif len(files) == 0:
                raise TypeError('no files found from this subject!')
            else:
                raise TypeError('more than one file found from this subject!')
                
            
        self._instance = find_string(self.filename, 'inst_\d+')
        
        self.maneuver_from_filename()
        self.period_from_filename()
        self.amplitude_from_filename()
        self.timestamp_from_filename()
        
    @abstractmethod
    def extract_from_mixed(self):
        """ extract multiple datasets from a mixed dataset """
        
        if not self._maneuver == 'mixed':
            print('This is not a mixed dataset')
        else:
            self.import_data()
            
            _maneuver_list = np.unique(self.data['maneuver'])
            
            _maneuver_list_str = [calib_maneuver_dict[x] for x in _maneuver_list]
            
            print('Found ' + str(len(_maneuver_list)) + ' different maneuvers')
            
            self._sub_datasets = [self.data[self.data['maneuver'] == x] for x in _maneuver_list]
            
            params = {}
            
            for i in self._sub_datasets:
                params['subject'] = self._subject
                params['input'] = self._input
                params['maneuver'] = calib_maneuver_dict[np.unique(i['maneuver'])[0]]   # first value of unique
                params['period'] = str(self._period)
                params['amplitude'] = str(self._amplitude)
                params['instance'] = str(settings['instance'])
                params['timestamp'] = self._timestamp
                
                params = params
            
                _sub_filename = self.filename_from_params(params)
            
                print('saving ' + _sub_filename + ' to ' + self.folder)
                if params['maneuver']!='straight':
                    self.save(os.path.join(self.folder, _sub_filename), i)
            
            create_dir_safe(os.path.join(self.folder, '_mixed_unpacked'))
            
            os.rename(os.path.join(self.folder, self.filename), os.path.join(self.folder, '_mixed_unpacked', self.filename))
            
            
    def filename_from_params(self, params):
        """ defines filename from given parameters """

        filename = params['maneuver'] + '_period_' + \
                    params['period'] + '_amplitude_' + \
                    params['amplitude'] + '_inst_' + \
                    params['instance'] + '_' + \
                    params['timestamp'] + '.txt'
        
        return filename
            
            
    def fix_subject_name(self, name):
        """ defines custom subject name """
        
        self._subject = name
            
            
    def maneuver_from_filename(self):
        """ defines maneuver from given filename """
        
        _maneuver = find_string(self.filename, '.+_period')
        self._maneuver = _maneuver.replace('_period', '')
            
            
    def period_from_filename(self):
        """ defines period from given filename """
        
        _period = find_string(self.filename, 'period_\d+')
        self._period = int(_period.replace('period_', ''))
            
            
    def amplitude_from_filename(self):
        """ defines amplitude from given filename """
        
        _amplitude = find_string(self.filename, 'amplitude_\d+')
        self._amplitude = int(_amplitude.replace('amplitude_', ''))
            
            
    def timestamp_from_filename(self):
        """ defines amplitude from given filename """
        
        _timestamp = find_string(self.filename, '2\d\d\d.+\.txt')
        self._timestamp = _timestamp.replace('.txt', '')
        
        
    @abstractmethod
    def import_data(self):
        """ import data """
        
        self.data = pd.read_csv(os.path.join(self.folder, self.filename))
        
        if 'CLEAN_' in self.filename: 
            self._is_processed = True
        else : 
            self._is_processed = False
            
        self.fields = list(self.data)
        
        
    @abstractmethod
    def is_processed(self):
        """ is the dataset processed """
        
        return self._is_processed
        
        
    def save(self, filename = None, data = None):
        """ save dataset to file """
        
        if filename is None:
            filename = self.filename
        if data is None:
            data = self.data
            
        data.to_csv(os.path.join(self.folder, filename), index=False)

        
    @abstractmethod
    def update_settings(self, settings_in):
        """ update settings """
        global settings
        settings = settings_in
        
    
    
class RemoteDataset(CalibrationDataset):
    
    _input = 'remote'
    
    
    def extract_from_mixed(self):
        """ extract multiple datasets from a mixed dataset """
        super().extract_from_mixed()
            
    
    def import_data(self):
        """ import data """
        super().import_data()
        
        
    def is_processed(self):
        """ is the dataset processed """
        super().is_processed()
        
        
    def update_settings(self, settings_in):
        """ update settings """
        super().update_settings(settings_in)
        
    
    
class ImuDataset(CalibrationDataset):
    
    _input = 'IMU'
    
    
    def extract_from_mixed(self, instance = 1):
        """ extract multiple datasets from a mixed dataset """
        super().extract_from_mixed(instance = instance)
            
    
    def import_data(self):
        """ import data """
        super().import_data()
        
        
    def is_processed(self):
        """ is the dataset processed """
        super().is_processed()
        
        
    def update_settings(self, settings_in):
        """ update settings """
        super().update_settings(settings_in)
        
    
    
class ImusDataset(CalibrationDataset):
    
    _input = 'IMUS'
    
    
    def extract_from_mixed(self):
        """ extract multiple datasets from a mixed dataset """
        super().extract_from_mixed()
            
    
    def import_data(self):
        """ import data """
        super().import_data()
        
        
    def is_processed(self):
        """ is the dataset processed """
        super().is_processed()
        
        
    def update_settings(self, settings_in):
        """ update settings """
        super().update_settings(settings_in)
        
        
    

""" SUBCLASSES """
    
    
class MotiveDataset(CalibrationDataset):
    
    _input = 'motive'
    
    
    def extract_from_mixed(self):
        """ extract multiple datasets from a mixed dataset """
        super().extract_from_mixed()
            
    
    def import_data(self):
        """ import data """
        super().import_data()
        
        
    def is_processed(self):
        """ is the dataset processed """
        super().is_processed()
        
        
    def update_settings(self, settings_in):
        """ update settings """
        super().update_settings(settings_in)
    
    
class ImusDataset(CalibrationDataset):
    
    _input = 'imus'
    
    
    def extract_from_mixed(self):
        """ extract multiple datasets from a mixed dataset """
        super().extract_from_mixed()
            
    
    def import_data(self):
        """ import data """
        super().import_data()
        
        
    def is_processed(self):
        """ is the dataset processed """
        super().is_processed()
        
        
    def update_settings(self, settings_in):
        """ update settings """
        super().update_settings(settings_in)