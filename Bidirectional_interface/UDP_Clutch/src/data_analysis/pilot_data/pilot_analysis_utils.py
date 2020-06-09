#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 02:19:54 2019

@author: lis
"""
from sklearn import metrics
from sklearn.utils import shuffle
import numpy as np

def test_maxmin(mapp, reg):
        
        # reset results
        mapp.test_results = []
        
        mapp._get_fit_datasets()
            
        train_dataset = mapp.train_dataset
        test_dataset = mapp.test_dataset
        
        if mapp.dim_red_done:
            feats = [x for x in list(train_dataset) if 'input' in x]
        else:
            feats = mapp.select_features()
        
        print('')
        print('')
        print('Fitting...')
        print('')
        print('')
        
        
        # TODO : as setting
        mapp.settings.maxmin_style = 'linreg'
        
        if mapp.settings.maxmin_style == 'linreg':
            X_df = mapp.motion_data['train'][feats]
            Y_df = mapp.test_dataset[mapp.settings.outputs]
            
            # get index of last samples
            idx = Y_df.index.values
            
            idx_diff = np.diff(idx)
            
            used_idx = np.hstack([np.array([0]), np.where(idx_diff != 1)[0], np.array([len(idx)-1])])
            
            X = X_df.values[used_idx]
            zs = Y_df.values[used_idx]
        
        [X, y] = [mapp.motion_data['train'][feats].values, mapp.test_dataset[mapp.settings.outputs].values]
        
        # TODO : pca as an option
        mapp.settings.dimred_style = 'cca'
        # if mapp.settings.pca_reduce_to_n_of_outputs:
        # PERFORM PCA
        
        if not mapp.dim_red_done:
            if mapp.settings.dimred_style == 'pca':
                mapp.dimred = decomposition.PCA(n_components=len(mapp.settings.outputs))
                mapp.dimred.fit(X)
                X = mapp.pca.transform(X)
            elif mapp.settings.dimred_style == 'cca':
                mapp.dimred = mapp.implement_cca(X, y)
                X = mapp.transform_cca(X, mapp.dimred)
        
        # predict
        y_score = reg.predict(X)
        
        print('Done.')
        
        mapp.test_results.append({
                    "mse":np.inf,
                    "y_true":y,
                    "x":test_dataset[feats],
                    "y_score":y_score
                    })
    
        if not np.isnan(y_score).any():
            mapp.test_results[-1]["mse"] = metrics.mean_squared_error(y, y_score)
            
            err = mapp.test_results[-1]["mse"]
    
        if mapp.settings.plot_reg_score:
            
            mapp._plot_score(only_true = mapp.settings.plot_score_only_true)
    
        mapp.plot_regression_inputs_outputs(feats)
        
        M_v = [np.max(x) for x in np.transpose(X)] if mapp.dim_red_done else [np.max(x) for x in np.transpose(mapp.transform_cca(X, mapp.dimred))]
        m_v = [np.min(x) for x in np.transpose(X)] if mapp.dim_red_done else [np.min(x) for x in np.transpose(mapp.transform_cca(X, mapp.dimred))]
        
        mapp.test_info = {"settings":mapp.settings,
                "results":mapp.test_results[:],
                "feats":feats,
                "train_dataset":train_dataset,
                "test_dataset":test_dataset,
                "fit_x":X,
                "fit_y":y,
                "max_values":M_v,
                "mmi_values":m_v,
                "maxmin_map":mapp.minmax_map,
                "dim_red":mapp.dimred
                }
        
        return err
    
    
#########################
    
    
def test_new(self, reg):
    
    self._get_fit_datasets()
        
    train_dataset = self.train_dataset
    test_dataset = self.test_dataset
    
    if self.dim_red_done:
        feats = [x for x in list(train_dataset) if 'input' in x]
    else:
        feats = self.select_features()
        
        
    if self.settings.shuffle_data:
        X, y = shuffle(train_dataset[feats].values, train_dataset[self.settings.outputs].values, random_state = 0)
    else:
        [X, y] = [train_dataset[feats].values, train_dataset[self.settings.outputs].values]
    
    # TODO : pca as an option
    self.settings.dimred_style = 'cca'
    # if self.settings.pca_reduce_to_n_of_outputs:
    # PERFORM PCA
    if not self.dim_red_done:
        if self.settings.dimred_style == 'pca':
            self.pca = decomposition.PCA(n_components=len(self.settings.outputs))
            self.pca.fit(X)
            X = self.pca.transform(X)
        elif self.settings.dimred_style == 'cca':
            self.pca = self.implement_cca(X, y)
            X = self.transform_cca(X, self.pca)
    
    y_true = test_dataset[self.settings.outputs].values
    
    y_score = reg.predict(test_dataset[feats].values) if self.dim_red_done else reg.predict(self.transform_cca(test_dataset[feats].values, self.pca))
    

    if not np.isnan(y_score).any():
        self.test_results[-1]["mse"] = metrics.mean_squared_error(y_true, y_score)
        
        err = metrics.mean_squared_error(y_true, y_score)
        
    return err
    
    
def test_nonpers(l, lin):

    list_idx =list(range(0, len(l)))
    err = []    
    
    for idx,i in enumerate(l):
        
        print('mapping ' + str(idx))
        
        for j in list_idx:
            if idx!=j:
                
                print('reg ' + str(j))
                
                if lin:
                    reg = l[j].minmax_map
                    
                    print(reg.steps[-1][1].estimators_[0].coef_)
                    
                    err.append(test_maxmin(i, reg))
                    
                    print('error ' + str(err[-1]))
                else:
                    reg = l[j].test_results[0]['reg']
                    
                    err.append(test_new(i, reg))
                    
                    print('error ' + str(err[-1]))
    
    return err