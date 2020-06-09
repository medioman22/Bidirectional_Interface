# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 17:23:13 2018

@author: macchini
"""
    

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

if parentdir not in sys.path:
    sys.path.insert(0,parentdir)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.pylab import savefig

import HRI_mapping_add
    
import HRI_mapping as hri

used_body_parts = HRI_mapping_add.HRI_mapping_settings().used_body_parts

filename = 'file:///C:/Users/macchini/Documents/Local_data/pilot_x1_wheel_motive_down_left_period_10_amplitude_50_inst_1_2018_Oct_26_12_49_38PM.txt'
filename = '/Volumes/GoogleDrive/My Drive/Matteo/EPFL/LIS/PhD/Natural_Mapping/DATA/acquired_data/mixed_unpacked/subject_24_motive_mixed_period_8_amplitude_50_inst_10_2018_Dec_14_04_10_27PM.txt'


file = pd.read_csv(filename)

### SELECT DATA ###

plot_list = ['roll', 'pitch']
plot_list = ['quat_x_8', 'quat_y_8', 'quat_z_8', 'quat_w_8']

# gets all input
plot_list = [x for x in list(file) if any(t in x for t in [str(y) for y in used_body_parts])]
plot_list = [x for x in plot_list if 'ID' not in x and 'input' not in x]

#pca = 

### CHOOSE PLOT TYPE ###

    
c0 = np.array([0,0,0])/256
c2 = np.array([204,0,0])/256
c1 = np.array([0,102,204])/256
c3 = np.array([0,100,0])/256

c_b = ["#5C9FDA", "#1E405E", "#396C98"]
c_r = ["#ff4d4d", "#750C0C", "#AC3838"]


lw = 1

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
    'boxplot.medianprops.linewidth' : lw,
    'text.usetex' : True,
    'font.family' : 'serif',
    'axes.linewidth' : 0.2

   }
mpl.rcParams.update(params)      

scale = 0.5


#########################
    

def import_and_test(mapping):

    # import and process train data
    mapping.import_data('train')
    mapping.process_data('train')


    # import and process test data
    mapping.import_data('test')
    mapping.process_data('test')
    
    # dimensionality reduction
    mapping.run_dimensionality_reduction()

    # separate by maneuver
    mapping.separate_datasets()
    
    mapping.augment_on_reduced_data()

    # test regressors
    mapping.implement_mapping()

    return mapping


#########################
    

def mapping_procedure(settings):


    mapping = hri.HRI_mapping()
    
    # working folder depends on pc
    if settings.windows:
        # Windows folder
        mapping.settings.data_folder = 'G:\\My Drive\\Matteo\\EPFL\\LIS\\PhD\\Natural_Mapping\\DATA\\acquired_data\\Experimental'
    #    mapping.settings.data_folder = 'C:\\Users\\macchini\\Documents\\Local_data'        # temporary
        mapping.settings.interface_folder = os.path.normpath(os.path.join(mapping.settings.data_folder, '..', 'interfaces'))
        mapping._create_hri_folders()
    if settings.dronedome:
        # DroneDome folder
        mapping.settings.data_folder = 'D:\\LIS\\Matteo\\DATA\\acquired_data'
        mapping.settings.interface_folder = os.path.normpath(os.path.join(mapping.settings.data_folder, '..', 'interfaces'))
        mapping._create_hri_folders()
    if settings.mac:
        # DroneDome folder
        mapping.settings.data_folder = '/Volumes/GoogleDrive/My Drive/Matteo/EPFL/LIS/PhD/Natural_Mapping/DATA/acquired_data/Non_experimental/'
        mapping.settings.interface_folder = os.path.normpath(os.path.join(mapping.settings.data_folder, '..', 'interfaces'))
        mapping._create_hri_folders()

    # setting current home folder
    mapping.settings.home_folder = os.path.dirname(os.path.realpath(__file__))
        
    ### USER ###
    mapping.user.settings = {'train' : {'subject' : [settings.subject_name],
                                'input' : [settings.input_device],
                                'maneuver' : [''],
                                'instance' : ['inst_1']
                                }}
    
    mapping.user.settings['test'] = mapping.user.settings['train']
    
    ### FIT SETTINGS ###
                     
    mapping.settings.fit_un_to_max = True
    mapping.settings.init_values_to_remove = 0
    
    # options : 'av delay', 'variance'
    mapping.settings.pll_mode = 'variance'
    
    mapping.settings.pll_av_delay = 100
    mapping.settings.dim_reduction = True
    mapping.data_augmentation = False
    #        mapping.augmentation_add_noise = False
    mapping.settings.augmentation_interpolate_to_zero = False
    mapping.settings.shuffle_data = True
    #        mapping.regress_each = False.
    #        mapping.state_feedback = False
    
    mapping.settings.variance_suff = 0.08
    mapping.settings.limbs_reduced = None
    
    # options : 'full', 'angles', 'euler', 'quaternions'
    mapping.settings.features_used = 'euler'
    # options : 'full', 'reduced', 'search'
    mapping.settings.regressors = 'SVR'
    # options : 'bones', 'signals'
    mapping.settings.dim_reduction_type = 'signals'
            
    # options : 'split', 'different maneuvers'
    mapping.settings.train_test_mode = 'split'
    mapping.settings.split_factor_train = 0.1
    
    ### MORE SETTINGS ###
    
    mapping.use_data_augmentation(activate = False, interpolate_to_zero = False, add_noise = False)
    mapping.use_data_downsampling(activate = False, frac = 1)
    mapping.choose_mapping_type(settings.control_style)
    
    mapping.settings.is_final_mapping = True
    
    ### LAUNCH ALGORITHM ###
    
    # import and test
    mapping = import_and_test(mapping)
    
    # plot results
    mapping.plot_test_results()
    
    return mapping


#########################    
    
def plot_from_df(df, field, ax, label = None, color = 'b'):
    
    ax.plot(np.arange(1, len(df[field])+1), df[field], color = color)
    
    
def norm(data):
    
    for i in list(data):
        m = np.mean(data[i])
        data[i] = data[i]-m
        
        s = np.std(data[i])
        data[i] = data[i]/s
        
    return data



def box(ax):
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylim([-4, 4])
        
#    ax.spines['right'].set_visible(False)
#    ax.spines['top'].set_visible(False)
#    ax.spines['bottom'].set_visible(False)
    
    

def plot_output(file, sv = False):
    
    file = norm(file)
    
    params = {
        'figure.figsize': [6*scale, 1*scale]
        }
    mpl.rcParams.update(params)  

    plt.figure()
    ax = plt.subplot(1, 1, 1)
    
    plot_from_df(file, 'roll', ax, label = r'\textit{$\theta$}', color = c1)
    plot_from_df(file, 'pitch', ax)
    
    box(ax)
    
    if sv:
        savefig('outputs.pdf', bbox_inches='tight') 


def plot_output_separated(file, sv = False):
    
    file = norm(file)
    
    
    params = {
        'figure.figsize': [2*scale, 2*scale]
        }
    mpl.rcParams.update(params)  

    plt.figure()
    
    for idx,i in enumerate(['roll', 'pitch']):
        
        ax = plt.subplot(2, 1, idx+1)
        plot_from_df(file, i, ax, color = c2)
    
        box(ax)
    
    if sv:
        savefig('outputs_sep.pdf', bbox_inches='tight') 


def plot_pitch_3_test(file, sv = False):
    
    file = norm(file)
    
    params = {
        'figure.figsize': [2*scale, 1*scale]
        }
    mpl.rcParams.update(params)  

    plt.figure()
    ax = plt.subplot(1, 1, 1)
    
    plot_from_df(file, 'pitch_3', ax, color = c1)
    
    box(ax)
    
    if sv:
        savefig('test.pdf', bbox_inches='tight') 


def plot_some(file, idx, sv = False):
    
    file = norm(file)
    
    params = {
        'figure.figsize': [2*scale, len(idx)*scale]
        }
    mpl.rcParams.update(params)  

    plt.figure()
    
    for j,i in enumerate(idx):
        ax = plt.subplot(len(idx), 1, j+1)
        
        plot_from_df(file, i, ax, color = c1)
    
        box(ax)
    
    if sv:
        savefig('test.pdf', bbox_inches='tight') 


def plot_feats(file, feats, sv = False):
    
    file = norm(file)
    
    params = {
        'figure.figsize': [2*scale, 3*scale]
        }
    mpl.rcParams.update(params)  

    plt.figure()
    
    for idx,i in enumerate(feats):
        
        ax = plt.subplot(len(feats), 1, idx+1)
        plot_from_df(file, i, ax, color = c1)
    
        box(ax)

    if sv:
        savefig('feats.pdf', bbox_inches='tight') 

        

def plot_cca(file, feats, cca, sv = False):
    
    file = norm(file)
    
    params = {
        'figure.figsize': [2*scale, 2*scale]
        }
    mpl.rcParams.update(params)  

    plt.figure()
    
    l = []
    
    for i in feats:
        l.append(file[i].values)
        
    c = []
    
    weights = []
        
    for idx,i in enumerate(cca):
        
        weights.append(i.x_weights_)
        
    
    out = []    
    
    c.append(weights[0][0] * l[0] + weights[0][1] * l[1] + weights[0][2] * l[2])
    c.append(weights[1][0] * l[0] + weights[1][1] * l[1] + weights[1][2] * l[2])
        
        

    plt.figure()
    
    for idx,i in enumerate(c):
        
        if idx==1:
            i = -i
        
        ax = plt.subplot(2, 1, idx+1)
        ax.plot(i, color = c1)
    
        box(ax)
        
    if sv:
        savefig('cca.pdf', bbox_inches='tight') 
    
    

import basic_settings as settings

settings.control_style = 'new'
settings.subject_name = 'pilot_x4'

mapping_current = mapping_procedure(settings)

# getting data before sync
    
deb = mapping_current._debug_process

# getting last data before merging

data_before_pll = mapping_current._debug_process['df_pll']

data_reor = data_before_pll

#order = [3, 4, 2, 5, 8, 7, 1, 0]
##
#data_reor = []
#
#for i in order:
#    data_reor.append(data_before_pll[i])
    
#
data1 = data_reor[1]
for i in data_reor[2:]:
    data1 = pd.concat([data1, i])

data = data1.copy()

#data = data.head(36000)

#data = data.iloc[:-200]

sv = True

plot_output(data, sv)

plot_output_separated(data, sv)
    
#data = data.iloc[:-1]

idx = ['roll_13','pitch_13', 'yaw_13']

plot_some(data, idx, sv)
    

feats = ['roll_3', 'pitch_3', 'yaw_3', ]

plot_feats(data, feats, sv)

cca = mapping_current.dimred

plot_cca(data, feats, cca, sv)
