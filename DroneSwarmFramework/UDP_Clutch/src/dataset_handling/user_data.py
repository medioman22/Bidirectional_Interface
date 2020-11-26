#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 17:46:13 2018

@author: matteomacchini
"""


#####################################################

import sys,os

import numpy as np

import context

import libs.quaternion_operations as quat_op
import utilities.utils as utils
from settings.settings import get_settings

#####################################################
from abc import ABC, abstractmethod

settings = get_settings()

""" ABSTRACT CLASS """


class UserData(ABC):



    ### INIT FUNCTION ###


    @abstractmethod
    def __init__(self, values):
        """ initialize sctructure """

        self.values = values

        self.settings = settings

        self.first_data = None


    ### PRIVATE FUNCTIONS ###


    @abstractmethod
    def _quat_idx(self):
        """ gets index of quaternions """

        return range(self.settings['quat_loc'], self.settings['quat_loc'] + self.settings['quat_len'])

    #####################################################

    @abstractmethod
    def _quaternion_to_values(self, quat):
        """ quaternion object to numpy array """

        quat_val = np.array([quat.x, quat.y, quat.z, quat.w])

        return quat_val

    #####################################################

    @abstractmethod
    def _relativize_bone(self, angles_to_correct, with_respect_to):
        """ set rotation relative to parent bone """

        if with_respect_to == 0:
            return

        ref_idx = self._search_bone_per_index(with_respect_to)
        abs_idx = self._search_bone_per_index(angles_to_correct)

        # extract rows
        ref_row = self.values[ref_idx].reshape(-1)
        abs_row = self.values[abs_idx].reshape(-1)

        # extract quaternions
        ref_quat = ref_row[self.settings['quat_loc']: self.settings['quat_loc'] + self.settings['quat_len']]
        abs_quat = abs_row[self.settings['quat_loc']: self.settings['quat_loc'] + self.settings['quat_len']]

        ref_quat_q = self._values_to_quaternion(ref_quat)
        abs_quat_q = self._values_to_quaternion(abs_quat)

        # compute difference
        rel_quat_q = ref_quat_q.inverse()*abs_quat_q

        # stick back in array
        abs_row[self.settings['quat_loc']: self.settings['quat_loc'] + self.settings['quat_len']] = self._quaternion_to_values(rel_quat_q)

        self.values[abs_idx] = abs_row

    #####################################################

    @abstractmethod
    def _search_bone_per_index(self, idx):
        """ return bone with index i """

        arr = self.values[:,0]

        i = np.where(idx==arr[:,None])[0]

        return i

    #####################################################

    @abstractmethod
    def _values_to_quaternion(self, quat_val):
        """ numpy array to quaternion object """

        quat = np.quaternion(quat_val[3], quat_val[0], quat_val[1], quat_val[2])

        return quat


    ### PUBLIC FUNCTIONS ###


    @abstractmethod
    def compute_ea_bone(self, a, str):
        """ compute single euler angle """

        quat_val = a[self.settings['quat_loc']: self.settings['quat_loc'] + self.settings['quat_len']]

        eul = quat_op.Q2EA((quat_val[3], quat_val[0], quat_val[1], quat_val[2]), EulerOrder="zyx", ignoreAllChk=True)[0]

        #            print(eul)

        # right order [xzy] : due to Motive settings
        return np.array(eul)

    #####################################################

    @abstractmethod
    def compute_ea(self):
        """ compute all euler angles for a given skeleton """

        # pre-allocation
        eul_skel = np.zeros([np.size(self.values, 0), np.size(self.values, 1) + 3])

        eul_skel[:, :np.size(self.values, 1)] = self.values

        tot_t = 0

        eul = np.apply_along_axis(self.compute_ea_bone, 1, self.values, self)

        eul_skel[:,-3:] = eul

        self.values = eul_skel

    #####################################################

    @abstractmethod
    def keep_features(self, feats):
        """ keep only given features """

        # size of mask : ID(1) + pos(3) + quat(3) + eul(3) = 11

        # mask depends on feats
        if feats == 'all':
            mask = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        elif feats == 'angles':
            mask = np.array([4, 5, 6, 7, 8, 9, 10])
        elif feats == 'euler':
            mask = np.array([8, 9, 10])
        elif feats == 'quaternions':
            mask = np.array([4, 5, 6, 7])

        self.values = self.values[:,mask]

    #####################################################

    @abstractmethod
    def keep_used_body_parts(self, parts = None):
        """ keep only given bones """

        if parts is None:
            parts = self.settings['used_body_parts']

        a = self._search_bone_per_index(parts)

        self.values = self.values[a,:]


    #####################################################


    @abstractmethod
    def normalize(self, av, std, feats = 'all'):
        """ normalized all signals """

        if feats == 'all':
            [self.values, garbage] = utils.normalize(self.values, [av, std])
        elif feats == 'euler':
            [self.values[:, -3:], garbage] = utils.normalize(self.values[:, -3:], [av, std])


    #####################################################

    @abstractmethod
    def relativize(self):
        """ set all rotations relative to base bone """

        for i in range(len(settings['used_body_parts'])):
            self._relativize_bone(settings['used_body_parts'][i], settings['kinematic_chain'][i])

    #####################################################

    @abstractmethod
    def unbias(self):
        """ restore initial rotation """

        for i in range(np.size(self.values, 0)):
            bias_quat = self.values[i,:][self.settings['quat_loc']: self.settings['quat_loc'] + self.settings['quat_len']]
            ref_quat = self.first_data.values[i,:][self.settings['quat_loc']: self.settings['quat_loc'] + self.settings['quat_len']]

            #unbias
            self.values[i][self.settings['quat_loc']: self.settings['quat_loc'] + self.settings['quat_len']] = self._quaternion_to_values(self._values_to_quaternion(ref_quat).inverse()*self._values_to_quaternion(bias_quat))

    #####################################################

    @abstractmethod
    def extract_features(self, feats):
        """ get a subset of arbitrary features """

        out = []

        for i in feats:
            n = int(utils.find_string(i, '\d+'))
            limb = utils.find_string(i, '.+_')[:-1]
            out.append(self.values[self._search_bone_per_index(n),self.feat_dict[limb]])

        return np.array(out)


class skeleton(UserData):


    ### INIT FUNCTION ###


    def __init__(self, values):
        """ initialize sctructure """
        super().__init__(values)

        self.settings['quat_loc'] = 4
        self.settings['quat_len'] = 4

        self.n_data_per_rigid_body = 8

        self.feat_dict = {'ID':0,
                          'pos_x':1,
                          'pos_y':2,
                          'pos_z':3,
                          'quat_x':4,
                          'quat_y':5,
                          'quat_z':6,
                          'quat_w':7,
                          'roll':8,
                          'pitch':9,
                          'yaw':10
                          }


    ### PRIVATE FUNCTIONS ###


    def _quat_idx(self):
        return super()._quat_idx()

    #####################################################

    def _quaternion_to_values(self, quat):
        return super()._quaternion_to_values(quat)

    #####################################################

    def _relativize_bone(self, angles_to_correct, with_respect_to):
        super()._relativize_bone(angles_to_correct, with_respect_to)

    #####################################################

    def _search_bone_per_index(self, idx):
        return super()._search_bone_per_index(idx)

    #####################################################

    def _values_to_quaternion(self, quat_val):
        return super()._values_to_quaternion(quat_val)


    ### PUBLIC FUNCTIONS ###


    def compute_ea_bone(self, a, str):
        return super().compute_ea_bone(a, str)

    #####################################################

    def compute_ea(self):
        super().compute_ea()

    #####################################################

    def normalize(self, av, std, feats = 'all'):
        super().normalize(av, std, feats)

    #####################################################

    def keep_features(self, feats):
        super().keep_features(feats)

    #####################################################

    def keep_used_body_parts(self, parts = None):
        super().keep_used_body_parts(parts)

    #####################################################

    def relativize(self):
        super().relativize()

    #####################################################

    def unbias(self):
        super().unbias()

    #####################################################

    def assign_first_skel(self, first_data):
        """ assigns first data """

        self.first_data = first_data

    #####################################################

    def extract_features(self, feats):
        """ get a subset of arbitrary features """
        return super().extract_features(feats)


class remote(UserData):


    ### INIT FUNCTION ###


    def __init__(self, values):
        """ initialize sctructure """
        super().__init__(values)


    ### PRIVATE FUNCTIONS ###


    def _quat_idx(self):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def _quaternion_to_values(self, quat):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def _relativize_bone(self, angles_to_correct, with_respect_to):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def _search_bone_per_index(self, idx):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def _values_to_quaternion(self, quat_val):
        raise NameError('this method does not exist for this instance of your class')


    ### PUBLIC FUNCTIONS ###


    def compute_ea_bone(self, a, str):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def compute_ea(self):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def keep_features(self, feats):
        super().keep_features()

    #####################################################

    def keep_used_body_parts(self, parts = None):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def normalize(self, av, std):
        super().normalize(av, std)

    #####################################################

    def relativize(self):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def unbias(self, first_skel):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def extract_features(self, feats):
        pass




class imu(UserData):


    ### INIT FUNCTION ###


    def __init__(self, values):
        """ initialize sctructure """
        super().__init__(values)


    ### PRIVATE FUNCTIONS ###


    def _quat_idx(self):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def _quaternion_to_values(self, quat):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def _relativize_bone(self, angles_to_correct, with_respect_to):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def _search_bone_per_index(self, idx):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def _values_to_quaternion(self, quat_val):
        raise NameError('this method does not exist for this instance of your class')


    ### PUBLIC FUNCTIONS ###


    def compute_ea_bone(self, a, str):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def compute_ea(self):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def keep_features(self, feats):
        super().keep_features()

    #####################################################

    def keep_used_body_parts(self, parts = None):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def normalize(self, av, std):
        super().normalize(av, std)

    #####################################################

    def relativize(self):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def unbias(self, first_skel):
        raise NameError('this method does not exist for this instance of your class')

    #####################################################

    def extract_features(self, feats):
        pass



class imus(UserData):


    ### INIT FUNCTION ###


    def __init__(self, values):
        """ initialize sctructure """
        super().__init__(values)

        self.init_data = None

        self.settings['quat_loc'] = 4
        self.settings['quat_len'] = 4

        self.n_data_per_rigid_body = 8

        self.feat_dict = {'ID':0,
                          'pos_x':1,
                          'pos_y':2,
                          'pos_z':3,
                          'quat_x':4,
                          'quat_y':5,
                          'quat_z':6,
                          'quat_w':7,
                          'roll':8,
                          'pitch':9,
                          'yaw':10
                          }


    ### PRIVATE FUNCTIONS ###


    def _quat_idx(self):
        return super()._quat_idx()

    #####################################################

    def _quaternion_to_values(self, quat):
        return super()._quaternion_to_values(quat)

    #####################################################

    def _relativize_bone(self, angles_to_correct, with_respect_to):
        super()._relativize_bone(angles_to_correct, with_respect_to)

    #####################################################

    def _search_bone_per_index(self, idx):
        return super()._search_bone_per_index(idx)

    #####################################################

    def _values_to_quaternion(self, quat_val):
        return super()._values_to_quaternion(quat_val)


    ### PUBLIC FUNCTIONS ###


    def compute_ea_bone(self, a, str):
        """ compute single euler angle """

        quat_val = a[self.settings['quat_loc']: self.settings['quat_loc'] + self.settings['quat_len']]

        eul = quat_op.Q2EA((quat_val[3], quat_val[0], quat_val[1], quat_val[2]), EulerOrder="zyx", ignoreAllChk=True)[0]

        #            print(eul)

        # right order [xzy] : due to Motive settings
        return np.array(eul)

    #####################################################

    def compute_ea(self):
        super().compute_ea()

    #####################################################

    def normalize(self, av, std, feats = 'all'):
        super().normalize(av, std, feats)

    #####################################################

    def keep_features(self, feats):
        super().keep_features(feats)

    #####################################################

    def keep_used_body_parts(self, parts = None):
        super().keep_used_body_parts(parts)

    #####################################################

    def relativize(self):
        super().relativize()

    #####################################################

    def unbias(self):
        super().unbias()

    #####################################################

    def init_pose(self):
        """ restore initial rotation """

        for i in range(np.size(self.values, 0)):
            bias_quat = self.values[i,:][self.settings['quat_loc']: self.settings['quat_loc'] + self.settings['quat_len']]
            ref_quat = self.init_data.values[i,:][self.settings['quat_loc']: self.settings['quat_loc'] + self.settings['quat_len']]

            #unbias
            self.values[i][self.settings['quat_loc']: self.settings['quat_loc'] + self.settings['quat_len']] = self._quaternion_to_values(self._values_to_quaternion(ref_quat).inverse()*self._values_to_quaternion(bias_quat))


    #####################################################

    def assign_first_skel(self, first_data):
        """ assigns first data """

        self.first_data = first_data


    #####################################################

    def assign_init_skel(self, init_data):
        """ assigns init data """

        self.init_data = init_data

    #####################################################

    def extract_features(self, feats):
        """ get a subset of arbitrary features """
        return super().extract_features(feats)