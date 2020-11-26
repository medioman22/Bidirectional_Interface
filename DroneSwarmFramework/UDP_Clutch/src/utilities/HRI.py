#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 17:21:39 2018

@author: matteomacchini
"""

import numpy as np
import pickle
import os
import pandas as pd

import context

import utilities.utils as utils


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def create_dir_safe(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def merge_data_df(unproc, delete_after_max = False, outputs = None, var_min = 3):

    fixed_idx = 1530        # TODO : implement fixed idx cut

    df = [x['df'] for x in unproc]

    df_list = df.copy()
    proc = df_list[0]

    idx = [[0]]

    if delete_after_max:

        m = []
        m_idx = []

        # find max over all outputs
        for j in outputs:

            [m_temp, m_idx_temp] = utils.find_maxmin(proc[j], absolute = True)
            m.append(m_temp)
            m_idx.append(m_idx_temp)

        # don't cut if input varies very little
        if max(m) > var_min: # TODO : put in settings
            m_idx_all = m_idx[m.index(max(m))]
        else:
            m_idx_all = len(proc[j])

        proc = proc.iloc[0:m_idx_all]

        idx[0].append(m_idx_all -1)


    for i in df_list[1:]:

        if delete_after_max:

            m = []
            m_idx = []

            # find max over all outputs
            for j in outputs:

                [m_temp, m_idx_temp] = utils.find_maxmin(i[j], absolute = True)
                m.append(m_temp)
                m_idx.append(m_idx_temp)

            # don't cut if input varies very little
            if max(m) > var_min: # TODO : put in settings
                m_idx_all = m_idx[m.index(max(m))]
            else:
                m_idx_all = len(proc[j])

            i = i.iloc[0:m_idx_all]

        idx.append([len(proc)])

        proc = pd.concat([proc, i])

        idx[-1].append(idx[-1][-1] + m_idx_all - 1)

    return [proc, idx]


def file_name(sett):

    return '{0}_{1}_inst_{2}'.format(sett['subject_name'],sett['input_device'],sett['instance'])


def hri_state(sett):
    """ Returns state of dataset ('NO DATA', 'ACQUIRED', 'PROCESSED')"""
    fol = sett['subject_folder']

    try:
        files = os.listdir(fol)
    except:
        # if folder does not exist
        return 'NO DATA'

    data = False
    processed = False
    if len(files)>3:    # depending on os, 2/3 elements are always there!
        data = True
        if any([sett['control_style'] in x for x in files]):
            processed = True
    
    if processed:
        return 'PROCESSED'
    if data:
        return 'ACQUIRED'
    else:
        return 'NO DATA'