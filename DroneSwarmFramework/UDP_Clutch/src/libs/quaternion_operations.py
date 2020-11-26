#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 16:15:39 2018

@author: matteomacchini
"""

#########################

import numpy as np

#########################
    

def Qnormalize(Q):
    if type(Q) is list:
        Q=np.array(Q);
    elif type(Q) is tuple:
        Q=np.array(Q);
    lqshp = len(Q.shape)
    if lqshp==1:
        if Q.shape[0] % 4 == 0:
            if Q.shape[0] > 4:
                Q.shape=[Q.size/4,4]
        else:
            print ("Wrong number of elements")
            sys.exit(1)
    elif Q.shape[lqshp-1] != 4:
        Q.shape=[Q.size/4,4]
    if lqshp==1:
        Q /= np.sqrt(np.power(Q,2).sum(axis=0))
    else:
        Q = (1/np.sqrt(np.power(Q,2).sum(axis=1)) * Q.T).T
    return(Q);
    

def Q2EA(Q,EulerOrder="zyx",tol = 10 * np.spacing(1), ichk=False, ignoreAllChk=False):
    # Implementation of quaternion to Euler angles based on D. M. Henderson 1977
    # Shuttle Program. Euler Angles, Quaternions, and Transformation Matrices Working Relationships.
    # National Aeronautics and Space Administration (NASA), N77-31234/6
    # Q - [q1,q2,q3,q4] to EA - [psi,theta,phi]
    # Madgwick (zyx) originaly used Q = [phi, theta, psi]
    # Jose Gama 2014
    if type(Q) is list:
        Q=np.array(Q);
    elif type(Q) is tuple:
        Q=np.array(Q);
    if len(Q.shape)==1:
        if Q.shape[0] % 4 == 0:
            Q.shape=[int(Q.size/4),4]
        else:
            print ("Wrong number of elements")
            sys.exit(1)
    if Q.shape[1] != 4:
        Q.shape=[Q.size/4,4]
    if ~ignoreAllChk:
        if ichk and (abs(Q) > tol).any():
            print ("Warning: (At least one of the) Input quaternion(s) is not a unit vector\n")
    # Normalize quaternion(s) in case of deviation from unity.
    Q = Qnormalize(Q)
    if (EulerOrder in ["zyx","zxy","yxz","xzy","xyz","yzx","zyz","zxz","yxy","yzy","xyx","xzx"])==False:
        print("Invalid input Euler angle order")
        sys.exit(1)
    N=Q.shape[0]
    if ignoreAllChk==False:
        if ichk and (abs(np.sqrt(np.power(Q,2).sum(axis=1) - 1)) > tol).any():
            print("Warning: (At least one of the) Input quaternion(s) is not a unit vector")

    Q0 = Q[:,0]
    Q1 = Q[:,1]
    Q2 = Q[:,2]
    Q3 = Q[:,3]

    if EulerOrder=="zyx":
        EA = np.c_[np.arctan2((2*(Q2*Q3 + Q0*Q1)),(1-2*(np.power(Q1,2) + np.power(Q2,2)))),
                    np.arcsin((2*(Q0*Q2 - Q1*Q3))),
                    np.arctan2((2*(Q0*Q3 + Q1*Q2)),(1-2*(np.power(Q2,2) + np.power(Q3,2))))]
    elif EulerOrder=="yxz":
        EA = np.c_[np.arctan2(2*(Q1*Q3 + Q0*Q2), 1-2*(np.power(Q1,2) + np.power(Q2,2))), np.arctan2(-(2*(Q2*Q3 - Q0*Q1)),np.sqrt(1-np.power(2*(Q2*Q3 - Q0*Q1),2))),np.arctan2((2*(Q1*Q2 + Q0*Q3)),(np.power(Q0,2) - np.power(Q1,2) + np.power(Q2,2)- np.power(Q3,2)))]
    elif EulerOrder=="xzy":
        EA = np.c_[ - np.arctan2(-(2*(Q2*Q3 + Q0*Q1)),(np.power(Q0,2) - np.power(Q1,2) + np.power(Q2,2)- np.power(Q3,2))), np.arctan2(-(2*(Q1*Q2 - Q0*Q3)),np.sqrt(1-np.power(2*(Q1*Q2 - Q0*Q3),2))),np.arctan2((2*(Q1*Q3 + Q0*Q2)),(np.power(Q0,2) + np.power(Q1,2) - np.power(Q2,2) - np.power(Q3,2)))]
    elif EulerOrder=="zxy":
        EA = np.c_[np.arctan2(-(2*(Q1*Q2 - Q0*Q3)),(np.power(Q0,2) - np.power(Q1,2) + np.power(Q2,2)- np.power(Q3,2))), np.arctan2((2*(Q2*Q3 + Q0*Q1)),np.sqrt(1-np.power(2*(Q2*Q3 + Q0*Q1),2))),np.arctan2(-(2*(Q1*Q3 - Q0*Q2)),(np.power(Q0,2) - np.power(Q1,2) - np.power(Q2,2) + np.power(Q3,2)))]
    elif EulerOrder=="yzx":
        EA = np.c_[np.arctan2(-(2*(Q1*Q3 - Q0*Q2)),(np.power(Q0,2) + np.power(Q1,2) - np.power(Q2,2) - np.power(Q3,2))), np.arctan2((2*(Q1*Q2 + Q0*Q3)),np.sqrt(1-np.power(2*(Q1*Q2 + Q0*Q3),2))),np.arctan2(-(2*(Q2*Q3 - Q0*Q1)),(np.power(Q0,2) - np.power(Q1,2) + np.power(Q2,2)- np.power(Q3,2)))]
    elif EulerOrder=="xyz":
        EA = np.c_[np.arctan2(-(2*(Q2*Q3 - Q0*Q1)),(np.power(Q0,2) - np.power(Q1,2) - np.power(Q2,2) + np.power(Q3,2))), np.arctan2((2*(Q1*Q3 + Q0*Q2)),np.sqrt(1-np.power(2*(Q1*Q3 + Q0*Q2),2))),np.arctan2(-(2*(Q1*Q2 - Q0*Q3)),(np.power(Q0,2) + np.power(Q1,2) - np.power(Q2,2) - np.power(Q3,2)))]
    elif EulerOrder=="zyz":
        EA = np.c_[np.arctan2((2*(Q2*Q3 - Q0*Q1)),(2*(Q1*Q3 + Q0*Q2))), np.arctan2(np.sqrt(1-np.power(np.power(Q0,2) - np.power(Q1,2) - np.power(Q2,2) + np.power(Q3,2),2)),(np.power(Q0,2) - np.power(Q1,2) - np.power(Q2,2) + np.power(Q3,2))),np.arctan2((2*(Q2*Q3 + Q0*Q1)),-(2*(Q1*Q3 - Q0*Q2)))]
    elif EulerOrder=="zxz":
        EA = np.c_[np.arctan2((2*(Q1*Q3 + Q0*Q2)),-(2*(Q2*Q3 - Q0*Q1))), np.arctan2(np.sqrt(1-np.power(np.power(Q0,2) - np.power(Q1,2) - np.power(Q2,2) + np.power(Q3,2),2)),(np.power(Q0,2) - np.power(Q1,2) - np.power(Q2,2) + np.power(Q3,2))),np.arctan2((2*(Q1*Q3 - Q0*Q2)),(2*(Q2*Q3 + Q0*Q1)))]
    elif EulerOrder=="yxy":
        EA = np.c_[np.arctan2((2*(Q1*Q2 - Q0*Q3)),(2*(Q2*Q3 + Q0*Q1))), np.arctan2(np.sqrt(1-np.power(np.power(Q0,2) - np.power(Q1,2) + np.power(Q2,2)- np.power(Q3,2),2)),(np.power(Q0,2) - np.power(Q1,2) + np.power(Q2,2)- np.power(Q3,2))),np.arctan2((2*(Q1*Q2 + Q0*Q3)),-(2*(Q2*Q3 - Q0*Q1)))]
    elif EulerOrder=="yzy":
        EA = np.c_[np.arctan2((2*(Q2*Q3 + Q0*Q1)),-(2*(Q1*Q2 - Q0*Q3))), np.arctan2(np.sqrt(1-np.power(np.power(Q0,2) - np.power(Q1,2) + np.power(Q2,2)- np.power(Q3,2),2)),(np.power(Q0,2) - np.power(Q1,2) + np.power(Q2,2)- np.power(Q3,2))),np.arctan2((2*(Q2*Q3 - Q0*Q1)),(2*(Q1*Q2 + Q0*Q3)))]
    elif EulerOrder=="xzx":
        EA = np.c_[np.arctan2((2*(Q1*Q3 - Q0*Q2)),(2*(Q1*Q2 + Q0*Q3))), np.arctan2(np.sqrt(1-np.power(np.power(Q0,2) + np.power(Q1,2) - np.power(Q2,2) - np.power(Q3,2),2)),(np.power(Q0,2) + np.power(Q1,2) - np.power(Q2,2) - np.power(Q3,2))),np.arctan2((2*(Q1*Q3 + Q0*Q2)),-(2*(Q1*Q2 - Q0*Q3)))]
    elif EulerOrder=="xyx":
        EA = np.c_[np.arctan2((2*(Q1*Q2 + Q0*Q3)),-(2*(Q1*Q3 - Q0*Q2))), np.arctan2(np.sqrt(1-np.power(np.power(Q0,2) + np.power(Q1,2) - np.power(Q2,2) - np.power(Q3,2),2)),(np.power(Q0,2) + np.power(Q1,2) - np.power(Q2,2) - np.power(Q3,2))),np.arctan2((2*(Q1*Q2 - Q0*Q3)),(2*(Q1*Q3 + Q0*Q2)))]
    else:
        print("Invalid input Euler angle order")
        sys.exit(1)
    #EA = EA * (180/pi) # (Nx3) Euler angles in degrees
    theta  = EA[:,1]       # (Nx1) Angle THETA in degrees
    # Check EA
    if ignoreAllChk==False:
        if isinstance(EA, complex):
            print("Unreal\nUnreal Euler EA. Input resides too close to singularity.\nPlease choose different EA type.")
            sys.exit(1)
        # Type 1 rotation (rotations about three distinct axes)
        # THETA is computed using ASIN and ranges from -90 to 90 degrees

    if ignoreAllChk==False:
        if EulerOrder[0] != EulerOrder[2]:
            singularities = np.abs(theta) > 89.9*(np.pi/180) # (Nx1) Logical index
            singularities[np.where(np.isnan(singularities))] = False
            if len(singularities)>0:
                if (singularities).any():
                    firstsing = np.where(singularities)[0] #which(singularities)[1] # (1x1)
                    print("Input rotation ", firstsing, " resides too close to Type 1 Euler singularity.\nType 1 Euler singularity occurs when second angle is -90 or 90 degrees.\nPlease choose different EA type.")
                    sys.exit(1)
        else:
            # Type 2 rotation (1st and 3rd rotation about same axis)
            # THETA is computed using ACOS and ranges from 0 to 180 degrees
            singularities = (theta<0.1*(np.pi/180)) | (theta>179.9*(np.pi/180)) # (Nx1) Logical index
            singularities[np.where(np.isnan(singularities))] = False
            if (len(singularities)>0):
                if((singularities).any()):
                    firstsing = np.where(singularities)[0] # (1x1)
                    print("Input rotation ", firstsing, " resides too close to Type 2 Euler singularity.\nType 2 Euler singularity occurs when second angle is 0 or 180 degrees.\nPlease choose different EA type.")
                    sys.exit(1)
    return(EA)