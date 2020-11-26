# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 10:45:10 2018

@author: macchini
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pickle
from scipy import stats
import re


#########################



def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


#########################


def find_string(string, pattern):
    match = re.search(pattern, string)
    if match: return match.group()
    else: return None


#########################
            

def normalize(array, norm_param = None):

    if norm_param is None: 
        # zero mean, unit variance
        
        av = np.average(array)
        
        array_zeromean = array-av
        
        std = np.std(array_zeromean) if np.std(array_zeromean) != 0 else 1
        
        array_norm = array_zeromean/std
        
        norm_param = [av, std]
        
    else:
        # norm_param is given
        
        if len(array.shape) == 1:
            mean = norm_param[0].flatten()
        else:
            mean = norm_param[0]#.resize(array.shape)
        
        array_zeromean = array-mean
        
        array_norm = array_zeromean
        
        if len(array.shape) == 1:
            var = norm_param[1].flatten()
        else:
            var = norm_param[1]#.resize(array.shape)
        
        array_norm = array_zeromean/var

    return [array_norm, norm_param]


#########################
            

def normalize_array(array, norm_param = None):

    if norm_param is None: 
        # zero mean, unit variance
        
        av = np.average(array)
        
        array_zeromean = array-av
        
        std = np.std(array_zeromean)
        
        array_norm = array_zeromean/std if std != 0 else array_zeromean
        
        norm_param = [av, std]
        
    else:
        # norm_param is given
        
        array_zeromean = array-norm_param[0]
        
        array_norm = array_zeromean
        
        # divide only where var != 0
        array_norm = array_zeromean/norm_param[1] if norm_param[1] != 0 else array_norm

    return [array_norm, norm_param]


#########################
    
    
def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


#########################


def moving_average(data_set, periods=3, fill_with_zeros = True):
    
    if data_set.size < periods:
        return data_set
    
    if isinstance(data_set, pd.DataFrame):
        print('a')
        data_set.index = range(len(data_set))

    weights = np.ones(periods) / periods
    
    ma = np.convolve(data_set, weights, mode='valid')

    if fill_with_zeros:
        fill_before = np.ones(int(np.ceil((len(data_set) - len(ma))/2))) * data_set[0]
        fill_after = np.ones(int(np.floor((len(data_set) - len(ma))/2))) * data_set[-1]
        ma = np.hstack([fill_before, ma, fill_after])
    
    return ma


def rms(signal):
    
    sq = sum(signal**2)
    mean = np.mean(sq)
    rms = np.sqrt(mean)
    
    return rms


def find_maxmin(my_array, what = 'max', absolute = False):
    
    if type(my_array) is list:
        my_array = np.array(my_array)
    
    if absolute:
        return [abs(my_array).max(), abs(my_array).argmax()]
    elif what == 'max':
        return [my_array.max(), my_array.argmax()]
    elif what == 'min':
        return [my_array.min(), my_array.argmin()]


def find_maxmin_first(my_array):
    
    if type(my_array) is list:
        my_array = np.array(my_array)
        
    M = my_array.max()
    m = abs(my_array.min())
    
    aM = my_array.argmax()
    am = my_array.argmin()
    
    # if both max and min are relevant
    if max([M,m])/min([M,m])<2:
        if aM<am:                    # itmax comes first
            return [M, aM]
        else:
            return [m, am]
    else:
        return find_maxmin(my_array, absolute = True)
    
    
def transpose_list(l):
    
    l1 = []
    
    for i in np.arange(len(l[0])):
        
        l1.append([x[i] for x in l])
        
    return l1

def norm_dict(d):
    
    m = max(d.values())
    
    for i in set(d):
        d[i] = d[i]/m
        
    return d

def norm_dict_to_one(d):
    
    m = sum(d.values())
    
    for i in set(d):
        d[i] = d[i]/m
        
    return d

def compute_noise_with_cuts(in_val_in, av, idx):
    
    if in_val_in.size == 0:
        return [0, 0]
    
    in_val = in_val_in.values
    
    list_cuts = [x[0] for x in idx[1:]]
            
    out_val_nocorr = in_val - moving_average(in_val, av)
    
    noise = out_val_nocorr[:]
    
    if noise.size>av:        
        for i in list_cuts:
            if noise.size>int(i-av/2):     # only if data reaches cut cut
                if noise.size>int(i+av/2):     # only if there is data after cut
                     # this removes noise around cuts
                    noise[int(i-av/2):int(i+av/2)] = np.zeros(av)   
                else:
                    noise[int(i-av/2):noise.size] = np.zeros(noise.size - int(i-av/2))   
            
    out_val = rms(noise)
    
    return [noise, out_val]
    
def outliers_Z (in_vals, n_std = 1):
    
    outliers = []
    indices = []
    
    threshold = n_std
    mean_1 = np.mean(in_vals)
    std_1 =np.std(in_vals)
    
    for idx, y in enumerate(in_vals):
        z_score= (y - mean_1)/std_1 
        if np.abs(z_score) > threshold:
            outliers.append(y)
            indices.append(idx)
            
    return [outliers, indices]
    
def outliers_IQR(in_vals, factor = 1.5):
    
    outliers = []
    
    sorted(in_vals)
    
    q1, q3= np.percentile(in_vals,[25,75])
    
    iqr = q3 - q1
    
    lower_bound = q1 - (factor * iqr)
    upper_bound = q3 + (factor * iqr)
    
    for y in in_vals:
        if y < lower_bound or y > upper_bound:
            outliers.append(y)
    return outliers

def outliers_Z_modified(in_vals, thres = 3.5):
    
    in_vals = np.array(in_vals)
    
    threshold = thres

    median_y = np.median(in_vals)
    median_absolute_deviation_y = np.median([np.abs(y - median_y) for y in in_vals])
    modified_z_scores = [0.6745 * (y - median_y) / median_absolute_deviation_y
                         for y in in_vals]
    return in_vals[np.where(np.abs(modified_z_scores) > threshold)]


def outliers_fixed(in_vals, thres = 0.1):
    
    in_vals = np.array(in_vals)
    
    return in_vals[np.where(in_vals > thres)]

    
def create_dir_safe(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        
        

def f_test(X, Y):
    
    varX = np.std(X)**2
    varY = np.std(Y)**2
    
    dofX = len(X)-1
    dofY = len(Y)-1
    
    F = min([varX, varY])/max([varX, varY])
    
    p_value = stats.f.cdf(F, dofX, dofY)
    
    return p_value
