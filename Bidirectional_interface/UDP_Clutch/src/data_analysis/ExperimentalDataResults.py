#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 17:21:39 2018

@author: matteomacchini
"""

import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from matplotlib.pylab import savefig
import numpy as np
import pandas as pd
import data_analysis_tools as da_tools
from utils import find_string


""" GLOBALS """

""" ABSTRACT CLASS """


class ExperimentalDataResults(ABC):
    
    """ private variables """
    _files_in_folder = None
    
    
    """ public variables """

    
    """ private functions """
    
    
#    @abstractmethod
    def __init__(self):
        """Initialize the dataset."""
        
        self.subject = None
        self.interface = None
        self.method = None
#        self.folder = 'D:\\_UnityData\\exp_remote_simple'
#        self.folder = '/Users/matteomacchini/Google Drive/Matteo/EPFL/LIS/PhD/Natural_Mapping/DATA/Unity_data/exp'
        self.folder = '/Users/lis/Google Drive File Stream/My Drive/Matteo/EPFL/LIS/PhD/Personalized_Mapping/DATA/Unity_data/experiments'
        
        pass
    
    
#    @abstractmethod
    def _list_files_in_folder(self):
        self._files_in_folder = os.listdir(self.folder)
        self._files_in_folder.sort()
        
    
#    @abstractmethod
    def _get_folder_info(self):
        
        self._list_files_in_folder()
        
        # list of dictionaries
        self.folder_info = []
        for i in self._files_in_folder:
            
            self.folder_info.append({})
            
            self.folder_info[-1]['filename'] = i
            self.folder_info[-1]['type'] = self._find_type(i)
            self.folder_info[-1]['subject'] = self._find_subject(i)
            self.folder_info[-1]['interface'] = self._find_interface(i)
            self.folder_info[-1]['method'] = self._find_method(i)
        
    
    def _find_subject(self, string):
        
        return da_tools.find_subject_from_filename(string)
        
    
    def _find_type(self, string):
        
        return da_tools.find_file_type_from_filename(string)
    
    
    def _find_interface(self, string):
        
        return da_tools.find_interface_from_filename(string)
            
        
    def _find_method(self, string):
        
        return da_tools.find_method_from_filename(string)
    
    
    """ public functions """
    
    
#    @abstractmethod
    def load(self, load_all = False):
        """Imports the files and stores them in a single pandas df"""
        
        # default values (all)
        if self.subject == None:
            self.subject = [x['subject'] for x in self.folder_info]
        
        if self.method == None:
            self.method = [x['method'] for x in self.folder_info]
        
        if self.interface == None:
            self.interface = [x['interface'] for x in self.folder_info]
        
        here = os.getcwd()
        os.chdir(self.folder)
        
        # distinguish if load everything
        not_to_load = [None] if load_all else [None, 'unity_history', 'control_history', 'control_history_raw', 'settings'] 
        
        # filter
        files_to_keep = [x for x in self.folder_info if x['subject'] in self.subject and x['method'] in self.method and x['interface'] in self.interface and x['type'] not in not_to_load]
               
#        for x in files_to_keep:
#            print (x['filename'])
#            {'data' : pd.read_csv(x['filename'], sep='\t', index_col = False), 'info' : x}
             
        # import
        self.filtered_data_all = [{'data' : pd.read_csv(x['filename'], sep='\t', index_col = False), 'info' : x} for x in files_to_keep]
        
        # concatenate instances per subject
        self.filtered_data = []

        for i in np.unique([x['info']['subject'] for x in self.filtered_data_all]):
#            all_man_subjects = [x for x in self.filtered_data_all if x['info']['subject'] == i and x['info']['type'] is 'maneuvers']
            all_perf_subjects = [x for x in self.filtered_data_all if x['info']['subject'] == i and x['info']['type'] is 'performance']
            
            # concatenate maneuvers
#            new_man = all_man_subjects[0]['data']
#            for j in all_man_subjects[1:]:
#                new_man = pd.concat([new_man, j['data']])
                
            # concatenate performance
            new_perf = all_perf_subjects[0]['data'][:-1]
            for j in all_perf_subjects[1:]:
                new_perf = pd.concat([new_perf, j['data'][:-1]])    # remove last value (= -1)
                
            # correct index
#            new_man.index = range(len(new_man.index))
            new_perf.index = range(len(new_perf.index))
            
            # save
#            self.filtered_data.append({'data' : new_man, 'info' : all_man_subjects[0]['info']})
            self.filtered_data.append({'data' : new_perf, 'info' : all_perf_subjects[0]['info']})
            
        
        os.chdir(here)
        
        return self.filtered_data
    
    
#    @abstractmethod
    def plot(self, options):
        """Plotting function for performance, time..."""
        pass
    
    
#    @abstractmethod
    def set_folder(self, new_folder = None):
        """Choose or refresh data folder"""
        
        if new_folder is None:
            new_folder = self.folder
        
        self.folder = new_folder
        self._get_folder_info()
    
    
#    @abstractmethod
    def set_subjects(self, subject):
        """Choose subjects for data analysis"""
        self.subject = subject
    
    
#    @abstractmethod
    def set_methods(self, method):
        """Choose methods for data analysis"""
        self.method = method
    
    
#    @abstractmethod
    def set_interfaces(self, interface):
        """Choose interfaces for data analysis"""
        self.interface = interface
    
    
#    @abstractmethod
    def plot_performance(self, style = 'multiplot'):
        """Plot performance over iterations"""
    
        plt.figure()
        
        if style == 'multiplot':
            
            performance_data = self.performance_data
            for i in performance_data:
                plt.plot(i['data']['performance'], label = i['info']['subject'])
                
        elif style == 'mean-var' or style == 'mean-max-min':
            
            if style == 'mean-var':
                plt.plot(self.mean, 'b')
                plt.plot(self.mean - 3*self.std, 'g')
                plt.plot(self.mean + 3*self.std, 'g')
            elif style == 'mean-max-min':
                plt.plot(self.mean, 'b')
                plt.plot(self.M, 'g')
                plt.plot(self.m, 'g')
            
            
        plt.xlabel('waypoint N')
        if self.process_method == 'error':
            plt.ylabel('distance from center [m]')
        elif self.process_method == 'squared error':
            plt.ylabel('distance from center [m], squared')
        plt.grid()
        plt.legend()
        plt.title(self.interface + self.method)
        
        plt.ylim([-5, 25])
                
        savefig('performance ' + str(self.interface) + ' ' + style + ' ' + self.process_method + '.pdf', bbox_inches='tight')
                
            
    
#    @abstractmethod
    def process_performance(self, running_average_window = 5, method = 'error'):
        """Plot performance over iterations"""
        
        self.used_window = running_average_window
        
        self.process_method = method
        
        # get performance data
        performance_data = [x for x in self.filtered_data if x['info']['type'] == 'performance']
        
        for i in performance_data:
            # compute SE
            if method == 'error':
                i['data']['performance_per_point'] = i['data']['dist2WPcenter']
            elif method == 'squared error':
                i['data']['performance_per_point'] = i['data']['dist2WPcenter']**2
            else:
                raise NameError('"', method, '"', ' is an unknown processing method')
            # compute running average
            i['data']['performance'] = np.concatenate([np.zeros(running_average_window-1,), np.convolve(i['data']['performance_per_point'], np.ones((running_average_window,))/running_average_window, mode='valid')])
#            i['data']['performance'] = np.convolve(i['data']['performance_per_point'], np.ones((running_average_window,))/running_average_window, mode='valid')
    
        all_perf = np.empty([len(performance_data[0]['data']['performance'][self.used_window+1:]), len(performance_data)])
        for idx, i in enumerate(performance_data):
            all_perf[:,idx] = i['data']['performance'][self.used_window+1:]
#             print(len(i['data']['performance'][self.used_window+1:]))
            
        mean = np.mean(all_perf,  axis=1)
        M = np.max(all_perf,  axis=1)
        m = np.min(all_perf,  axis=1)
        std = np.std(all_perf,  axis=1)
                
        # save data for manual plot
        
        self.M = M
        self.m = m
        self.mean = mean
        self.std = std
        
        self.all_perf = all_perf
        
        self.performance_data = performance_data