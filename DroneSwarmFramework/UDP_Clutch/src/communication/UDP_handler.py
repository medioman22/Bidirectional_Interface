# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 15:19:28 2018

@author: macchini
"""

import numpy as np
import select
import socket as soc
from socket import timeout
import socket
import struct
import sys

import os,sys

import context

from settings.settings import get_sockets
from settings.settings import get_settings

import time

import logging


sockets = get_sockets()
settings = get_settings()

logging.basicConfig(level=settings['logging_level'])

# NEEDS TO BE SOLVED
class Socket_struct:

    socket = None
    ID = None

    previous_state = 't'            # CAREFUL : 't' is a special message
                                    # don't use it for communication

    pass



class UDP_handler():


    def __init__(self):

        self.timeout = 0.001        # 1ms to read before timeout

        self.sockets = sockets


    """"""""""""""""""""""""""""""
    """   PRIVATE  FUNCTIONS   """
    """"""""""""""""""""""""""""""


    def _setup_socket(self, IP, PORT, ID, timeout = 0.001):

        return setup_socket(IP, PORT, ID, timeout)


    #########################


    def _udp_read(self, socket_struct, keep_last = False):

        return udp_read(socket_struct, keep_last = keep_last)

    #########################


    def _udp_read_last(self, socket_struct, keep_last = False):

        return udp_read_last(socket_struct, keep_last = keep_last)


    #########################


    def _udp_process(self, data, socket_struct):

        return udp_process(data, socket_struct)

    #########################


    def _udp_write(self, msg):

        udp_write(self.sockets, msg)


    """"""""""""""""""""""""
    """ PUBLIC FUNCTIONS """
    """"""""""""""""""""""""


    def close_sockets(self):

        self.sockets = close_sockets(self.sockets)


    #########################


    def setup_sockets(self):

        self.sockets = setup_sockets(self.sockets, self.timeout)


"""#######################"""
"""#######################"""
"""#######################"""


def close_sockets(sockets = sockets):

    if sockets['read_unity_flag'] is None:
        print('unity read flag socket not open')
    else:
        # close unity read flag socket
        sockets['read_unity_flag'].socket.close()
        sockets['read_unity_flag'] = None

    if sockets['read_unity_control'] is None:
        print('unity control read socket not open')
    else:
        # close unity control read socket
        sockets['read_unity_control'].socket.close()
        sockets['read_unity_control'] = None

    if sockets['read_unity_info'] is None:
        print('unity unity info read socket not open')
    else:
        # close unity info read socket
        sockets['read_unity_info'].socket.close()
        sockets['read_unity_info'] = None

    if sockets['read_motive_sk'] is None:
        print('motive read socket not open')
    else:
        # close motive read socket
        sockets['read_motive_sk'].socket.close()
        sockets['read_motive_sk'] = None

    if sockets['read_imu'] is None:
        print('motive read socket not open')
    else:
        # close motive read socket
        sockets['read_imu'].socket.close()
        sockets['read_imu'] = None

    if sockets['read_imus'] is None:
        print('motive read socket not open')
    else:
        # close motive read socket
        sockets['read_imus'].socket.close()
        sockets['read_imus'] = None

    if sockets['write_unity_sk'] is None:
        print('unity write skeleton socket not open')
    else:
        # close unity write skeleton socket
        sockets['write_unity_sk'].socket.close()
        sockets['write_unity_sk'] = None

    return sockets

#######################


def setup_socket(IP, PORT, ID, timeout = 0.001):
    # Datagram (udp) socket
    try:
        socket = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)
        logging.debug('socket ' + ID + ' created')
    except socket.error as msg:
        logging.error('Failed to create socket. Error : ' +  msg)
        sys.exit()
    # Bind socket to local IP and port
    try:
        socket.bind((IP, PORT))
    except soc.error as msg:
        logging.error('Bind failed. Error Code : ' +  msg)
        sys.exit()
    logging.debug('socket ' + ID + ' bind complete')

    # set timeout
    socket.settimeout(timeout)

    read_s = Socket_struct() # Create an empty socket structure

    read_s.socket = socket
    read_s.ID = ID

    return read_s


#######################


def setup_sockets(sockets = sockets, timeout = 0.001):

    # create unity read flag / write skeleton socket
    sockets['read_unity_flag'] = setup_socket(sockets['unity_flag']['IP'], sockets['unity_flag']['PORT'], 'UNITY_FLAG', timeout = timeout)
    sockets['write_unity_sk'] = sockets['read_unity_flag']

    # create unity control read socket
    sockets['read_unity_control'] = setup_socket(sockets['unity_calib']['IP'], sockets['unity_calib']['PORT'], 'UNITY_CALIB',  timeout = timeout)

    # create unity info read socket
    sockets['read_unity_info'] = setup_socket(sockets['unity_info']['IP'], sockets['unity_info']['PORT'], 'UNITY_INFO',  timeout = timeout)

    # create motive read socket
    sockets['read_motive_sk'] = setup_socket(sockets['motive']['IP'], sockets['motive']['PORT'], 'MOTIVE_SK',  timeout = timeout)

    # create imu read socket
    sockets['read_imu'] = setup_socket(sockets['imu']['IP'], sockets['imu']['PORT'], 'imu',  timeout = timeout)

    # create imus read socket
    sockets['read_imus'] = setup_socket(sockets['imus']['IP'], sockets['imus']['PORT'], 'imus',  timeout = timeout)

    return sockets


#########################


def udp_read(socket_struct, keep_last = False):

    t = time.time()

    """ new implementation (reading only last package) """

    data = udp_read_last(socket_struct, keep_last)

    logging.debug('read in ' +  str(time.time() - t))

    return data


#########################


def udp_read_last(socket_struct, keep_last = False):

    # print('\nREADING FROM', socket_struct.type, '\n')
    # receive data from client (data, addr)

    my_socket = socket_struct.socket

    data = socket_struct.previous_state if keep_last else 't'

    data_ready = False
    data_ready = select.select([my_socket],[],[],0)[0]

    lost_p = 0

    while data_ready:
        data, addr = my_socket.recvfrom(1024)   # buffer size is 1024 bytes

        data_ready = False
        data_ready = select.select([my_socket],[],[],0)[0]

        if data_ready:
            lost_p = lost_p + 1

    if lost_p:
        logging.debug('lost ' +  str(lost_p) + ' frame(s) here! (reading only last), ID = ' +  socket_struct.ID)

    socket_struct.previous_state = data

    return data


#########################


def udp_write(sockets, msg):

    sockets['write_unity_sk'].socket.sendto(msg, (sockets['unity_write_sk_client']['IP'], sockets['unity_write_sk_client']['PORT']))

    HW_IP = "192.168.1.167"
    HW_PORT = 5000

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(msg, (HW_IP, HW_PORT))

    print('udp sent ' + str(msg) + ' to ' + sockets['unity_write_sk_client']['IP'] + ', ' + str(sockets['unity_write_sk_client']['PORT']))


#########################


def udp_process(data, socket_struct):
    raise Exception('moved to HRI_communication.py!')
