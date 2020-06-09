# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 12:34:22 2018

@author: macchini
"""

import ExperimentalDataResults

def initialize_settings():
    
    
    settings = {'methods' : None,
                'subjects' : None,
                'methods' : None,
                'interfaces' : None,
                'plot_style' : None,
                'metric' : None,
                'plot' : None,
                'run_av_window' : 10
                }
    
    return settings


def run_data_results_analysis(settings):
    
    exp_data = ExperimentalDataResults.ExperimentalDataResults()
    
    exp_data.set_folder()
    
    #exp_data.set_subjects([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    #exp_data.set_subjects([2])
    exp_data.set_methods(settings['methods'])
    exp_data.set_interfaces(settings['interfaces'])
    
    blah = exp_data.load()
    
    exp_data.process_performance(running_average_window = settings['run_av_window'], method = settings['metric'])
    
    # options : 'multiplot', 'mean-var', 'mean-max-min'
    if settings['plot']:
        exp_data.plot_performance(settings['plot_style'])
    
    return exp_data

# Run as script
if __name__ == '__main__':
    
    settings = initialize_settings()
    
    settings['methods'] = ['simple']
    settings['interfaces'] = ['remote']
    settings['plot_style'] = 'mean-max-min'
    settings['metric'] = 'error'
    settings['run_av_window'] = 1
    settings['plot'] = True



    exp_data = run_data_results_analysis(settings)