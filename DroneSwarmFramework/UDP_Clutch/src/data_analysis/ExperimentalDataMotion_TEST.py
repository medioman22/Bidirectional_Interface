# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 15:19:01 2019

@author: macchini
"""

import ExperimentalDataMotion

def initialize_settings():
    


    settings = {'methods' : None,
                'subjects' : None,
                'methods' : None,
                'interfaces' : None,
                }

    return settings

def run_data_motion_analysis(settings):

    exp_data = ExperimentalDataMotion.ExperimentalDataMotion()

    exp_data.set_folder()

    #exp_data.set_subjects([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    #exp_data.set_subjects([2])
    exp_data.set_methods(settings['methods'])
    exp_data.set_interfaces(settings['interfaces'])

    blah = exp_data.load_ready()

    exp_data.process_motion()

    # options : 'multiplot', 'mean-var', 'mean-max-min'
#    exp_data.plot_performance(style = 'mean-max-min')

    return exp_data

# Run as script
if __name__ == '__main__':

    settings = initialize_settings()

    settings['methods'] = ['simple']
    settings['interfaces'] = ['motive']

    exp_data = run_data_motion_analysis(settings)
