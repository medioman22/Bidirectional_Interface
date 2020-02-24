from termcolor import colored
from scipy import stats
from numpy.random import seed
from scipy.stats import kruskal
from scipy.stats import levene

import numpy as np

def remove_outliers_iqr(X):

    q1, q3= np.percentile(X,[25,75])
    iqr = q3 - q1

    lower_bound = q1 -(1.5 * iqr) 
    upper_bound = q3 +(1.5 * iqr)
    
    
    Y = X[:]
    
    if type(Y) is not list:
        Y = Y.tolist()
        
    for idx,i in enumerate(Y):
        if i<lower_bound or i>upper_bound:
            
                Y.remove(i)
            
    
    return Y

def str_from_p(p):
    
    if p<0.01:
        add_str = ' !!!!!!!!!!'
    elif p<0.05:
        add_str = ' !!!!!!'
    elif p<0.1:
        add_str = ' !'
    else:
        add_str = ''
        
    return add_str

def print_p(p):
    
    col = None
    
    if p<0.01:
        col = 'green'
    elif p<0.05:
        col = 'yellow'
    elif p<0.1:
        col = 'red'
        
    if col is not None:
        print(colored('p = '+ str(p) + str_from_p(p), col))
    else:
        print('p = '+ str(p) + str_from_p(p))
        
def t_test_kruskal(X, Y):
    
    # Kruskal-Wallis H-test
    X = remove_outliers_iqr(X)
    Y = remove_outliers_iqr(Y)
    
    # seed the random number generator
    seed(1)
    
    # compare samples
    stat, p = kruskal(X, Y)
    
    return [stat, p]

def t_test_levene(X, Y):
    
    # Kruskal-Wallis H-test
    X = remove_outliers_iqr(X)
    Y = remove_outliers_iqr(Y)
    
    # seed the random number generator
    seed(1)
    
    # compare samples
    stat, p = levene(X, Y)
    
    return [stat, p]