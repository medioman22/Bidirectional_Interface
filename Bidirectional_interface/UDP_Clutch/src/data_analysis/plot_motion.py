# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 16:11:26 2019

@author: macchini
"""

import ExperimentalDataMotion_TEST
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import savefig
from scipy import optimize
from scipy import stats
import utils

import matplotlib as mpl



### Parameters

c0 = np.array([102, 153, 255])
c1 = np.array([150,0,0])
c2 = np.array([0,0,100])

c_b = ["#5C9FDA", "#1E405E", "#396C98"]
c_r = ["#ff4d4d", "#750C0C", "#AC3838"]

lw = 1.5

params = {
    'axes.labelsize': 11,
    'font.size': 11,
    'legend.fontsize': 11,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'text.usetex': False,
    'figure.figsize': [6, 5],
    'boxplot.boxprops.linewidth' : lw,
    'boxplot.whiskerprops.linewidth' : lw,
    'boxplot.capprops.linewidth' : lw,
    'boxplot.medianprops.linewidth' : lw

   }
mpl.rcParams.update(params)




settings = ExperimentalDataMotion_TEST.initialize_settings()

settings['methods'] = ['simple']
settings['interfaces'] = ['motive']
settings['plot_style'] = 'mean-max-min'
settings['metric'] = 'error'
settings['plot'] = True



exp_data = ExperimentalDataMotion_TEST.run_data_motion_analysis(settings)


covar_mean = exp_data.covar_mean
snr_mean = exp_data.snr_mean
coeff_mean = exp_data.coeff_mean
covar_std = exp_data.covar_std
snr_std = exp_data.snr_std
coeff_std = exp_data.coeff_std

n_uses_rpy = exp_data.n_uses_rpy
body_parts = exp_data.body_parts
rot = exp_data.rot


# plot all
plt.figure()

xlabels = [''] * 9
axis = plt.subplot(311)
utils.bar_multi(vals = (np.array(covar_mean)*100).tolist(), error = None, xlabels = xlabels, ylabel = 'Correlation [%]', legend = rot, title = '', normalize = False, colors = c_b, ax = axis)
xlabels = [''] * 9
plt.ylim([0,40])
plt.yticks([0,10,20,30,40])

axis = plt.subplot(312)
xlabels = [''] * 9
utils.bar_multi(vals = (np.array(snr_mean)*100).tolist(), error = None, xlabels = xlabels, ylabel = 'SNR [%]', legend = rot, title = '', normalize = False, colors = c_b, ax = axis)
plt.ylim([0,40])
plt.yticks([0,10,20,30,40])


axis = plt.subplot(313)
utils.bar_multi(vals = (n_uses_rpy/np.max(n_uses_rpy)*100).tolist(), error = None, xlabels = body_parts, ylabel = 'Relevant features [%]', legend = rot, title = '', normalize = False, colors = c_r, ax = axis)

plt.ylim([0,100])

savefig('../../a2019a_wearableForAerial/Paper/figures/motion_analysis.pdf', bbox_inches='tight')
