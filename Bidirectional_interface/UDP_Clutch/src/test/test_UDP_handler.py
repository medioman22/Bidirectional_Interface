#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 13:02:00 2019

@author: lis
"""

import context

import communication.UDP_handler as udp

import struct


sockets = udp.sockets

sockets = udp.close_sockets(sockets)

sockets = udp.setup_sockets(sockets)

ret = udp.udp_read(sockets['read_unity_query'])

values = [1, 2, 3]

msg = struct.pack('%sf' % len(values), *values)

udp.udp_write(sockets, msg)

sockets = udp.close_sockets(sockets)