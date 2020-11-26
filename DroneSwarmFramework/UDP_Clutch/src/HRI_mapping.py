#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 10:23:24 2018

@author: matteomacchini
"""


########################################################

import matplotlib.pyplot as plt
from matplotlib.pylab import savefig
plt.close
import numpy as np
import os
import pandas as pd
from sklearn import cross_decomposition
from sklearn import decomposition
from sklearn import metrics
from sklearn.multioutput import MultiOutputRegressor
from sklearn.utils import shuffle
import time

import utilities.HRI as HRI
import quaternion as quat
import libs.quaternion_operations as quat_op
import utilities.utils as utils

from settings.settings import get_settings
from settings.settings import get_feat_names
from settings.settings import get_regressors

import utilities.my_plots as my_plots

import logging


########################################################

settings = get_settings()
logging.basicConfig(level=settings['logging_level'])

feat_names = get_feat_names()
regressors = get_regressors()

_PLOT = {}
_DEBUG = {}
_DEBUG['process'] = {}


class HRI_mapping():


    """"""""""""
    """ DATA """
    """"""""""""


    """"""""""""""""""""""""
    """ CLASS  FUNCTIONS """
    """"""""""""""""""""""""


    """"""""""""""""""""""""
    """ PUBLIC FUNCTIONS """
    """"""""""""""""""""""""


    def delete_all_clean_data(self):

        delete_all_clean_data()


########################################################


def import_data():
    '''Imports data from a calibration dataset'''

    # list folders 
    folder = settings['subject_folder']

    # list files
    files = os.listdir(folder)
    files_new = [x for x in files if 'inst' in x]
    
    # keep clean
    temp = [w[:-4] for w in files_new]
    ext = files_new[0][-4:]
    files_processed = [x + ext for x in temp if 'CLEAN' in x]
    files_unprocessed = [x + ext for x in temp if 'CLEAN' not in x]

    if len(files_processed) == len(files_unprocessed):    # data are processed
        keep = files_processed
        clean = True
    else:
        keep = files_unprocessed   
        clean = False 

    # import dataframes
    motion_data_unprocessed = []

    for i in keep:

        file_path = os.path.join(folder, i)
        motion_data_unprocessed.append({'df':pd.read_csv(file_path), 'isclean' : clean, 'filename' : i})

        logging.info('Imported dataset "{}"'.format(i))

    return motion_data_unprocessed


########################################################


def process_data(unprocessed_data = None, motion_data_man_list = None, param = {}):
    '''Processes data from a calibration dataset'''

    # process if not clean
    if not unprocessed_data[0]['isclean']:
        unprocessed_data1 = _preprocess_data_input(unprocessed_data) 

    # get list of maneuvers
    man_list = ['just_left','just_right','just_up','just_down','up_left','up_right','down_left','down_left','straight']
    
    filenames = [x['filename'] for x in unprocessed_data]
    motion_data_man_list = [x for x in man_list if any(x in y for y in filenames)]

    # merge dataframes
    logging.info('merging...')

    [motion_data, motion_data_idx] = HRI.merge_data_df(unprocessed_data, settings['fit_un_to_max'], settings['outputs'])

    #normalize
    logging.info('normalizing...')

    av = []
    std = []

    for j in list(motion_data):

        # if not an output
        if j not in settings['outputs'] and j not in settings['outputs_no_pll']:

            # normalize data and store parameters
            [array_norm, norm_param_t] = utils.normalize_array(motion_data[j])
            motion_data[j] = array_norm

            av.append(norm_param_t[0])
            std.append(norm_param_t[1])
        else:
            # don't normalize and store [av = 0, std = 1]
            av.append(0)
            std.append(1)

            
    param = pd.DataFrame([av, std], columns = list(motion_data))  ### TOFIX

    # store debug data
    _DEBUG['param'] = param
    _DEBUG['process']['df_norm'] = motion_data

    return [motion_data, motion_data_idx, motion_data_man_list, param]


########################################################


def _preprocess_data_input(unprocessed_data):
    '''Preprocesses data from a calibration dataset'''

    mot_data_ret = []

    for idx,mot_data in enumerate(unprocessed_data):

        logging.info('PROCESSING unclean data from file {} ...'.format(mot_data['filename']))
        
        # remove fictional and useless data
        logging.info('   removing fictional and useless data...')

        if settings['input_device'] in ['motive', 'imus']:
            used_str = ['_' + str(x) for x in settings['used_body_parts']]

        elif settings['input_device'] in ['motive', 'imus']:
            used_str = [settings['input_device']]

        my_cols = [col for col in mot_data['df'].columns if any(y in col for y in used_str)]
        my_cols.extend(settings['outputs_no_pll'])
        mot_data['df'] =  mot_data['df'][my_cols]

        _DEBUG['process']['df_base'] = mot_data['df']

        # remove initial data
        logging.info('   removing initial data...')

        mot_data['df'] = mot_data['df'].drop(mot_data['df'].index[:settings['init_values_to_remove']])
        mot_data['df'].index = mot_data['df'].index - settings['init_values_to_remove']

        _DEBUG['process']['df_noinit'] = mot_data['df']

        # if motion data
        if settings['input_device'] in ['motive', 'imus']:
            
            # compute relative angles
            logging.info('   relative angles...')
        
            mot_data['df'] = _relativize_df(mot_data['df'], idx)

            _DEBUG['process']['df_rel'] = mot_data['df']

            # unbias angles
            logging.info('   unbias angles...')

            mot_data['df'] = _unbias_df(mot_data['df'], idx)

            _DEBUG['process']['df_unb'] = mot_data['df']

            # compute euler angles
            logging.info('   compute euler angles...')

            mot_data['df'] = _compute_ea_df(mot_data['df'], idx)

            _DEBUG['process']['df_eul'] = mot_data['df']

        # sync input-output
        logging.info('   syncing datasets...')

        mot_data['df'] = _pll_df(mot_data['df'], idx)

        _DEBUG['process']['df_pll'] = mot_data['df']

        # save clean data to file
        mot_data['df'].to_csv(os.path.join(settings['subject_folder'], 'CLEAN_' + mot_data['filename']), index=False)

        mot_data_ret.append(mot_data)

    return mot_data_ret


########################################################


def _relativize_df(df, idx):
    ''' Substracts to an orientation in a rigid body the orientation of the upstram rigid body in the kinematic chain for all datasets '''

    for i in range(0, len(settings['used_body_parts'])):
        df = relativize_angles(settings['used_body_parts'][i], settings['kinematic_chain'][i], df, idx)

    return df


########################################################


_PLOT['relativize_angles'] = []

def relativize_angles(angles_to_correct, with_respect_to, dataframe, idx):
    ''' Substracts to an orientation in a rigid body the orientation of the upstram rigid body in the kinematic chain '''

    global _PLOT
    
    dataframe_out = pd.DataFrame.copy(dataframe)

    if with_respect_to == 0:
        return dataframe_out
        
    # get data index
    str_abs = {}
    str_ref = {}

    for i in ['x', 'y', 'z', 'w']:
        str_abs[i] = 'quat_' + i + '_' + str(angles_to_correct)
        str_ref[i] = 'quat_' + i + '_' + str(with_respect_to)

    for i in range(0, dataframe.shape[0]):
        # get quaternions
        reference = np.quaternion(dataframe[str_ref['w']].values[i], dataframe[str_ref['x']].values[i], dataframe[str_ref['y']].values[i], dataframe[str_ref['z']].values[i])
        absolute = np.quaternion(dataframe[str_abs['w']].values[i], dataframe[str_abs['x']].values[i], dataframe[str_abs['y']].values[i], dataframe[str_abs['z']].values[i])

        # implement inverse rotation
        relative = absolute/reference

        # save back to dataframe
        dataframe_out[str_abs['w']].values[i] = relative.w
        dataframe_out[str_abs['x']].values[i] = relative.x
        dataframe_out[str_abs['y']].values[i] = relative.y
        dataframe_out[str_abs['z']].values[i] = relative.z

    _PLOT['relativize_angles'].append({})
    _PLOT['relativize_angles'][-1]['p1'] = dataframe['quat_w_' + str(angles_to_correct)].values
    _PLOT['relativize_angles'][-1]['p2'] = dataframe['quat_w_' + str(with_respect_to)].values
    _PLOT['relativize_angles'][-1]['p3'] = dataframe_out['quat_w_' + str(angles_to_correct)].values
    _PLOT['relativize_angles'][-1]['s1'] = 'angle {} respect to {}'.format(angles_to_correct, with_respect_to) 

    tit = 'relativize_angles_plot_{}_angle_{}_to_{}.pdf'.format(idx, angles_to_correct, with_respect_to)
    _PLOT['relativize_angles'][-1]['tit'] = tit

    if settings['plots']:
        relativize_angles_plot(_PLOT['relativize_angles'][-1], save=True)
            
    return dataframe_out


########################################################



def relativize_angles_plot(vals, save=False):

    plt.figure()
    plt.plot(vals['p1'], label="absolute")
    plt.plot(vals['p2'], label="reference")
    plt.plot(vals['p3'], label="relative")
    plt.grid()
    plt.legend()
    plt.title(vals['s1'])

    if save:
        fol = os.path.join(settings['plot_folder'], 'relitivize')
        HRI.create_dir_safe(fol)
        savefig(os.path.join(fol, vals['tit']), bbox_inches='tight')
        plt.close


########################################################


def _unbias_df(df, idx):
    ''' Substracts to an orientation in a rigid body the initial orientation such that it is zero in the first frame for all datasets '''

    for i in settings['used_body_parts']:
        df = _unbias(i, df, idx)

    return df
        

########################################################


_PLOT['unbias'] = []

def _unbias(limb, dataframe, idx):
    ''' Substracts to an orientation in a rigid body the initial orientation such that it is zero in the first frame '''

    global _PLOT

    dataframe_out = pd.DataFrame.copy(dataframe)

    # get data index
    str_abs = {}

    for i in ['x', 'y', 'z', 'w']:
        str_abs[i] = 'quat_' + i + '_' + str(limb)


    # get reference quaterion
    reference = np.quaternion(dataframe[str_abs['w']].values[0], dataframe[str_abs['x']].values[0], dataframe[str_abs['y']].values[0], dataframe[str_abs['z']].values[0])

    for i in range(0, dataframe.shape[0]):
        # get quaternions
        absolute = np.quaternion(dataframe[str_abs['w']].values[i], dataframe[str_abs['x']].values[i], dataframe[str_abs['y']].values[i], dataframe[str_abs['z']].values[i])

        # implement inverse rotation
        relative= absolute/reference

        # save back to dataframe
        dataframe_out[str_abs['w']].values[i] = relative.w
        dataframe_out[str_abs['x']].values[i] = relative.x
        dataframe_out[str_abs['y']].values[i] = relative.y
        dataframe_out[str_abs['z']].values[i] = relative.z


    if settings['input_device'] == 'leap':
        _PLOT['unbias'].append({})
        _PLOT['unbias'][-1]['p1'] = dataframe['quat_w_' + str((limb//20)+1) + '_' + str((limb%20)+1)].values
        _PLOT['unbias'][-1]['p2'] = dataframe_out['quat_w_' + str((limb//20)+1) + '_' + str((limb%20)+1)].values
        _PLOT['unbias'][-1]['s1'] = 'angle ' + str((limb//20)+1) + '_' + str((limb%20)+1)
        tit = 'unbias_plot_{}_angle_{}.pdf'.format(idx, str((limb//20)+1) + '_' + str((limb%20)+1))
        _PLOT['unbias'][-1]['tit'] = tit
    else:
        _PLOT['unbias'].append({})
        _PLOT['unbias'][-1]['p1'] = dataframe['quat_w_' + str(limb)].values
        _PLOT['unbias'][-1]['p2'] = dataframe_out['quat_w_' + str(limb)].values
        _PLOT['unbias'][-1]['s1'] = 'angle ' + str(limb)
        tit = 'unbias_plot_{}_angle_{}.pdf'.format(idx, limb)
        _PLOT['unbias'][-1]['tit'] = tit
    if settings['plots']:
        _unbias_plot(_PLOT['unbias'][-1], save=True)

    return dataframe_out


########################################################


def _unbias_plot(vals, save=False):

    plt.figure()
    plt.plot(vals['p1'], label="old")
    plt.plot(vals['p2'], label="new")
    plt.grid()
    plt.legend()
    plt.title(vals['s1'])

    if save:
        fol = os.path.join(settings['plot_folder'], 'unbias')
        HRI.create_dir_safe(fol)
        savefig(os.path.join(fol, vals['tit']), bbox_inches='tight')
        plt.close


########################################################


def _compute_ea_df(df, idx):
    ''' Compute Euler Angles from Quaternions for all datasets '''

    for i in settings['used_body_parts']:
        df = _compute_euler_angles(i, df, idx)

    return df


########################################################


_PLOT['compute_euler_angles'] = []

def _compute_euler_angles(limb, dataframe, idx):
    ''' Compute Euler Angles from Quaternions for all datasets '''

    global _PLOT

    dataframe_out = pd.DataFrame.copy(dataframe)

    eul = []

    # get data index
    str_abs = {}

    for i in ['x', 'y', 'z', 'w']:
        str_abs[i] = 'quat_' + i + '_' + str(limb)

    for i in range(0, dataframe.shape[0]):

        # get quaternions
        q = np.quaternion(dataframe[str_abs['w']].values[i], dataframe[str_abs['x']].values[i], dataframe[str_abs['y']].values[i], dataframe[str_abs['z']].values[i])

        # compute Euler Angles
        eul.append(quat_op.Q2EA(np.array([q.w, q.x, q.y, q.z]), EulerOrder="zyx", ignoreAllChk=True)[0])

    # WAS FILTERED
    # dataframe_out['roll_' + str(limb)] = pd.Series(utils.moving_average(np.array([x[2] for x in eul]), 1), index=dataframe_out.index)
    # dataframe_out['pitch_' + str(limb)] = pd.Series(utils.moving_average(np.array([x[0] for x in eul]), 1), index=dataframe_out.index)
    # dataframe_out['yaw_' + str(limb)] = pd.Series(utils.moving_average(np.array([x[1] for x in eul]), 1), index=dataframe_out.index)

    dataframe_out['roll_' + str(limb)] = pd.Series(np.array([x[2] for x in eul]), index=dataframe_out.index)
    dataframe_out['pitch_' + str(limb)] = pd.Series(np.array([x[0] for x in eul]), index=dataframe_out.index)
    dataframe_out['yaw_' + str(limb)] = pd.Series(np.array([x[1] for x in eul]), index=dataframe_out.index)

    _PLOT['compute_euler_angles'].append({})
    _PLOT['compute_euler_angles'][-1]['p1'] = dataframe_out['roll_' + str(limb)].values
    _PLOT['compute_euler_angles'][-1]['p2'] = dataframe_out['pitch_' + str(limb)].values
    _PLOT['compute_euler_angles'][-1]['p3'] = dataframe_out['yaw_' + str(limb)].values
    _PLOT['compute_euler_angles'][-1]['s1'] = 'angle ' + str(limb)

    tit = 'compute_euler_angles{}_angle_{}.pdf'.format(idx, limb)
    _PLOT['compute_euler_angles'][-1]['tit'] = tit

    if settings['plots']:
        _compute_euler_angles_plot(_PLOT['compute_euler_angles'][-1], save=True)

    return dataframe_out


########################################################


def _compute_euler_angles_plot(vals, save=False):
    
    plt.figure()
    plt.plot(vals['p1'], label="roll")
    plt.plot(vals['p2'], label="pitch")
    plt.plot(vals['p3'], label="yaw")
    plt.grid()
    plt.legend()
    plt.title(vals['s1'])

    if save:
        fol = os.path.join(settings['plot_folder'], 'euler')
        HRI.create_dir_safe(fol)
        savefig(os.path.join(fol, vals['tit']), bbox_inches='tight')
        plt.close


########################################################


def _pll(y, y1, init_lim = 50, idx = 0, xvals = None, max_shift = None):
    ''' Synchronizes input y and y1, in terms of starting moment and duration '''

    global _PLOT

    def rescale(y, m_shift, y_init):

        if max_shift>0:
            # align max
            to_add = np.ones(max_shift) * y_init
            y = np.hstack([y[max_shift:], to_add])
        elif max_shift<0:
            # align max
            to_add = np.ones(-max_shift) * y_init
            y = np.hstack([to_add, y[:max_shift]])

        return y

    y_in = y[:]

    # remove initial value
    y_first_val = y[0]
    y1_first_val = y1[0]

    y = y - y_first_val
    y1 = y1 - y1_first_val

    # find initial value
    y_init = np.mean(y[0:init_lim])
    y1_init = np.mean(y1[0:init_lim])

    # find max
    [m, m_i] = utils.find_maxmin(y, absolute = True)
    [m1, m1_i] = utils.find_maxmin_first(y1)

    # prevents bugs from straight manevuers
    if m<1:
        return [y, 0]

    # prevents bugs from straight manevuers with remote (problem when only one value changes)
    if len(np.unique(y1)) <=10:
        return [y, 0]

    # find diff
    y_diff = m - y_init
    y1_diff = m1 - y1_init

    # find 10% indices
    i_10 = np.argmax(abs(y)> 0.1 * y_diff)
    i1_10 = np.argmax(abs(y1)> 0.1 * y1_diff)

    delta = m_i - i_10
    delta1 = m1_i - i1_10

    delta_frac = delta/delta1

    # rescale
    if xvals is None:
        xvals =  np.arange(len(y))*delta_frac

    y = np.interp(xvals, np.arange(len(y)), y)

    # sync max
    [m, m_i] = utils.find_maxmin(y, absolute = True)

    if max_shift is None:
        max_shift = m_i-m1_i

    y = rescale(y, max_shift, y_init)

    # put back initial value
    y = y + y_first_val
    y1 = y1 + y1_first_val

    _PLOT['pll'] = {}
    _PLOT['pll']['p1'] = y_in
    _PLOT['pll']['p2'] = y1 / utils.find_maxmin(y1, absolute = True)[0] * utils.find_maxmin(y, absolute = True)[0]
    _PLOT['pll']['p3'] = y
    _PLOT['pll']['s1'] = 'synchronization_{}'.format(idx)

    tit = 'synchronization_{}.pdf'.format(idx)
    _PLOT['pll']['tit'] = tit

    if settings['plots']:
        _pll_plot(_PLOT['pll'], save=True)

    return [y, [init_lim, xvals, max_shift]]


########################################################


def _pll_plot(vals, save=False):
    plt.figure()
    plt.plot(vals['p1'], label = 'original input')
    plt.plot(vals['p2'], label = 'sync input')
    plt.plot(vals['p3'], label = 'output')

    plt.grid()
    plt.legend()
    plt.title(vals['s1'])

    if save:
        fol = os.path.join(settings['plot_folder'], 'sync')
        HRI.create_dir_safe(fol)
        savefig(os.path.join(fol, vals['tit']), bbox_inches='tight')
        plt.close


########################################################


def _pll_df(df_in, idx):
    ''' Synchronizes all inputs in a df with the outputs, in terms of starting moment and duration '''

    global _DEBUG
    global _PLOT

    def get_array_with_max_variance(arr_list):

        var = [np.std(x)**2 for x in arr_list]

        max_var_arr = arr_list[np.argmax(var)]

        return max_var_arr

    if settings['pll_mode'] == 'variance':

        ### split into inputs and outputs
        out_df = df_in[settings['outputs_no_pll']]

        if settings['input_device'] in ['remote', 'imu']:
            in_df = df_in.drop(settings['outputs_no_pll'], axis=1)
        elif settings['input_device'] in ['motive', 'imus']:
            feats = select_motive_features()    # using only euler angles (for example)
            in_df = df_in[feats]

        # make list of inputs
        in_list = [in_df[x] for x in list(in_df)]

        # use pca to find variable with most variance
        t = time.time()
        pca = decomposition.PCA(n_components=1)
        pca.fit(in_df.values)
        in_max_var1 = pca.transform(in_df.values)
            
        in_max_var = get_array_with_max_variance(in_list)

        _PLOT['pll_df'] = {}
        _PLOT['pll_df']['p1'] = in_max_var
        _PLOT['pll_df']['p2'] = in_max_var1
        _PLOT['pll_df']['s1'] = 'pca_use_for_pll'

        tit = 'pca_use_for_pll.pdf'
        _PLOT['pll_df']['tit'] = os.path.join(settings['subject_folder'], tit)

        in_max_var = in_max_var1

        _DEBUG['in_max_var'] = in_max_var

        # make list of outputs
        out_list = [out_df[x] for x in list(out_df)]

        # find output with max variance
        out_max_var = get_array_with_max_variance(out_list)
        _DEBUG['out_max_var'] = out_max_var

        # reunite df
        df_out = pd.concat([in_df,out_df], axis=1, join='inner')

        # pll
        [pll_main_output, params] = _pll(out_max_var, in_max_var, idx)

        _DEBUG['pll_main_output'] = pll_main_output

        # pll on all outputs
        for i in range(0, len(out_list)):

            ### TODO : in the future we just check the maneuver
            if params != 0:
                [pll_all_output, _] = _pll(out_list[i], in_max_var, idx, params[0], params[1], params[2])
                df_out[settings['outputs'][i]] = pll_all_output
            else:                                                 # meaning that if the pll failed because of a flat output
                df_out[settings['outputs'][i]] = out_list[i]      # we just copy the standard output

            _PLOT['pll_df']['out_list'] = out_list
            _PLOT['pll_df'][i] = {}
            _PLOT['pll_df'][i]['p3'] = in_max_var
            _PLOT['pll_df'][i]['p4'] = out_list[i]
            _PLOT['pll_df'][i]['p5'] = pll_all_output
            _PLOT['pll_df'][i]['s2'] = 'pll_df_{}'.format(i)

            tit = 'pll_df_{}_{}.pdf'.format(idx, i)
            _PLOT['pll_df'][i]['tit'] = tit

        if settings['plots']:
            _pll_df_plot(_PLOT['pll_df'], save=True)

    return df_out


########################################################


def _pll_df_plot(vals, save=False):
    plt.figure()
    plt.plot(vals['p1'], label = 'old pll signal')
    plt.plot(vals['p2'], label = 'pca signal')
    plt.title(vals['s1'])

    plt.grid()
    plt.legend()

    if save:
        fol = os.path.join(settings['plot_folder'], 'sync')
        HRI.create_dir_safe(fol)
        savefig(os.path.join(fol, vals['tit']), bbox_inches='tight')
        plt.close

    for i in range(0, len(vals['out_list'])):
        plt.figure()
        plt.plot(vals[i]['p3'], label="Original input")
        plt.plot(vals[i]['p4'], label="Original output")
        plt.plot(vals[i]['p5'], label="Corrected output")
        plt.title(vals[i]['s2'])

        plt.grid()
        plt.legend()

        if save:
            fol = os.path.join(settings['plot_folder'], 'sync')
            HRI.create_dir_safe(fol)
            savefig(os.path.join(fol, vals[i]['tit']), bbox_inches='tight')
            plt.close


########################################################


def select_motive_features():
    ''' Return a subset of Motive features to be used for the mapping'''

    if settings['features_used'] == 'full':
        feats_in = feat_names['positions'] + feat_names['quaternions'] + feat_names['euler']
    elif settings['features_used'] == 'angles':
        feats_in = feat_names['quaternions'] + feat_names['euler']
    elif settings['features_used'] == 'euler':
        feats_in = feat_names['euler']
    elif settings['features_used'] == 'quaternions':
        feats_in = feat_names['quaternions']

    # find all used features from feat_in
    feats = [x + '_' + str(y) for y in settings['used_body_parts'] for x in feats_in]

    return feats


########################################################


def run_dimensionality_reduction(param, motion_data):
    ''' Compresses input data with a dimensionality reduction algorithm (PCA'''

    global _DEBUG

    # get basic feat_names
    if settings['input_device'] in ['motive', 'imus']:
        feats_all = select_motive_features()

    elif settings['input_device'] in ['remote', 'imu']:
        feats_all = feat_names[settings['input_device']]

    _DEBUG['features_all'] = feats_all

    # select subset
    if settings['dim_reduction']:
        feats = _with_dim_reduction(param, motion_data, feats_all)

    _DEBUG['features_filtered'] = feats

    out = settings['outputs']
    
    dimred = {}
    feats_compressed = {}
    feats_compressed_idx = {}
    # perform the algorithm specified in settings
    for out in settings['regression_outputs']:
        if settings['dimred_style'] == 'pca':
            dimred[out] = decomposition.PCA(n_components=len(out))
            dimred[out].fit(motion_data[feats[out]])
            feats_compressed[out] = dimred[out].transform(motion_data[feats[out]])
        elif settings['dimred_style'] == 'cca':
            dimred[out] = implement_cca(motion_data[feats[out]].values, motion_data[out].values)
            feats_compressed[out] = transform_cca(motion_data[feats[out]].values, dimred[out])

        # compute compressed output
        feats_compressed[out] = np.transpose(feats_compressed[out])

        feats_compressed_idx[out] = []
        for count, i in enumerate(feats_compressed[out]):
            feats_compressed_idx[out] = 'reduced_inputs_{}'.format(out)
            motion_data[feats_compressed_idx[out]] = i

    _DEBUG['features_compressed'] = feats_compressed_idx
        
    return [feats_all, feats, feats_compressed_idx, dimred, motion_data]


########################################################


def implement_cca(x, y):
    ''' Implement CCA between input [x] and output [y], returns CCA function '''

    cca = cross_decomposition.CCA(1)
    cca.fit(x, y.reshape(-1, 1))

    return cca


########################################################


def transform_cca(x, cca):
    ''' Transformes input [x] with CCA function [cca] '''

    output = cca.transform(x)

    return output


########################################################


def _with_dim_reduction(param, motion_data, feats):
    ''' Selects subset of features using quality parameter '''

    global _DEBUG
    global _PLOT
    _PLOT['dim_red'] = {}

    motion = motion_data

    variance_features = {}
    covariance_features_outputs = {}
    signal_rms = {}
    noise_rms = {}
    snr = {}

    # choose if to separate regressors
    outs = settings['regression_outputs']

    variance_features = {}
    signal_rms = {}
    noise_rms = {}
    snr = {}

    for i in feats:
        
        # compute variance
        variance_features[i] = param[i].iloc[1]**2
        # compute snr
        signal_rms[i] = utils.rms(motion[i])
        noise_rms[i] = utils.rms(motion[i] - utils.moving_average(motion[i].values, 50))
        snr[i] = (signal_rms[i]/noise_rms[i])**2 if noise_rms[i] != 0 else 0

    
    covar = {}
    coeff = {}
    covar_sorted_by_value = {}
    coeff_sorted_by_value = {}
    covar_sort = {}
    coeff_sort = {}
    covar_relative = {}
    sum_covar = {}
    coeff_relative = {}
    sum_coeff = {}
    covar_norm = {}
    coeff_norm = {}
    feats_sorted = {}

    feat_suff = {}

    for out in outs:

        covariance_features_outputs[out] = {}

        _PLOT['dim_red'][out] = {}

        # compute var, covar, snr
        for i in feats:
            # compute variance
            variance_features[i] = param[i].iloc[1]**2
            if settings['separate_regressors']:
                covariance_features_outputs[out][i] = np.abs(np.dot(motion[i], motion[out]) * variance_features[i])
            else:
                covariance_features_outputs[out][i] = [np.abs(np.dot(motion[i], motion[x]) * variance_features[i]) for x in settings['outputs']]


        # compute quality metrics
        if settings['separate_regressors']:
            covar[out] = {x:covariance_features_outputs[out][x] for x in covariance_features_outputs[out].keys()}
        else:
            covar[out] = {x:sum(covariance_features_outputs[out][x]) for x in covariance_features_outputs[out].keys()}
        coeff[out] = {x : covar[out][x]*snr[x] for x in covar[out].keys()}

        var_sorted_by_value = sorted(variance_features.items(), key=lambda kv: kv[1], reverse=True)
        snr_sorted_by_value = sorted(snr.items(), key=lambda kv: kv[1], reverse=True)
        covar_sorted_by_value[out] = sorted(covar[out].items(), key=lambda kv: kv[1], reverse=True)
        coeff_sorted_by_value[out] = sorted(coeff[out].items(), key=lambda kv: kv[1], reverse=True)

        # sort
        var_sort = [x[1] for x in var_sorted_by_value]
        snr_sort = [x[1] for x in snr_sorted_by_value]
        covar_sort[out] = [x[1] for x in covar_sorted_by_value[out]]
        coeff_sort[out] = [x[1] for x in coeff_sorted_by_value[out]]

        # return list of used features
        var_relative = var_sort/sum(var_sort)
        sum_var = np.cumsum(var_relative)

        snr_relative = snr_sort/sum(snr_sort)
        sum_snr = np.cumsum(snr_relative)

        covar_relative[out] = covar_sort[out]/sum(covar_sort[out])
        sum_covar[out] = np.cumsum(covar_relative[out])

        coeff_relative[out] = coeff_sort[out]/sum(coeff_sort[out])
        sum_coeff[out] = np.cumsum(coeff_relative[out])

        # normalize
        var_norm = {x: variance_features[x]/sum(var_sort) for x in variance_features.keys()}
        snr_norm = {x: snr[x]/sum(snr_sort) for x in snr.keys()}
        covar_norm[out] = {x: covar[out][x]/sum(covar_sort[out]) for x in covar[out].keys()}
        coeff_norm[out] = {x: coeff[out][x]/sum(coeff_sort[out]) for x in coeff[out].keys()}

        # select quality metric
        if settings['dim_reduction_signal'] == 'variance':
            feats_sorted[out] = [x[0] for x in var_sorted_by_value[out]]
            signal = var_relative
            sum_signal = sum_var
        elif settings['dim_reduction_signal'] == 'covariance':
            feats_sorted[out] = [x[0] for x in covar_sorted_by_value[out]]
            signal = covar_relative[out]
            sum_signal = sum_covar[out]
        elif settings['dim_reduction_signal'] == 'coefficient':
            feats_sorted[out] = [x[0] for x in coeff_sorted_by_value[out]]
            signal = coeff_relative[out]
            sum_signal = sum_coeff[out]

        # select features based on quality metric
        if settings['dim_reduction_var'] == 'threshold':
            feat_suff[out] = feats_sorted[out][0:np.argmax(signal<settings['variance_suff'])]
        elif settings['dim_reduction_var'] == 'sum':
            feat_suff[out] = feats_sorted[out][0:np.argmax(sum_signal>settings['variance_suff'])+1]


        _PLOT['dim_red'][out]['feats_sorted'] = feats_sorted[out]
        _PLOT['dim_red'][out]['var_norm'] = var_norm
        _PLOT['dim_red'][out]['covar_norm'] = covar_norm[out]
        _PLOT['dim_red'][out]['snr_norm'] = snr_norm
        _PLOT['dim_red'][out]['coeff_norm'] = coeff_norm[out]
        _PLOT['dim_red'][out]['out'] = out

        if settings['plots']:
            _dim_red_plot_results(_PLOT['dim_red'][out], save=True)

    if not settings['separate_regressors']:
        # if number is not sufficient compared to output
        if len(feat_suff[out]) < len(settings['outputs']):
            # take at least one per output
            feat_suff[out] = feats_sorted[0:len(settings['outputs'])]

    _PLOT['dim_red']['feats_sorted'] = feats_sorted[out]
    _PLOT['dim_red']['motion'] = motion
    _PLOT['dim_red']['param'] = param
    _PLOT['dim_red']['out'] = out

    if settings['plots']:
        _dim_red_plot_features(_PLOT['dim_red'], save=True)

    # store debug values
    _DEBUG['var'] = variance_features
    _DEBUG['var_relative'] = var_relative
    _DEBUG['sumvar'] = sum_var

    _DEBUG['covar'] = covar
    _DEBUG['covar_relative'] = covar_relative
    _DEBUG['sum_covar'] = sum_covar

    _DEBUG['coeff'] = coeff
    _DEBUG['coeff_relative'] = coeff_relative
    _DEBUG['sum_coeff'] = sum_coeff

    _DEBUG['noise_estimation'] = noise_rms
    _DEBUG['snr'] = snr

    _DEBUG['feats_sorted'] = feats

    return feat_suff


########################################################

def _dim_red_plot_features(vals, save=False):

    for i in vals['feats_sorted']:
        plt.figure()
        for out in settings['outputs']:
            plt.plot(np.arange(1, len(vals['motion'][out]) + 1), vals['motion'][out], label = out)
        plt.plot(np.arange(1, len(vals['motion'][i]) + 1), vals['motion'][i] * vals['param'][i].iloc[1] * 200, label = i)
        tit = 'dim_red_feat_{}'.format(i)
        plt.title(tit)

        plt.grid()
        plt.legend()

        tit = '{}.pdf'.format(i)
        if save:
            fol = os.path.join(settings['plot_folder'], 'dim_red')
            HRI.create_dir_safe(fol)
            savefig(os.path.join(fol, tit), bbox_inches='tight')
            plt.close


########################################################


def _dim_red_plot_results(vals, save=False):

    v = [vals['var_norm'][x] for x in vals['feats_sorted']]
    c = [vals['covar_norm'][x] for x in vals['feats_sorted']]
    s = [vals['snr_norm'][x] for x in vals['feats_sorted']]
    x = [vals['coeff_norm'][x] for x in vals['feats_sorted']]

    plt.figure()

    my_plots.bar_multi([v,c,s,x], legend = ['Variance', 'Covariance', 'SNR', 'Coefficient'], xlabels = vals['feats_sorted'], width = 0.2)
        
    plt.legend()
    tit = 'Feature Selection Coefficient per Feature'
    plt.title(tit)

    tit = 'dim_red_coefficient_{}.pdf'.format(vals['out'])
    if save:
        fol = os.path.join(settings['plot_folder'], 'dim_red')
        HRI.create_dir_safe(fol)
        savefig(os.path.join(fol, tit), bbox_inches='tight')
        plt.close



########################################################


def separate_datasets(motion_data_unprocessed, motion_data, motion_data_idx):
    ''' Separates dataset in maneuvers '''

    ### THESE TWO FUNCTIONS SHOULD BE MERGED
    motion_data_maneuvers = []

    ### TODO: CHANGE STANDARD NAMES FOR MANEUVERS TO AN ENCODED VERSION
    man_list = ['just_left','just_right','just_up','just_down','up_left','up_right','down_left','down_right','straight']

    ### get existing files per maneuver
    filenames = [x['filename'] for x in motion_data_unprocessed]
    motion_data_maneuvers = [x for x in man_list if any(x in y for y in filenames)]

    motion_data_separated = {}

    # separate datasets basd on indices
    for count, i in enumerate(motion_data_maneuvers):
        motion_data_separated[i] = motion_data.iloc[motion_data_idx[count][0]:motion_data_idx[count][1]]

    return [motion_data_maneuvers, motion_data_separated]


########################################################


def augment_on_reduced_data(motion_data_separated):
    ''' Augments data on separated datasets '''

    ### THESE TWO FUNCTIONS SHOULD BE MERGED
    df_in = motion_data_separated

    ### TODO: CHANGE STANDARD NAMES FOR MANEUVERS TO AN ENCODED VERSION
    # define couples: the algorithm will interpolate between these couples
    to_interpolate = [['just_right', 'up_right'],
                      ['just_right', 'down_right'],
                      ['just_left', 'up_left'],
                      ['just_left', 'down_left'],
                      ['just_up', 'up_right'],
                      ['just_down', 'down_right'],
                      ['just_up', 'up_left'],
                      ['just_down', 'down_left']]

    motion_data = {}

    # create datasets for interpolated maneuvers ('right'+'down' -> 'right_down')
    for i in to_interpolate:

        df = []
        outputs = []
        inputs = []

        # extract datasets corresponding to the two maneuvers
        df.append(df_in[i[0]])
        df.append(df_in[i[1]])

        # get shorter and longer dataset
        min_len = min([len(x) for x in df])
        max_len = max([len(x) for x in df])
        longer = df[np.argmax([len(x) for x in df])]
        shorter = df[np.argmin([len(x) for x in df])]

        # interpolate
        xvals = np.arange(min_len)/(min_len/max_len)
        longer_new = pd.DataFrame()

        for j in list(longer):
            longer_new[j] = np.interp(xvals, np.arange(len(longer[j])),longer[j])

        # average values
        df_out = (longer_new + shorter)/2

        df_in[i[0] + '_int_' + i[1]] = df_out

    # concatenate
    bau = df_in[list(df_in.keys())[0]]

    for i in list(df_in.keys())[1:]:
        bau = pd.concat([bau, df_in[i]])

    motion_data = bau

    # renew data indices
    motion_data_man_list = list(df_in.keys())
    bau1 = [[0, len(df_in[motion_data_man_list[0]]) - 1]]

    for i in motion_data_man_list[1:]:
        bau1.append([bau1[-1][-1] + 1, bau1[-1][-1] + len(df_in[i])])

    motion_data_idx = bau1

    return [motion_data, motion_data_man_list, motion_data_idx]


########################################################


def implement_mapping(motion_data, feats_compressed):
    ''' Implementation of regression for the definition of the human-robot mapping '''
    return test_regressors(motion_data, feats_compressed)


########################################################


def test_regressors(motion_data, feats_compressed):
    ''' Test the selected set of regressors '''

    global _PLOT
    _PLOT['score'] = {} 
    _PLOT['reg_in_out'] = {} 
    _PLOT['results'] = {}

    # reset results
    test_results = []

    # get final datasets for fitting
    train_dataset, test_dataset = _get_fit_datasets(motion_data)

    count = 0

    # get list of regressors
    regs = _pick_regressor_list()

    test_info = {}

    for out in settings['regression_outputs']:

        logging.info('Fitting output {}'.format(out))

        feats_compressed_out = feats_compressed[out]

        for reg in regs:

            count += 1
            
            logging.info('Fitting with {}'.format(reg))
            logging.info('Testing {} of {}'.format(count, regs))

            if settings['shuffle_data']:
                X, y = shuffle(train_dataset[feats_compressed_out].values, train_dataset[out].values, random_state = 0)
            else:
                X, y = [train_dataset[feats_compressed_out].values, train_dataset[out].values]

            X = X.reshape(-1, 1)
            y= y.reshape(-1, 1)

            # measure time
            t = time.monotonic()
            # fit datasets
            reg.fit(X,y)
            fit_time = time.monotonic()-t

            # real outputs
            y_true = test_dataset[out].values

            # measure time
            t = time.monotonic()
            # predict 
            y_score = reg.predict(test_dataset[feats_compressed_out].values.reshape(-1, 1))
            pred_time = (time.monotonic()-t)/len(test_dataset)

            logging.info('Done.')

            # store results
            test_results.append({"reg":reg.steps[-1][1],
                        "reg_type":str(reg.steps[-1][1]),
                        "fit_time":fit_time,
                        "pred_time":pred_time,
                        "mse":np.inf,
                        "y_true":y_true,
                        "x":test_dataset[feats_compressed],
                        "y_score":y_score
                        })

            # assign error
            if not np.isnan(y_score).any():
                test_results[-1]["mse"] = metrics.mean_squared_error(y_true, y_score)

            # plot score
            if settings['plot_reg_score']:
                _PLOT['score']['test_results'] = test_results
                _plot_score(_PLOT['score'], out, only_true = settings['plot_score_only_true'], save = True)

        # plot
        _PLOT['results']['test_results'] = test_results
        plot_test_results(_PLOT['results'], settings['regression_outputs'], save = True)
        # plot
        if settings['dim_reduction']:

            _PLOT['reg_in_out']['feats'] = feats_compressed_out
            _PLOT['reg_in_out']['motion_data'] = motion_data
            _PLOT['reg_in_out']['test_dataset'] = test_dataset
            plot_regression_inputs_outputs(_PLOT['reg_in_out'], out, save = True)

        perf = [x['mse'] for x in test_results]

        best_idx = np.argmin(perf)                      # best
        used_idx = 1                                    # first non linear

        M_v = [np.max(x) for x in np.transpose(X)]
        m_v = [np.min(x) for x in np.transpose(X)]

        # store info
        test_info[out] = {"settings":settings,
                        "results":test_results[:],
                        "best":best_idx,
                        "used":used_idx,
                        "feats_compressed":feats_compressed_out,
                        "train_dataset":train_dataset,
                        "test_dataset":test_dataset,
                        "fit_x":train_dataset[feats_compressed_out].values,
                        "fit_y":train_dataset[settings['outputs']],
                        "max_values":M_v,
                        "min_values":m_v
                        }

    return test_info


########################################################


def _get_fit_datasets(motion_data, motion_data_idx = None):
    ''' Returns final datasets for fitting '''
    
    # base separation
    train_dataset = motion_data.copy()
    test_dataset = motion_data.copy()

    # options
    if settings['data_augmentation']:
        train_dataset = _with_data_augmentation(train_dataset)

    if settings['data_downsampling']:
        train_dataset = _with_data_downsampling(train_dataset)

    if settings['train_test_mode'] == 'split':
        #this samples not randomly
        train_dataset = train_dataset.iloc[np.arange(0, len(train_dataset), 1/ settings['split_factor_train'])]

    return [train_dataset, test_dataset]


########################################################


def _with_data_augmentation( train_dataset):
    ''' Creates additional data based on the current settings '''

    if settings['augmentation_interpolate_to_zero']:
        # creates new datasets scaling the available values [interpolation_duplicates] times until 0 is reached

        original_df = train_dataset.copy()
        df_to_return = train_dataset.copy()

        for i in range(1, settings['interpolation_duplicates'] + 1):
            copy = original_df.copy()
            copy = copy * i/settings['interpolation_duplicates']
            df_to_return = pd.concat([df_to_return, copy])

    if settings['augmentation_add_noise']:
        # creates [settings['noisy_copies']] noisy copies of the original dataset

        original_df = train_dataset.copy()
        df_to_return = train_dataset.copy()

        for i in range(1, settings['noisy_copies'] + 1):

            copy = original_df.copy()
            for i in list(copy):
                copy[i] = copy[i] + np.random.randn(copy[i].size) * settings['noise_std'] # noise, same std = std_noise

            df_to_return = pd.concat([df_to_return, copy])

    return df_to_return


########################################################

### TODO : pass arguments, instead of using global settings (makes the function more versatile)
def _with_data_downsampling(train_dataset):
    ''' Downsamples data by a factor [settings['downsampling_fraction']] '''

    frac = settings['downsampling_fraction']
    original_df = train_dataset.copy()
    df_to_return = original_df.sample(frac = frac)

    return df_to_return


########################################################


def _plot_score(vals, out, idx = -1, only_true = False, save = False):
    ''' Plots regression result, true vs predicted '''

    # get data
    res = vals['test_results'][idx]

    # make subplots
    ax = plt.figure()
    plt.ylabel(out)
    plt.xlabel('Sample #')

    # plot true
    plt.scatter(list(range(1,len(res['y_true'])+1)), res['y_true'], s=1, c = 'b', marker = "s", label = 'Real')
    if not only_true:
        # plot predicted
        plt.scatter(list(range(1,len(res['y_score'])+1)), res['y_score'], s=1, c = 'r', marker = "o", label = 'Predicted')
    plt.grid()
    if not only_true:
        plt.legend()

    plt.title('test_score_{}'.format(out))

    if save:
        fol = os.path.join(settings['plot_folder'], 'results')
        HRI.create_dir_safe(fol)
        savefig(os.path.join(fol, 'test_score.pdf'), bbox_inches='tight')
        plt.close

########################################################


def plot_regression_inputs_outputs(vals, out, save = False):
    ''' Plots dimensionality reduction : selected features, compressed features, outputs '''

    global _DEBUG

    feats = vals['feats']
    motion_data = vals['motion_data']
    test_dataset = vals['test_dataset']

    plt.figure()

    # selected features
    for idx, i in enumerate(_DEBUG['features_filtered'][out]):

        plt.subplot(len(_DEBUG['features_filtered'][out]), 3, 1 + 3*idx)
        plt.plot(np.arange(1, len(motion_data[i]) + 1), motion_data[i], label = i)
        plt.legend(loc = 'upper right')
        plt.grid()

    # compressed features
    plt.subplot(1, 3, 2)
    plt.plot(np.arange(1, len(motion_data['reduced_inputs_'+out]) + 1), motion_data['reduced_inputs_'+out], label = 'reduced_inputs_'+out)
    plt.legend(loc = 'upper right')
    plt.grid()

    # outputs
    plt.subplot(1, 3, 3)
    plt.plot(np.arange(1, len(test_dataset[out]) + 1), test_dataset[out], label = out)
    plt.legend(loc = 'upper right')
    plt.grid()

    plt.title('Regression input - output')

    if save:
        fol = os.path.join(settings['plot_folder'], 'results')
        HRI.create_dir_safe(fol)
        savefig(os.path.join(fol, 'regression_input_output.pdf'), bbox_inches='tight')
        plt.close

########################################################


def plot_test_results(vals, outs, mode = 'error', save = False):
    ''' Plots quality metric for regression '''

    global _DEBUG

    test_results = vals['test_results']

    # metric selection
    if mode == 'error':
        out = [x['mse'] for x in test_results]
        title = 'performance'
    elif mode == 'fit_time':
        out = [x['fit_time'] for x in test_results]
        title = 'time to fit'
    elif mode == 'pred_time':
        out = [x['pred_time'] for x in test_results]
        title = 'time to predict'

    # bar plot
    ax = plt.figure()
    plt.grid('on')
    plt.title(title)
    plt.bar(np.arange(0, len(out))+1, out)
    plt.xticks(np.arange(len(outs))+1, outs)

    plt.title('Test Results ({})'.format(mode))

    if save:
        fol = os.path.join(settings['plot_folder'], 'results')
        HRI.create_dir_safe(fol)
        savefig(os.path.join(fol, 'test_results_{}.pdf'.format(mode)), bbox_inches='tight')
        plt.close

########################################################


def store(data, is_struct = False):
    ''' Stores mattping data in subject folder '''

    if is_struct:       # in this case, data = self
        HRI.save_obj(data, os.path.join(settings['subject_folder'], settings['input_device']))
    else:               # in this case, data = {}
        HRI.save_obj(data, os.path.join(settings['subject_folder'], settings['input_device']))


########################################################


def get_debug_data():
    ''' Returns debug data '''
    return _DEBUG


########################################################


def get_plot_data():
    ''' Returns plot data '''
    return _PLOT


########################################################


def _pick_regressor_list():
    ''' Returns list of regressors to test '''

    regs = regressors[settings['regressor_settings']]

    # legacy name for linear regression
    if settings['control_style'] == 'maxmin':
        regs = regressors['LIN']

    return regs


########################################################


def plot_motion_data(motion_data, processed = False):
    ''' Plots motion data '''

    global _DEBUG

    # plot processed
    if processed:
        df = motion_data
        ax = plt.figure()

        for i in list(df):
            plt.plot(df[i], label = i)

        plt.grid()
        plt.legend()

    # plot unprocessed
    else:
        df_all = motion_data
        for i in df_all:
            df = i['df']

            plt.figure()

            for j in list(df):
                plt.plot(df[j], label = j)

            plt.grid()
            plt.legend()

    _DEBUG['plot_motion_data'] = ax


########################################################


def delete_all_clean_data():    ### TOFIX
    ''' Deletes clean data for the selected  '''

    #move to data folder
    os.chdir(settings['data_folder'])

    # list files
    files = os.listdir()

    files_to_delete = [x for x in files if 'CLEAN' in x]

    for i in files_to_delete:
        os.remove(i)


########################################################


def update_settings(settings_in):
    """ Update settings """
    global settings
    settings = settings_in


########################################################


def run():

    unprocessed_data = {}
    motion_data = {}
    
    # import and process data
    unprocessed_data = import_data()
    motion_data, motion_data_idx, motion_data_man_list, parameters = process_data(unprocessed_data = unprocessed_data)

    # dimensionality reduction
    feats_all, feats, feats_compressed, dimred, motion_data = run_dimensionality_reduction(parameters, motion_data)

    # separate by maneuver
    # motion_data_maneuvers, motion_data_separated = separate_datasets(unprocessed_data, motion_data, motion_data_idx)
    
    # [motion_data, motion_data_man_list, motion_data_idx] = augment_on_reduced_data(motion_data_separated)

    # test regressors
    test_info = implement_mapping(motion_data, feats_compressed)

    return [settings, feats, parameters, dimred, test_info]


########################################################
########################################################
########################################################


if __name__ == '__main__':

    settings, feats, parameters, dimred, test_info = run()

    _debug = get_debug_data()
    _plot = get_plot_data()

    plt.show()

    mapping_tostore = {'settings' : settings,
                       'features' : feats,
                       'parameters' : parameters,
                       'dimred' : dimred,
                       'test_info' : test_info,
                       '_debug' : _debug,
                       '_plot' : _plot}

    if settings['store_mapping']:

        store(mapping_tostore)