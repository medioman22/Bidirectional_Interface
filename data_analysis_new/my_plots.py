#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 12:05:04 2019

@author: lis
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import savefig


        
    
def bar_multi(vals, error = None, xlabels = '', xticks = None, yticks = None, xlim = None, ylim = None, ylabel = '', title = '', legend = '', normalize = False, colors = None, w= None, ax = None, save = False, where = None):
    
    
    print(colors)
    
    if colors is None:
        colors = 'rgbkmyc'
    
    def norm_list(l, M_all = None):
        
        if M_all is None:
            M = [max(i) for i in l]
            M_all = max(M)
        
        list_l_norm = l[:]
        
        for idx, i in enumerate(l):
            print(i)
            list_l_norm[idx] = np.array(i)/M_all
            print(i)
            
        l = list_l_norm
        
        return [l, M_all]
        
    # make list of lists if not
    if type(vals[0]) is not list:
        vals = [vals]
#        for i in np.arange(len(vals)):
#            vals[i] = [vals[i]]
    
    n_ticks = len(vals[0])
    l_each = len(vals)
    
    no_legend = False
    if legend == '':
        no_legend = True
        legend = [''] * l_each
        
        
    if ax is None:
        ax = plt.subplot(111)
    
    plt.title(title)
    ax.grid('on')
    
    ax.set_ylabel(ylabel)
    ax.set_xlabel("")
    
    
    if normalize:
        
        [vals, M] = norm_list(vals)
        
        if error is not None:
            [error, _] = norm_list(error, M)
    
    x = np.arange(n_ticks) + 1
    if w is None:
        w = 0.3
    
    bars = []
    
    for count, i in enumerate(vals):
        if error is None:
            bars.append(ax.bar(x - w*l_each/2 + w*(count + 1/2), i, width=w,align='center', label = legend[count], color = colors[count], ecolor = colors[count]))
        else:
            bars.append(ax.bar(x - w*l_each/2 + w*(count + 1/2), i, yerr=error[count],width=w,align='center', label = legend[count], color = colors[count], ecolor = colors[count]))
            
    if not no_legend:
        ax.legend()
        
    plt.xticks(x, xlabels, axes=ax)
    
    if xlim is not None:
        plt.xlim(xlim)    
    if ylim is not None:
        plt.xlim(ylim)
    if xticks is not None:
        plt.xticks(xticks)    
    if yticks is not None:
        plt.yticks(yticks)
        
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    if save:
        savefig(where, bbox_inches='tight')
    
    return ax
        
        
def boxplot_elegant(ax, data, position, c, whis = 1.5):
    
    plt.boxplot(data, notch=None, positions = position, patch_artist=True,
                boxprops=dict(color=c, facecolor='none'),
                capprops=dict(color=c),
                whiskerprops=dict(color=c),
                flierprops=dict(color=c, markeredgecolor=c),
                medianprops=dict(color=c),
                whis = whis
                )
    
def make_fig_simple():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    return [fig, ax]