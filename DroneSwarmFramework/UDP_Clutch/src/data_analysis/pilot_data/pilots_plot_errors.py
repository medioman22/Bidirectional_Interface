#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 03:15:27 2019

@author: lis
"""


import utils
import HRI
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.pylab import savefig

from scipy import optimize
from scipy import stats


def main(errors = None):
    
    white = np.array([1,1,1])
        
    c0 = np.array([0,0,0])/256
    c1 = np.array([150,0,0])/256
    c2 = np.array([0,0,100])/256
    c3 = np.array([0,100,0])/256
    
    c4 = np.array([100,0,100])/256
    c5 = np.array([150,50,150])/256
    
    clearer = 40/256
    
    c = [c1, c2, c4, c1 + clearer, c2 + clearer, c4 + clearer]
    c_f = [c1, c2, c4, c1 + clearer, c2 + clearer, c4 + clearer]
    
    al1 = 1
    al2 = 1
    
    al = [al1, al1, al1, al2, al2, al2]
    
    
    lw = 1.5
    
    params = {
        'axes.labelsize': 11,
        'font.size': 11,
        'legend.fontsize': 11,
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'figure.figsize': [4, 3.5],
        'legend.loc': 'upper left',
        'boxplot.boxprops.linewidth' : lw,
        'boxplot.whiskerprops.linewidth' : lw,
        'boxplot.capprops.linewidth' : lw,
        'boxplot.medianprops.linewidth' : lw,
        'text.usetex' : True,
        'font.family' : 'serif',
    
       }
    
    mpl.rcParams.update(params)
    
    #values

    
    if errors is None:
        
        file = 'errors_new'
        errors = HRI.load_obj(file)
        
    else:
        file = ''
    
    m = [np.mean(errors[x]) for x in errors.keys()]
    s = [np.std(errors[x]) for x in errors.keys()]
    
    m_p = np.mean(errors['l_p'] + errors['nl_p'])
    m_np = np.mean(errors['l_np'] + errors['nl_np'])
    
    s_p = np.std(errors['l_p'] + errors['nl_p'])
    s_np = np.std(errors['l_np'] + errors['nl_np'])
    
    M = min(m)
    
    m = [x/M for x in m]
    s = [x/M for x in s]

    
    m_p = [m_p/M]
    m_np = [m_np/M]
    s_p = [s_p/M]
    s_np = [s_np/M]
    
    vals = [m[2], m[3], m_np, m[0], m[1] , m_p]
    err = [s[2], s[3], s_np, s[0], s[1], s_p]
    
    
    xlabels = ['Non Personalized', 'Personalized']
    legend = [None, None, None, 'linear', 'nonlinear', 'mean']
    
    fig = plt.figure()
    
    ax = plt.subplot2grid((2, 1), (0, 0))
    
    l_each = 2
    w = 0.2
    
    bars = []
    
    gap = 0.25
    
    x = [1-gap, 1, 1+gap, 2-gap, 2, 2+gap]
        
    for count, i in enumerate(vals):
            bars.append(ax.bar(x[count], i, yerr=err[count],width=w,align='center', label = legend[count], facecolor = c_f[count], edgecolor = c[count], ecolor = c[count], alpha = al[count]))
    
    plt.xticks([1, 2], xlabels, axes=ax)
    #plt.yticks([0, 2, 4, 6, 8, 10])
    
    plt.xticks(rotation=0)
    plt.grid()
    plt.legend(loc = 'upper right')
    plt.xlim([0.5, 2.5])
    plt.ylim([0.5, 100])
    ax.set_yscale('log')
        
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    #values

    
    if errors is None:
        
        file = 'errors_new_outliers'
        errors = HRI.load_obj(file)
        
    else:
        file = ''
    
    m = [np.mean(errors[x]) for x in errors.keys()]
    s = [np.std(errors[x]) for x in errors.keys()]
    
    m_p = np.mean(errors['l_p'] + errors['nl_p'])
    m_np = np.mean(errors['l_np'] + errors['nl_np'])
    
    s_p = np.std(errors['l_p'] + errors['nl_p'])
    s_np = np.std(errors['l_np'] + errors['nl_np'])
    
    M = min(m)
    
    m = [x/M for x in m]
    s = [x/M for x in s]

    
    m_p = [m_p/M]
    m_np = [m_np/M]
    s_p = [s_p/M]
    s_np = [s_np/M]
    
    vals = [m[2], m[3], m_np, m[0], m[1] , m_p]
    err = [s[2], s[3], s_np, s[0], s[1], s_p]
    
    ax = plt.subplot2grid((2, 1), (1, 0))
    
    l_each = 2
    w = 0.2
    
    bars = []
    
    gap = 0.25
    
    x = [1-gap, 1, 1+gap, 2-gap, 2, 2+gap]
        
    for count, i in enumerate(vals):
            bars.append(ax.bar(x[count], i, yerr=err[count],width=w,align='center', label = legend[count], facecolor = c_f[count], edgecolor = c[count], ecolor = c[count], alpha = al[count]))
    
    plt.xticks([1, 2], xlabels, axes=ax)
    #plt.yticks([0, 2, 4, 6, 8, 10])
    
    plt.xticks(rotation=0)
    plt.grid()
#    plt.legend(loc = 'upper right')
    plt.xlim([0.5, 2.5])
    plt.ylim([0.5, 100])
    ax.set_yscale('log')
        
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
#    
#    #######
#    
#    vals = [m_np, m_p]
#    err = [s_np, s_p]
#    
#    ax = plt.subplot2grid((1, 3), (0,2))
#    
#    l_each = 2
#    w = 0.2
#    
#    bars = []
#    
#    gap = 0.15
#    
#    x = [[1-gap], [1+gap]]
#        
#    for count, i in enumerate(vals):
#            bars.append(ax.bar(x[count], i, yerr=err[count], width=w,align='center', label = legend[count], facecolor = c_pf[count], edgecolor = c_p[count], ecolor = c_p[count]))
#    
#    plt.xticks(x, xlabels, axes=ax)
#    plt.yticks([1, 10, 100], ['', '', ''], axes=ax)
#    #plt.yticks([0, 2, 4, 6, 8, 10])
#    
#    plt.xticks(rotation=0)
#    plt.grid()
#    plt.xlim([0.5, 1.5])
#    plt.ylim([0.5, 100])
#    ax.set_yscale('log')

    plt.ylabel('MSE (normalized)')
        
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    plt.show()
    
    
    t, p = stats.ttest_ind(errors['l_p'], errors['nl_p'])
    t_pers, p_pers = stats.ttest_ind(errors['l_p'] + errors['nl_p'], errors['l_np'] + errors['nl_np'])
    
    savefig('../../../a2019a_wearableForAerial/Paper/figures/pilots_' + file + '.pdf', bbox_inches='tight')

def plot_all():
    
    white = np.array([1,1,1])
        
    c0 = np.array([0,0,0])/256
    c1 = np.array([150,0,0])/256
    c2 = np.array([0,0,100])/256
    c3 = np.array([0,100,0])/256
    
    c4 = np.array([100,0,100])/256
    c5 = np.array([150,50,150])/256
    
    clearer = 40/256
    
    c = [c1, c2, c4, c1 + clearer, c2 + clearer, c4 + clearer]
    c_f = [c1, c2, c4, c1 + clearer, c2 + clearer, c4 + clearer]
    
    al1 = 1
    al2 = 1
    
    al = [al1, al1, al1, al2, al2, al2]
    
    
    lw = 1.5
    
    params = {
        'axes.labelsize': 11,
        'font.size': 11,
        'legend.fontsize': 11,
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'figure.figsize': [4, 3],
        'legend.loc': 'upper left',
        'boxplot.boxprops.linewidth' : lw,
        'boxplot.whiskerprops.linewidth' : lw,
        'boxplot.capprops.linewidth' : lw,
        'boxplot.medianprops.linewidth' : lw,
        'text.usetex' : True,
        'font.family' : 'serif',
    
       }
    
    mpl.rcParams.update(params)
    
    #values

    
    file = 'errors_new'
    errors = HRI.load_obj(file)
    
    m = [np.mean(errors[x]) for x in errors.keys()]
    s = [np.std(errors[x]) for x in errors.keys()]
    
    m_p = np.mean(errors['l_p'] + errors['nl_p'])
    m_np = np.mean(errors['l_np'] + errors['nl_np'])
    
    s_p = np.std(errors['l_p'] + errors['nl_p'])
    s_np = np.std(errors['l_np'] + errors['nl_np'])
    
    M = min(m)
    
    m = [x/M for x in m]
    s = [x/M for x in s]

    
    m_p = [m_p/M]
    m_np = [m_np/M]
    s_p = [s_p/M]
    s_np = [s_np/M]
    
    vals = [m[2], m[3], m_np, m[0], m[1] , m_p]
    err = [s[2], s[3], s_np, s[0], s[1], s_p]
    
    
    xlabels = ['Non Personalized', 'Personalized']
    legend = [None, None, None, 'linear', 'nonlinear', 'mean']
    
    plt.figure()
    
    ax = plt.subplot2grid((2, 1), (0, 0))

    w = 0.2
    
    bars = []
    
    gap = 0.25
    
    x = [1-gap, 1, 1+gap, 2-gap, 2, 2+gap]
        
    for count, i in enumerate(vals):
            bars.append(ax.bar(x[count], i, yerr=err[count],width=w,align='center', label = legend[count], facecolor = c_f[count], edgecolor = c[count], ecolor = c[count], alpha = al[count]))
    
    plt.xticks([1, 2], ['', ''], axes=ax)
    #plt.yticks([0, 2, 4, 6, 8, 10])
    
    plt.xticks(rotation=0)
    plt.grid()
    plt.legend(loc = 'upper right')
    plt.xlim([0.5, 2.5])
    plt.ylim([0.5, 100])
    ax.set_yscale('log')
        
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.ylabel('MSE')
    
    #values

    
    file = 'errors_new_outliers'
    errors = HRI.load_obj(file)
    
    m = [np.mean(errors[x]) for x in errors.keys()]
    s = [np.std(errors[x]) for x in errors.keys()]
    
    m_p = np.mean(errors['l_p'] + errors['nl_p'])
    m_np = np.mean(errors['l_np'] + errors['nl_np'])
    
    s_p = np.std(errors['l_p'] + errors['nl_p'])
    s_np = np.std(errors['l_np'] + errors['nl_np'])
    
    M = min(m)
    
    m = [x/M for x in m]
    s = [x/M for x in s]

    
    m_p = [m_p/M]
    m_np = [m_np/M]
    s_p = [s_p/M]
    s_np = [s_np/M]
    
    vals = [m[2], m[3], m_np, m[0], m[1] , m_p]
    err = [s[2], s[3], s_np, s[0], s[1], s_p]
    
    ax = plt.subplot2grid((2, 1), (1, 0))
    
    l_each = 2
    w = 0.2
    
    bars = []
    
    gap = 0.25
    
    x = [1-gap, 1, 1+gap, 2-gap, 2, 2+gap]
        
    for count, i in enumerate(vals):
            bars.append(ax.bar(x[count], i, yerr=err[count],width=w,align='center', label = legend[count], facecolor = c_f[count], edgecolor = c[count], ecolor = c[count], alpha = al[count]))
    
    plt.xticks([1, 2], xlabels, axes=ax)
    #plt.yticks([0, 2, 4, 6, 8, 10])
    
    plt.xticks(rotation=0)
    plt.grid()
#    plt.legend(loc = 'upper right')
    plt.xlim([0.5, 2.5])
    plt.ylim([0.5, 1000])
    ax.set_yscale('log')
        
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
#    
#    #######
    

    plt.ylabel('MSE')
        
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    plt.show()
    
    
    t, p = stats.ttest_ind(errors['l_p'], errors['nl_p'])
    t_pers, p_pers = stats.ttest_ind(errors['l_p'] + errors['nl_p'], errors['l_np'] + errors['nl_np'])

    savefig('../../../a2019a_wearableForAerial/Paper/figures/pilots.pdf', bbox_inches='tight')

def plot_all_split():
    
    white = np.array([1,1,1])
        
    c0 = np.array([0,0,0])/256
    c1 = np.array([150,0,0])/256
    c2 = np.array([0,0,100])/256
    c3 = np.array([0,100,0])/256
    
    c4 = np.array([100,0,100])/256
    c5 = np.array([150,50,150])/256
    
    clearer = 40/256
    
    c = [c1, c2, c1 + clearer, c2 + clearer]
    c_f = [c1, c2, c1 + clearer, c2 + clearer]
    
    c2_f = [c4, c4 + clearer]
    
    lw = 1.5
    
    params = {
        'axes.labelsize': 11,
        'font.size': 11,
        'legend.fontsize': 11,
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'figure.figsize': [4, 3],
        'legend.loc': 'upper left',
        'boxplot.boxprops.linewidth' : lw,
        'boxplot.whiskerprops.linewidth' : lw,
        'boxplot.capprops.linewidth' : lw,
        'boxplot.medianprops.linewidth' : lw,
        'text.usetex' : True,
        'font.family' : 'serif',
    
       }
    
    mpl.rcParams.update(params)
    
    #values

    
    file = 'errors_new'
    errors = HRI.load_obj(file)
    
    m = [np.mean(errors[x]) for x in errors.keys()]
    s = [np.std(errors[x]) for x in errors.keys()]
    
    m_p = np.mean(errors['l_p'] + errors['nl_p'])
    m_np = np.mean(errors['l_np'] + errors['nl_np'])
    
    s_p = np.std(errors['l_p'] + errors['nl_p'])
    s_np = np.std(errors['l_np'] + errors['nl_np'])
    
    M = min(m)
    
    m = [x/M for x in m]
    s = [x/M for x in s]
    m_p = [m_p/M]
    m_np = [m_np/M]
    s_p = [s_p/M]
    s_np = [s_np/M]

###
    
    plt.figure()
    
    vals = [m[2], m[3], m[0], m[1]]
    err = [s[2], s[3], s[0], s[1]]
    
    
    
    xlabels = ['NP', 'P']
    legend = [None, None, 'linear', 'nonlinear']
    
    ax = plt.subplot2grid((2, 3), (0, 0), colspan = 2)

    w = 0.2
    
    bars = []
    
    gap = 0.15
    
    x = [1-gap, 1+gap, 2-gap, 2+gap]
        
    for count, i in enumerate(vals):
            bars.append(ax.bar(x[count], i, yerr=err[count],width=w,align='center', label = legend[count], facecolor = c_f[count], edgecolor = c[count], ecolor = c[count]))
    
    plt.xticks([1, 2], ['', ''], axes=ax)
    #plt.yticks([0, 2, 4, 6, 8, 10])
    
    plt.xticks(rotation=0)
    plt.grid()
    plt.legend(loc = 'upper right')
    plt.xlim([0.5, 2.5])
    plt.ylim([0.5, 200])
    ax.set_yscale('log')
        
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.ylabel('MSE')
    
    ###
    
    vals = [m_np, m_p]
    err = [s_np, s_p]
    
    legend = [None, None, None, 'linear', 'nonlinear', 'mean']
    
    ax = plt.subplot2grid((2, 3), (0, 2))

    w = 0.2
    
    bars = []
    
    gap = 0.15
    
    x = [1-gap, 1+gap]
        
    for count, i in enumerate(vals):
            bars.append(ax.bar(x[count], i, yerr=err[count],width=w,align='center', label = legend[count], facecolor = c2_f[count], edgecolor = c2_f[count], ecolor = c2_f[count]))
    
    plt.xticks(x, ['', ''], axes=ax)
    
    plt.xticks(rotation=0)
    plt.grid()
#    plt.legend(loc = 'upper right')
    plt.xlim([0.5, 1.5])
    plt.ylim([0.5, 200])
    ax.set_yscale('log')
    plt.yticks([1, 10, 100], ['', '', ''], axes=ax)
        
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    p_vals = {}
    pf_vals = {}
    
    t, p_vals['non_out_pers'] = stats.ttest_ind(errors['l_p'], errors['nl_p'])
    t_pers_out, p_vals['non_out_all'] = stats.ttest_ind(errors['l_p'] + errors['nl_p'], errors['l_np'] + errors['nl_np'])
    
    pf_vals['non_out_pers'] = utils.f_test(errors['l_p'], errors['nl_p'])
    pf_vals['non_out_all'] = utils.f_test(errors['l_p'] + errors['nl_p'], errors['l_np'] + errors['nl_np'])
    

    savefig('../../../a2019a_wearableForAerial/Paper/figures/pilotdfsfs.pdf', bbox_inches='tight')
    
    #values

    
    file = 'errors_new_outliers'
    errors = HRI.load_obj(file)
    
    m = [np.mean(errors[x]) for x in errors.keys()]
    s = [np.std(errors[x]) for x in errors.keys()]
    
    m_p = np.mean(errors['l_p'] + errors['nl_p'])
    m_np = np.mean(errors['l_np'] + errors['nl_np'])
    
    s_p = np.std(errors['l_p'] + errors['nl_p'])
    s_np = np.std(errors['l_np'] + errors['nl_np'])
    
    M = min(m)
    
    m = [x/M for x in m]
    s = [x/M for x in s]
    m_p = [m_p/M]
    m_np = [m_np/M]
    s_p = [s_p/M]
    s_np = [s_np/M]

###
    
    vals = [m[2], m[3], m[0], m[1]]
    err = [s[2], s[3], s[0], s[1]]
    
    
    
    xlabels = ['NP', 'P']
    legend = [None, None, 'linear', 'nonlinear']
    
    ax = plt.subplot2grid((2, 3), (1, 0), colspan = 2)

    w = 0.2
    
    bars = []
    
    gap = 0.15
    
    x = [1-gap, 1+gap, 2-gap, 2+gap]
        
    for count, i in enumerate(vals):
            bars.append(ax.bar(x[count], i, yerr=err[count],width=w,align='center', label = legend[count], facecolor = c_f[count], edgecolor = c[count], ecolor = c[count]))
    
    plt.xticks([1, 2], xlabels, axes=ax)
#    plt.yticks([1, 10, 100], ['', '', ''], axes=ax)
    #plt.yticks([0, 2, 4, 6, 8, 10])
    
    plt.xticks(rotation=0)
    plt.grid()
#    plt.legend(loc = 'upper right')
    plt.xlim([0.5, 2.5])
    plt.ylim([0.5, 200])
    ax.set_yscale('log')
        
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.ylabel('MSE')
    
    ###
    
    vals = [m_np, m_p]
    err = [s_np, s_p]
    
    legend = [None, None, None, 'linear', 'nonlinear', 'mean']
    
    ax = plt.subplot2grid((2, 3), (1, 2))

    w = 0.2
    
    bars = []
    
    gap = 0.15
    
    x = [1-gap, 1+gap]
        
    for count, i in enumerate(vals):
            bars.append(ax.bar(x[count], i, yerr=err[count],width=w,align='center', label = legend[count], facecolor = c2_f[count], edgecolor = c2_f[count], ecolor = c2_f[count]))
    
    plt.xticks(x, xlabels, axes=ax)
    #plt.yticks([0, 2, 4, 6, 8, 10])
    
    plt.xticks(rotation=0)
    plt.grid()
#    plt.legend(loc = 'upper right')
    plt.xlim([0.5, 1.5])
    plt.ylim([0.5, 200])
    ax.set_yscale('log')
    plt.yticks([1, 10, 100], ['', '', ''], axes=ax)
        
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
#    plt.ylabel('MSE')
    
    plt.show()
    
    
    t, p_vals['out_pers'] = stats.ttest_ind(errors['l_p'], errors['nl_p'])
    t_pers_out, p_vals['out_all'] = stats.ttest_ind(errors['l_p'] + errors['nl_p'], errors['l_np'] + errors['nl_np'])
    
    pf_vals['out_pers'] = utils.f_test(errors['l_p'], errors['nl_p'])
    pf_vals['out_all'] = utils.f_test(errors['l_p'] + errors['nl_p'], errors['l_np'] + errors['nl_np'])

    savefig('../../../a2019a_wearableForAerial/Paper/figures/pilots.pdf', bbox_inches='tight')
    
    return [p_vals, pf_vals]
    
    

if __name__ == '__main__':

    p_vals = plot_all_split()