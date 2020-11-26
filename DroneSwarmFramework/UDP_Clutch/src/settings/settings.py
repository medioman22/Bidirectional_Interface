#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 16:56:28 2020

@author: lis
"""
#####################
###  HRI MAPPING  ###
#####################

#####################################################

import context

from sklearn.linear_model import LinearRegression
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import (RBF)
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVR
from sklearn.svm import NuSVR

import utilities.HRI as HRI

import numpy as np
import os
import datetime
import configparser
import logging


def get_settings():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.ini'))

    def parse_ini(s):
        if s == 'True':
            return True
        if s == 'False':
            return False
        try:
            out = float(s)
            if out == int(out):
                return int(out)
            else:
                return out
        except:
            return s
    
    ####################################################

    settings = {}
    for i in config['basic']:
        settings[i] = parse_ini(config['basic'][i])
    for i in config['mapping']:
        settings[i] = parse_ini(config['mapping'][i])
    for i in config['communication']:
        settings[i] = parse_ini(config['communication'][i])
    for i in config['debug']:
        settings[i] = parse_ini(config['debug'][i])
    
    ####################################################

    for i in config['input_motive']:
        settings[i] = parse_ini(config['input_motive'][i])
    for i in config['input_IMUs']:
        settings[i] = parse_ini(config['input_IMUs'][i])
    
    ####################################################

    settings['imu_ID'] = {}
    for i in config['IMU_ID']:
        settings['imu_ID'][i] = parse_ini(config['IMU_ID'][i])
    
    ####################################################
    
    # if [n_readings] not defined, acquire indefintely
    if settings['n_readings'] == 0:
        settings['n_readings'] = np.inf

    ###

    motive_used_body_parts = {'upper_body':[3, 6, 7, 8, 9, 10, 11, 12, 13]}
    motive_kinematic_chain = {'upper_body':[0, 3, 6, 7, 8, 3, 10, 11, 12]}
    body_parts_code = {'upper_body':{3 : 'torso',
                                    6 : 'left shoulder',
                                    7 : 'left arm',
                                    8 : 'left forearm',
                                    9 : 'left hand',
                                    10 : 'right shoulder',
                                    11 : 'right arm',
                                    12 : 'right forearm',
                                    13 : 'right hand'
                                    }
                        }

    if settings['input_device'] == 'motive':
        settings['used_body_parts'] = motive_used_body_parts[settings['motive_body_representation']]
        settings['kinematic_chain'] = motive_kinematic_chain[settings['motive_body_representation']]
        settings['body_parts_code'] = body_parts_code[settings['motive_body_representation']]

        settings['n_rigid_bodies_in_skeleton'] = len(settings['used_body_parts'])

    imus_kinematic_chain = {'upper_body':[0, 1, 2, 3, 4, 0, 6, 7, 8],
                            'full_body_7':[0, 1, 2, 3, 0, 5, 6],
                            'torso_arm':[0, 1, 2, 3, 4],
                            'arm':[0, 1, 2, 3],
                            'arm_no_shoulder':[0, 1, 2],
                            'forearm':[0, 1],
                            'two_hands':[0, 0],
                            'single':[0]}
                            
    if settings['input_device'] == 'imus':

        settings['kinematic_chain'] = imus_kinematic_chain[settings['imu_body_representation']]

        settings['used_body_parts'] = list(range(1,len(settings['kinematic_chain'])+1))

    ###

    # options : 'roll', 'pitch', both (list)
    settings['outputs_no_pll'] = ['roll', 'pitch']
    # set pll outputs
    settings['outputs'] = [x + '_pll' for x in settings['outputs_no_pll']] ### TOFIX

    ###
    if settings['separate_regressors']:
        settings['regression_outputs'] = settings['outputs']
    else:
        settings['regression_outputs'] = ['all']

    ###
        
    # working folder depends on pc
    if settings['location'] == 'windows':
        # Windows folder
        settings['data_folder'] = 'G:\\My Drive\\Matteo\\EPFL\\LIS\\PhD\\Natural_Mapping\\DATA\\acquired_data\\Experimental'
    if settings['location'] == 'dronedome':
        # DroneDome folder
        settings['data_folder'] = 'D:\\LIS\\Matteo\\DATA\\acquired_data'
    if settings['location'] == 'mac':
        # mac folder
        settings['data_folder'] = '/Volumes/GoogleDrive/My Drive/Matteo/EPFL/LIS/PhD/__Personalized_Mapping/DATA/acquired_data'

    settings['subject_folder'] = os.path.normpath(os.path.join(settings['data_folder'], HRI.file_name(settings)))

    settings['control_folder'] = os.path.normpath(os.path.join(settings['subject_folder'], 'control_data'))

    settings['home_folder'] = os.path.dirname(os.path.realpath(__file__))

    settings['plot_folder'] = os.path.normpath(os.path.join(settings['subject_folder'], 'plots'))

    HRI.create_dir_safe(settings['subject_folder'])
    HRI.create_dir_safe(settings['control_folder'])
    HRI.create_dir_safe(settings['home_folder'])
    HRI.create_dir_safe(settings['plot_folder'])

    ###

    settings['filename'] = datetime.datetime.now().strftime("%Y_%b_%d_%I_%M_%S%p")

    ###

    regressors = get_regressors()
    settings['regressor'] = regressors[settings['regressor_settings']]

    ### headers

    control_history_header = np.char.array([ 'roll', 'pitch'])

    motive_header = np.array([])

    motive_header_base = np.char.array([ 'ID', 'pos_x', 'pos_y', 'pos_z', 'quat_x', 'quat_y', 'quat_z', 'quat_w'])

    motive_regression_header = np.array([])

    motive_regression_header_base = np.char.array([ 'ID', 'pos_x', 'pos_y', 'pos_z', 'quat_x', 'quat_y', 'quat_z', 'quat_w', 'roll', 'pitch', 'yaw'])

    for i in range(settings['n_rigid_bodies_in_skeleton']):

        n = np.char.array([('_' + str(i+1))])

        if i==0:
            motive_header = motive_header_base + (n)
            if i+1 in settings['used_body_parts']:
                motive_regression_header = motive_regression_header_base + (n)
        else:
            motive_header = np.r_[motive_header, motive_header_base + (n)]
            if i+1 in settings['used_body_parts']:
                motive_regression_header = np.r_[motive_regression_header, motive_regression_header_base + (n)]

    settings['headers'] = {}

    if settings['robot'] in ['Fixed-wing (fixed speed)', 'Fixed-wing']:
        unity_header_calib = np.char.array([ 'input1', 'input2', 'input3', 'input4', 'roll', 'pitch', 'yaw', 'roll_rate', 'pitch_rate', 'yaw_rate', 'vel_x', 'vel_y', 'vel_z', 'vel_semiloc_x', 'vel_semiloc_y', 'vel_semiloc_z', 'corr_roll', 'corr_pitch', 'pos_x', 'pos_y', 'pos_z', 'rot_x', 'rot_y', 'rot_z', 'rot_w', 'speed', 'timestamp', 'state', 'maneuver', 'maneuver duration', 'maneuver max amplitude', 'instance', 'loop counter' ])

    elif settings['robot'] in ['Quadrotor']:
        unity_header_calib = np.char.array([ 'input1', 'input2', 'input3', 'input4', 'pos_x', 'pos_y', 'pos_z', 'quat_x', 'quat_y', 'quat_z', 'quat_w', 'roll', 'pitch', 'yaw', 'timestamp', 'state', 'maneuver', 'maneuver duration', 'maneuver max amplitude', 'instance', 'loop counter' ])

    settings['headers']['remote'] = np.char.array([ 'remote1', 'remote2', 'remote3', 'remote4' ])
    settings['headers']['imu'] = np.char.array([ 'roll_imu', 'pitch_imu', 'yaw_imu' ])
    settings['headers']['imus_base'] =  np.char.array([ 'ID', 'roll', 'pitch', 'yaw', 'quat_x', 'quat_y', 'quat_z', 'quat_w']) # it's built dinamically
    settings['headers']['motive'] = np.array(motive_header)
    

    settings['headers']['unity'] = np.array(unity_header_calib)

    settings['headers']['motive_calib'] = np.r_[settings['headers']['motive'], settings['headers']['unity']]

    settings['headers']['remote_calib'] = np.r_[settings['headers']['remote'], settings['headers']['unity']]

    settings['headers']['imu_calib'] = np.r_[settings['headers']['imu'], settings['headers']['unity']]

    settings['headers']['control_history'] = control_history_header

    ###
    
    settings['headers']['imus'] = settings['headers']['imus_base'] + '_1'

    if settings['input_device'] == 'motive':
        settings['headers']['calib'] = settings['headers']['motive_calib']
    elif settings['input_device'] == 'remote':
        settings['headers']['calib'] = settings['headers']['remote_calib']
    elif settings['input_device'] == 'imu':
        settings['headers']['calib'] = settings['headers']['imu_calib']
    elif settings['input_device'] == 'imus':
        for i in settings['used_body_parts'][1:]:                
            settings['headers']['imus'] = np.r_[settings['headers']['imus'], settings['headers']['imus_base'] + '_' + (str(i))]

        settings['headers']['calib'] = np.r_[settings['headers']['imus'], settings['headers']['unity']]

    settings['headers']['calib'] = settings['headers']['calib'].reshape(1, settings['headers']['calib'].size)

    ###

    if settings['input_device'] == 'motive':
        settings['headers']['history'] = settings['headers']['motive']
    elif settings['input_device'] == 'remote':
        settings['headers']['history'] = settings['headers']['remote']
    elif settings['input_device'] == 'imu':
        settings['headers']['history'] = settings['headers']['imu']

    ### debug

    if settings['logging_level'] == 'DEBUG':
        settings['logging_level'] = logging.DEBUG
    elif settings['logging_level'] == 'INFO':
        settings['logging_level'] = logging.INFO
    elif settings['logging_level'] == 'WARNING':
        settings['logging_level'] = logging.WARNING
    elif settings['logging_level'] == 'ERROR':
        settings['logging_level'] = logging.ERROR
    elif settings['logging_level'] == 'CRITICAL':
        settings['logging_level'] = logging.CRITICAL

    return settings


def get_sockets():
    
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.ini'))

    def parse_ini(s):
        if s == 'True':
            return True
        if s == 'False':
            return False
        try:
            out = float(s)
            if out == int(out):
                return int(out)
            else:
                return out
        except:
            return s

    IPs = {}
    for i in config['IPs']:
        IPs[i] = parse_ini(config['IPs'][i])
    ports = {}
    for i in config['ports']:
        ports[i] = parse_ini(config['ports'][i])

    ###

    sockets = {}

    ## open

    sockets['read_unity_flag'] = None
    sockets['write_unity_sk'] = None
    sockets['read_unity_control'] = None
    sockets['read_unity_info'] = None
    sockets['read_motive_sk'] = None
    sockets['read_imu'] = None
    sockets['read_imus'] = None

    sockets['motive'] = {'IP' : IPs['motive'], 'PORT' : ports['motive']}  # Local MOTIVE client, arbitrary non-privileged port

    sockets['imu'] = {'IP' : IPs['imu'], 'PORT' : ports['imu']}  # Local MOTIVE client, arbitrary non-privileged port
    sockets['imus'] = {'IP' : IPs['imus'], 'PORT' : ports['imus']}  # Local MOTIVE client, arbitrary non-privileged port

    ## unity

    sockets['unity_flag'] = {'IP' : IPs['unity_flag'], 'PORT' : ports['unity_flag']}  # Local UNITY client, arbitrary non-privileged port
    sockets['unity_calib'] = {'IP' : IPs['unity_calib'], 'PORT' : ports['unity_calib']}  # Local UNITY client, arbitrary non-privileged port
    sockets['unity_info'] = {'IP' : IPs['unity_info'], 'PORT' : ports['unity_info']}  # Local UNITY client, arbitrary non-privileged port
    sockets['unity_write_sk'] = {'IP' : IPs['unity_write_sk'], 'PORT' : ports['unity_write_sk']}  # Local UNITY client, arbitrary non-privileged port
    sockets['unity_write_sk_client'] = {'IP' : IPs['unity_write_sk_client'], 'PORT' : ports['unity_write_sk_client']}  # Local UNITY client, arbitrary non-privileged port
    #        sockets['unity_write_sk_client'] = {'IP' : "192.168.1.167", 'PORT' : 5000}  # hardware

    sockets['unity_sk_client'] = {'IP' : IPs['unity_sk_client'], 'PORT' : ports['unity_sk_client']}  # Local UNITY client, arbitrary non-privileged port

    return sockets


def get_feat_names():
    
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.ini'))

    def parse_ini(s):
        if s == 'True':
            return True
        if s == 'False':
            return False
        try:
            out = float(s)
            if out == int(out):
                return int(out)
            else:
                return out
        except:
            return s

    settings = {}
    for i in config['basic']:
        settings[i] = parse_ini(config['basic'][i])
    for i in config['mapping']:
        settings[i] = parse_ini(config['mapping'][i])
    for i in config['communication']:
        settings[i] = parse_ini(config['communication'][i])
    for i in config['debug']:
        settings[i] = parse_ini(config['debug'][i])

    ###

    feat_names = {}
    feat_names['positions'] = ['pos_x', 'pos_y', 'pos_z']
    feat_names['quaternions'] = ['quat_x', 'quat_y', 'quat_z', 'quat_w']
    feat_names['euler'] = ['roll', 'pitch', 'yaw']

    feat_names['remote'] = ['remote1', 'remote2', 'remote3', 'remote4']  # can think of adding some buttons
    feat_names['imu'] = ['roll_imu', 'pitch_imu', 'yaw_imu']

    return feat_names

def get_regressors():

    regressors = {}
    regressors['one'] = [make_pipeline(MultiOutputRegressor(LinearRegression())), # linear
            make_pipeline(MLPRegressor(128, activation = 'relu', solver = 'adam', max_iter = 1000))] # MLP

    regressors['reduced'] = [make_pipeline(MultiOutputRegressor(LinearRegression())), # linear
            make_pipeline(MLPRegressor(8, activation = 'relu', solver = 'sgd', max_iter = 1000, early_stopping = True)),
            make_pipeline(MLPRegressor(32, activation = 'relu', solver = 'sgd', max_iter = 1000, early_stopping = True)),
            make_pipeline(MLPRegressor(64, activation = 'relu', solver = 'sgd', max_iter = 1000, early_stopping = True)),
            make_pipeline(MLPRegressor(128, activation = 'relu', solver = 'sgd', max_iter = 1000, early_stopping = True))] # MLP

    grid_hl = [8, 32, 64, 128, (8,8), (32,8), (64,8), (128,8), (8, 8, 8), (32, 8, 8), (64, 8, 8), (128, 8, 8)]
    grid_solver = ['lbfgs', 'sgd', 'adam']
    grid_alpha = [0.0001, 0.001, 0.01, 0.1, 1, 10]
    grid_lr = [0.0001, 0.001, 0.01]

    regs_search = [make_pipeline(MultiOutputRegressor(LinearRegression()))] # linear

    for i in grid_hl:
        for ii in grid_solver:
            for iii in grid_alpha:
                for iiii in grid_lr:
                    regs_search.append(make_pipeline(MLPRegressor(hidden_layer_sizes = i, solver = ii, alpha = iii, learning_rate_init = iiii)))

    regressors['full'] = [make_pipeline(MultiOutputRegressor(LinearRegression())), # linear
            make_pipeline(MLPRegressor(10, activation = 'relu', solver = 'lbfgs')),
            make_pipeline(MLPRegressor(25, activation = 'relu', solver = 'lbfgs')),
            make_pipeline(MLPRegressor(50, activation = 'relu', solver = 'lbfgs')),
            make_pipeline(MLPRegressor(100, activation = 'relu', solver = 'lbfgs')),
            make_pipeline(MLPRegressor(10, activation = 'relu', solver = 'adam')),
            make_pipeline(MLPRegressor(25, activation = 'relu', solver = 'adam')),
            make_pipeline(MLPRegressor(50, activation = 'relu', solver = 'adam')),
            make_pipeline(MLPRegressor(100, activation = 'relu', solver = 'adam')), # MLP
            make_pipeline(MultiOutputRegressor(SVR(kernel='rbf', C=1))),
            make_pipeline(MultiOutputRegressor(SVR(kernel='linear', C=1))),
            make_pipeline(MultiOutputRegressor(SVR(kernel='poly', C=1))),
            make_pipeline(MultiOutputRegressor(SVR(kernel='rbf', C=10))),
            make_pipeline(MultiOutputRegressor(SVR(kernel='linear', C=10))),
            make_pipeline(MultiOutputRegressor(SVR(kernel='poly', C=10))),
            make_pipeline(MultiOutputRegressor(SVR(kernel='rbf', C=100))),
            make_pipeline(MultiOutputRegressor(SVR(kernel='linear', C=100))),
            make_pipeline(MultiOutputRegressor(SVR(kernel='poly', C=100)))] # SVM

    regressors['GP_one'] = [make_pipeline(MultiOutputRegressor(LinearRegression())), # linear
                    make_pipeline(MultiOutputRegressor(GaussianProcessRegressor(kernel=None,
                                            alpha=1e-10,
                                            optimizer='fmin_l_bfgs_b',
                                            n_restarts_optimizer=0,
                                            normalize_y=False,
                                            copy_X_train=True,
                                            random_state=None)))]

    regressors['GP'] = [make_pipeline(MultiOutputRegressor(LinearRegression())), # linear
                    make_pipeline(MultiOutputRegressor(GaussianProcessRegressor(kernel=None,
                                            alpha=1e-10,
                                            optimizer='fmin_l_bfgs_b',
                                            n_restarts_optimizer=0,
                                            normalize_y=False,
                                            copy_X_train=True,
                                            random_state=None))),
                    make_pipeline(MultiOutputRegressor(GaussianProcessRegressor(kernel=None,
                                            alpha=1e-5,
                                            optimizer='fmin_l_bfgs_b',
                                            n_restarts_optimizer=0,
                                            normalize_y=False,
                                            copy_X_train=True,
                                            random_state=None))),
                    make_pipeline(MultiOutputRegressor(GaussianProcessRegressor(kernel=None,
                                            alpha=1e-2,
                                            optimizer='fmin_l_bfgs_b',
                                            n_restarts_optimizer=0,
                                            normalize_y=False,
                                            copy_X_train=True,
                                            random_state=None))),
                    make_pipeline(MultiOutputRegressor(GaussianProcessRegressor(kernel=None,
                                            alpha=1e-10,
                                            optimizer='fmin_l_bfgs_b',
                                            n_restarts_optimizer=1,
                                            normalize_y=False,
                                            copy_X_train=True,
                                            random_state=None))),
                    make_pipeline(MultiOutputRegressor(GaussianProcessRegressor(kernel=None,
                                            alpha=1e-10,
                                            optimizer='fmin_l_bfgs_b',
                                            n_restarts_optimizer=0,
                                            normalize_y=True,
                                            copy_X_train=True,
                                            random_state=None))),
                    make_pipeline(MultiOutputRegressor(GaussianProcessRegressor(kernel=None,
                                            alpha=1e-10,
                                            n_restarts_optimizer=0,
                                            normalize_y=False,
                                            copy_X_train=True,
                                            random_state=None))),
                    make_pipeline(MultiOutputRegressor(GaussianProcessRegressor(kernel=None,
                                            alpha=1e-10,
                                            optimizer='fmin_l_bfgs_b',
                                            n_restarts_optimizer=2,
                                            normalize_y=False,
                                            copy_X_train=True,
                                            random_state=None)))]

    regressors['SVR'] = [#make_pipeline(MultiOutputRegressor(LinearRegression())), # linear
                    make_pipeline(MultiOutputRegressor(SVR(kernel='rbf', C=10)))]

    regressors['LIN'] = [make_pipeline(MultiOutputRegressor(LinearRegression()))] # linear

    return regressors

######

if __name__ == '__main__':
    get_settings()
    get_sockets()
    get_feat_names()
    get_regressors()