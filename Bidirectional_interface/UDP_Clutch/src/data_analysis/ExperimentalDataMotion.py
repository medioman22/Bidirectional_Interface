#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 17:21:39 2018

@author: matteomacchini
"""

import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scriptz'))

from abc import ABC, abstractmethod
import basic_settings as settings
import collections
import HRI_mapping_test
import HRI
import matplotlib.pyplot as plt
from matplotlib.pylab import savefig
import numpy as np
import pandas as pd
from utils import find_string
import utils
import pickle



""" GLOBALS """

""" ABSTRACT CLASS """


class ExperimentalDataMotion(ABC):

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
#        self.folder = '/Users/matteomacchini/Google Drive/Matteo/EPFL/LIS/PhD/Natural_Mapping/DATA/acquired_data/Experimental'
#        self.folder_ready = '/Users/matteomacchini/Google Drive/Matteo/EPFL/LIS/PhD/Natural_Mapping/DATA/acquired_data/interfaces'
        self.folder = '/Users/lis/Google Drive File Stream/My Drive/Matteo/EPFL/LIS/PhD/Personalized_Mapping/DATA/acquired_data/Experimental'
        self.folder_ready = '/Users/lis/Google Drive File Stream/My Drive/Matteo/EPFL/LIS/PhD/Personalized_Mapping/DATA/acquired_data/interfaces'

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
            self.folder_info[-1]['maneuver'] = self._find_maneuver(i)
            self.folder_info[-1]['subject'] = self._find_subject(i)
            self.folder_info[-1]['interface'] = self._find_interface(i)
            self.folder_info[-1]['method'] = self._find_method(i)


    def _find_subject(self, string):

        _subject = find_string(string, 'subject_\d+')

        if _subject is not None:
            return int(_subject.replace('subject_', ''))
        else:
            return None


    def _find_maneuver(self, string):

            if 'straight' in string:
                return 'straight'
            elif 'just_left' in string:
                return 'just_left'
            elif 'just_right' in string:
                return 'just_right'
            elif 'just_up' in string:
                return 'just_up'
            elif 'just_down' in string:
                return 'just_down'
            elif 'up_left' in string:
                return 'up_left'
            elif 'up_right' in string:
                return 'up_right'
            elif 'down_right' in string:
                return 'down_right'
            elif 'down_left' in string:
                return 'down_left'
            else:
                return None


    def _find_interface(self, string):

            if 'remote' in string:
                return 'remote'
            elif 'motive' in string:
                return 'motive'
            else:
                return None


    def _find_method(self, string):

            if 'simple' in string:
                return 'simple'
            elif 'maxmin' in string:
                return 'maxmin'
            elif 'new' in string:
                return 'new'
            elif 'personal' in string:
                return 'personal'
            else:
                return None


    """ public functions """


#    @abstractmethod
    def load(self, load_clean = True):
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
        to_load =  [x['filename'] for x in self.folder_info if 'CLEAN' in x['filename']] if load_clean else [x['filename'] for x in self.folder_info]

        # filter
        files_to_keep = [x for x in self.folder_info if x['subject'] in self.subject and x['method'] in self.method and x['interface'] in self.interface and x['filename'] in to_load]

        # import
        self.filtered_data_all = [{'info' : x} for x in files_to_keep]

        # concatenate instances per subject
        self.filtered_data = []

        for i in np.unique([x['info']['subject'] for x in self.filtered_data_all]):

            settings.subject_name = 'subject_' + str(i)
            settings.input_device = 'motive'
            settings.control_style = 'maxmin'
            settings.store = True

            self.filtered_data.append({'data' : HRI_mapping_test.mapping_procedure(settings), 'subject' : i})


        os.chdir(here)

        return self.filtered_data


#    @abstractmethod
    def load_ready(self):
        """Imports the files and stores them in a single pandas df"""

        self.filtered_data = []

        for i in os.listdir(self.folder_ready):

            if i != 'desktop.ini' and i != 'Icon\r' and '.pkl' in i:

                print(i)
                with open(os.path.join(self.folder_ready, i), 'rb') as f:
                    temp = pickle.load(f)
                self.filtered_data.append({'data' : temp, 'filename' : i})

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

        # get performance data
        performance_data = [x for x in self.filtered_data if x['info']['type'] == 'performance']

        plt.figure()

        if style == 'multiplot':
            for i in performance_data:
                plt.plot(i['data']['performance'], label = i['info']['subject'])
        elif style == 'mean-var' or style == 'mean-max-min':


            all_perf = np.empty([len(performance_data[0]['data']['performance'][self.used_window+1:]), len(performance_data)])
            for idx, i in enumerate(performance_data):
                all_perf[:,idx] = i['data']['performance'][self.used_window+1:]

            mean = np.mean(all_perf,  axis=1)
            M = np.max(all_perf,  axis=1)
            m = np.min(all_perf,  axis=1)
            std = np.std(all_perf,  axis=1)

            if style == 'mean-var':
                plt.plot(mean, 'b')
                plt.plot(mean - 3*std, 'g')
                plt.plot(mean + 3*std, 'g')
            elif style == 'mean-max-min':
                plt.plot(mean, 'b')
                plt.plot(M, 'g')
                plt.plot(m, 'g')


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
        savefig('performance ' + str(self.interface) + ' ' + style + ' ' + self.process_method + '.png', bbox_inches='tight')

        # save data for manual plot

        self.M = M
        self.m = m
        self.mean = mean
        self.std = std



#    @abstractmethod
    def process_motion(self):
        """Plot performance over iterations"""

        rot = ['roll', 'pitch', 'yaw']
        digits = [9, 8, 7, 6, 3, 10, 11, 12, 13]
        body_parts = [HRI.settings['body_parts_code'][i] for i in digits]

        def sum_dict_over_list(d):

            # compute all dictionaries
            mean = {}
            std = {}

            for j in set(d[-1]):
                mean[j] = np.mean([i[j] for i in d])
                std[j] = np.std([i[j] for i in d])

            mean = collections.OrderedDict(sorted(mean.items()))
            std = collections.OrderedDict(sorted(std.items()))

            # get lists of values from dictionaries
            mean_per_limb = {}
            std_per_limb = {}

            for i in digits:

                mean_v = []
                std_v = []
                for r in rot:
                    key = r + '_' + str(i)
                    mean_v.append(mean[key])
                    std_v.append(std[key])
                mean_per_limb[str(i)] = mean_v
                std_per_limb[str(i)] = std_v

            mean_rpy = utils.transpose_list(list(mean_per_limb.values()))
            std_rpy = utils.transpose_list(list(std_per_limb.values()))

            mean_per_limb_tot_dict = {}

            for i in digits:
                key = str(i)
                mean_per_limb_tot_dict[key] = sum(mean_per_limb[key])

            mean_per_limb_tot = list(mean_per_limb_tot_dict.values())

            return [mean_rpy, std_rpy, mean_per_limb_tot]

        def process(in_dict):
            # plots
            norm = False

            [mean_rpy, std_rpy, mean] = sum_dict_over_list(in_dict)

            return [mean_rpy, std_rpy]


        deb = [x['data']._debug for x in self.filtered_data]

        o_covar = []
        o_snr = []
        o_signal_rms = []
        o_noise_rms = []
        o_coeff = []

        for i in deb:

            o_covar.append(utils.norm_dict_to_one(collections.OrderedDict(sorted(i['covar'].items()))))
            # o_signal_rms.append(utils.norm_dict_to_one(collections.OrderedDict(sorted(i['signal_rms'].items()))))
            # o_noise_rms.append(utils.norm_dict_to_one(collections.OrderedDict(sorted(i['noise_rms'].items()))))
            o_snr.append(utils.norm_dict_to_one(collections.OrderedDict(sorted(i['snr'].items()))))
            o_coeff.append(utils.norm_dict_to_one({k: o_covar[-1].get(k, 0) * o_snr[-1].get(k, 0) for k in set(o_covar[-1]) & set(o_snr[-1])}))

        covar_mean, covar_std = process(o_covar)
        snr_mean, snr_std = process(o_snr)
        coeff_mean, coeff_std = process(o_coeff)

        outl = []
        idx = []

        for i in o_coeff:
            test = list(i.values())
            outl.append(utils.outliers_Z(test, 0.5)[0])
            idx.extend(utils.outliers_Z(test, 0.5)[1])

        n_all = {list(o_coeff[0].keys())[x] : np.histogram(idx, np.arange(28) - 0.5)[0][x] for x in np.arange(len(list(o_coeff[0].keys())))}

        n_uses_per_limb = {}

        for i in digits:

            n_uses = []

            for r in rot:
                key = r + '_' + str(i)
                n_uses.append(n_all[key])
            n_uses_per_limb[str(i)] = n_uses

        n_uses_rpy = utils.transpose_list(list(n_uses_per_limb.values()))

#        utils.bar_multi(vals = n_uses_rpy, xlabels = body_parts, legend = rot, title = 'use per feature', normalize = False)


        list_comp = [covar_mean, snr_mean, coeff_mean]

#        utils.bar_multi(vals = list_comp, xlabels = body_parts, legend = ['covariance', 'snr', 'coefficient'], normalize = False)

        self.covar_mean = covar_mean
        self.snr_mean = snr_mean
        self.coeff_mean = coeff_mean
        self.covar_std = covar_std
        self.snr_std = snr_std
        self.coeff_std = coeff_std

        self.n_uses_rpy = n_uses_rpy
        self.body_parts = body_parts
        self.rot = rot

    def plot_motion():

        def plot(mean_rpy, std_rpy, tit, norm):

            utils.bar_multi(vals = mean_rpy, error = std_rpy, xlabels = self.body_parts, legend = self.rot, title = tit, normalize = norm)

        plot(covar_mean, covar_std, 'covariance', False)
        plot(snr_mean, snr_std, 'snr', False)
        plot(coeff_mean, coeff_std, 'coefficient', False)
