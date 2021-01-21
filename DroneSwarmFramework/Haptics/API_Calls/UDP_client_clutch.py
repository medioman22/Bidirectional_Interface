#!usrbinenv python3
# -- coding utf-8 --

from clutch.clutch import FourClutches
import socket
import struct
import select
import time
import json
import sys
import os

fourcl = FourClutches()

DISTANCE_THRESHOLD = 1
MAXIMUM_MOTOR_INPUT = 99

############# setup UDP communication #############
# function to get the data from Unity


def get_data(my_socket):

    data = []
    # read data as long as packets are coming
    data_ready = False
    data_ready = select.select([my_socket], [], [], 0)[0]

    while data_ready:
    
        t, _ = my_socket.recvfrom(1024)  # buffer size is 1048 bytes
        data.append(t)
        data_ready = False
        data_ready = select.select([my_socket], [], [], 0)[0]
    
    return data

# local IP. Do not change that
UDP_IP = '127.0.0.1'
# socket to which data is being received
UDP_PORT_DISTANCES = 8051
# open the receiving socket
distances_socket = socket.socket(socket.AF_INET,  # Internet
                                 socket.SOCK_DGRAM)  # UDP
distances_socket.bind((UDP_IP, UDP_PORT_DISTANCES))
##################################################


distances_dict = {
                  'frontObstacle': 0,
                  'backObstacle': 0,
                  'leftObstacle': 0,
                  'rightObstacle': 0
                  }


def fillDict(current_data):

    distances_dict['frontObstacle'] = current_data[0]
    distances_dict['backObstacle'] = current_data[1]
    distances_dict['leftObstacle'] = current_data[2]
    distances_dict['rightObstacle'] = current_data[3]


# had to sleep otherwise hardware overwhelmed
time.sleep(2)

# MAIN LOOP
while(True):
    distances = get_data(distances_socket)
    # had to sleep otherwise hardware overwhelmed
    time.sleep(0.05)
    
    if len(distances):
        print('acquired distances, total number=', len(distances))

        # send only the last packet otherwise too many packets sent too fast
        packet = distances[-1]
        # 4 floats
        strs = 'ffff'
        # unpack.
        unpacked = struct.unpack(strs, packet)
        # parse the data
        fillDict(unpacked)
        print(distances_dict)

        state = 0

        if distances_dict['frontObstacle'] < DISTANCE_THRESHOLD:
            state += 1
        if distances_dict['backObstacle'] < DISTANCE_THRESHOLD:
            state += 2
        if distances_dict['leftObstacle'] < DISTANCE_THRESHOLD:
            state += 4
        if distances_dict['rightObstacle'] < DISTANCE_THRESHOLD:
            state += 8
            
        print('state = {}'.format(state))

        fourcl.set_state(state)
    else:
        print('no data')
