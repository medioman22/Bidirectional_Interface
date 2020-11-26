#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 01:42:22 2018

@author: matteomacchini
"""

import os
import Mapping

# settings

in_data = {'subject' : ['pilot1_'],
           'maneuvre' : [''],
           'instance' : ['inst_1', 'inst_2']
           }

out_data = {'subject' : ['pilot1_'],
           'maneuvre' : [''],
           'instance' : ['inst_3']
           }

# options : 'full', 'angles', 'euler', 'quaternions'
input_data = 'euler'

STATE_FEEDBACK = False
DIMENSION_REDUCTION = False

# options : 'full', 'reduced'
REGRESSORS = 'reduced'

only_best_nonlin = False



res_folder = 'results/'
file_name_comp = REGRESSORS + '_' + input_data + '_IN' + '_' + ''.join(in_data['subject']) + '_' + ''.join(in_data['maneuvre']) + '_' + ''.join(in_data['instance']) + '_' + 'OUT' + '_' + ''.join(out_data['subject']) + '_' + ''.join(out_data['maneuvre']) + '_' + ''.join(out_data['instance'])

#file_name_comp = input_data + '_IN' + '_' + ''.join(in_data['subject']) + '_' + ''.join(in_data['maneuvre']) + '_' + ''.join(in_data['instance']) + '_' + 'OUT' + '_' + ''.join(out_data['subject']) + '_' + ''.join(out_data['maneuvre']) + '_' + ''.join(out_data['instance'])

    
files = os.chdir(res_folder)
files = os.listdir()

file_name = [x for x in files if find_in_str(file_name_comp, x) ]

if DIMENSION_REDUCTION:
    file_name = [x for x in file_name if 'DIM_RED_' in x]
else:
    file_name = [x for x in file_name if 'DIM_RED_' not in x]
if STATE_FEEDBACK:
    file_name = [x for x in file_name if 'STATE_FB_' in x]
else:
    file_name = [x for x in file_name if 'STATE_FB_' not in x]
    
    
#file_name = ['IN_pilot1___inst_1inst_2_OUT_pilot1___inst_3_.pkl']

file_name_fin = file_name[0][:-4]

res = load_obj(file_name_fin)

print('Plotting from dataset : ' + file_name_fin)


## put random forest at end
#rf = [x for x in res if 'RandomForest' in x['reg']]
#no_rf = [x for x in res if 'RandomForest' not in x['reg']]
#res = no_rf[:]

nonlin = res[1:]
best_res_nonlin = nonlin[np.argmin([x['mse'] for x in nonlin])]

if only_best_nonlin:
    res = [res[0], best_res_nonlin]
    
# go back    
os.chdir(home_folder)


font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 12}

matplotlib.rc('font', **font)

idx = 0
plt.figure()
plt.xlabel('Regressor #')
plt.ylabel('MSE')
plt.grid('on')
plt.title('Performance')

plt.ylim(0, 500)
plt.xticks(np.arange(1, 3, step=1))

for i in res:
    idx = idx + 1
    if 'MLP' in i['reg']:
        col = 'r'
    elif 'SVR' in i['reg']:
        col = 'g' 
    elif 'LinearRegression' in i['reg']:
        col = 'b' 
    else:
        col = [0.5, 0.5, 0.5]
    plt.bar(idx, i['mse'], color = col)

savefig('Performance_Regressors__' + file_name_fin)

idx = 0
plt.figure()
plt.xlabel('Regressor #')
plt.ylabel('MSE (normalized)')
plt.grid('on')
plt.title('Performance')

norm = np.amax([x['mse'] for x in res])

for i in res:
    idx = idx + 1
    if 'MLP' in i['reg']:
        col = 'r'
    elif 'SVR' in i['reg']:
        col = 'g' 
    elif 'LinearRegression' in i['reg']:
        col = 'b' 
    else:
        col = [0.5, 0.5, 0.5]
    plt.bar(idx, i['mse']/norm, color = col)
        
savefig('Performance_Regressors_norm__' + file_name_fin)

idx = 0
plt.figure()
plt.xlabel('Regressor #')
plt.ylabel('Time [s]')
plt.grid('on')
plt.title('Time to fit')
#plt.ylim(0, 600)

for i in res:
    idx = idx + 1
    if 'MLP' in i['reg']:
        col = 'r'
    elif 'SVR' in i['reg']:
        col = 'g' 
    elif 'LinearRegression' in i['reg']:
        col = 'b' 
    else:
        col = [0.5, 0.5, 0.5]
    plt.bar(idx, i['fit_time'], color = col)
        
savefig('Time_to_fit_Regressors__' + file_name_fin)

idx = 0
plt.figure()
plt.grid('on')
plt.xlabel('Regressor #')
plt.ylabel('Time [s]')
plt.title('time to predict')

for i in res:
    idx = idx + 1
    if 'MLP' in i['reg']:
        col = 'r'
    elif 'SVR' in i['reg']:
        col = 'g' 
    elif 'LinearRegression' in i['reg']:
        col = 'b' 
    else:
        col = [0.5, 0.5, 0.5]
    plt.bar(idx, i['pred_time'], color = col)
        
savefig('Time_to_predict_Regressors__' + file_name_fin)

title = ''

idx = 0

for i in res:
    idx = idx + 1
    y_true = i['y_real']
    y_score = i['y_pred']
    for j in range(0, size(y_true,1)):
        if j==0:
            plt.figure()
            plt.subplot(211)
            if 'MLP' in i['reg']:
                title = 'MultiLayer Perceptron' 
            elif 'SVR' in i['reg']:
                title = 'State Vector Regressor' 
            elif 'LinearRegression' in i['reg']:
                title = 'Linear Regressor' 
            plt.title(title)
            plt.ylabel('Roll [deg]')
        else:
            plt.subplot(212)
            plt.ylabel('Pitch [deg]')
            plt.xlabel('Sample #')
            
        plt.scatter(list(range(1,len(y_true)+1)), y_true[:,j], s=1, c='b', marker="s", label='Real')
        plt.scatter(list(range(1,len(y_score)+1)),y_score[:,j], s=1, c='r', marker="o", label='Predicted')
        plt.grid()
        
        if j==0:
            plt.legend()
    
    savefig('R_P_performance__' + str(idx) + '_' + file_name_fin)