
import numpy as np
import select
import socket
import struct

import time

def get_data(my_socket):
    
    data = []
    
    data_ready = False
    data_ready = select.select([my_socket],[],[],0)[0]
    
    while data_ready:
        t, addr = my_socket.recvfrom(1024) # buffer size is 1024 bytes
        
        data.append(t)
            
        data_ready = False
        data_ready = select.select([my_socket],[],[],0)[0]
        
    return data  
        

RB_PER_SKELETON = 21
MANY = 1000000      # this is about 46 minutes of acquisition with 3 markers
                    # (increase for longer acquisition time)

UDP_IP = socket.gethostname()
UDP_PORT_SKELETONS = 9000
UDP_PORT_RIGID_BODIES = 5001 # receiving port
UDP_PORT_MARKERS = 9002

skeletons_socket = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
skeletons_socket.bind((UDP_IP, UDP_PORT_SKELETONS))

rigid_bodies_socket = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
rigid_bodies_socket.bind((UDP_IP, UDP_PORT_RIGID_BODIES))

markers_socket = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
markers_socket.bind((UDP_IP, UDP_PORT_MARKERS))

"""SETTINGS"""

RECEINVING_FROM_DIFFERENT_MACHINE = True
STREAM_TO_DIFFERENT_MACHINE = False

READ_MARKERS = False
READ_RIGID_BODIES = True
READ_SKELETONS = False
    
if not RECEINVING_FROM_DIFFERENT_MACHINE:
    
    CLIENT_IP = "192.168.1.235" # here your client's IP (run ifconfig to verify)
    SERVER_PORT = 5000
    CLIENT_PORT = 5001 # here the port you want to communicate to
    
    str_marker = 'ifff' # one int, three floats
    
    def send_data(my_socket, data, data_type):
            
        if data_type == 'marker':
            print("sent a marker")
        
            message = struct.pack('%sf' % len(data), *data)
            
            print(message)
            my_socket.sendto(message, (CLIENT_IP, CLIENT_PORT))
        elif data_type == 'rb':
            print("sent a rigid body")
        
            message = struct.pack('%sf' % len(data), *data)
            
            my_socket.sendto(message, (CLIENT_IP, CLIENT_PORT))
        elif data_type == 'sk':
            print("sent a skeleton")
        
            message = struct.pack('%sf' % len(data), *data)
            
            my_socket.sendto(message, (CLIENT_IP, CLIENT_PORT))
    
    send_socket = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    send_socket.bind(('', SERVER_PORT))

markers_list = [None] * MANY
rigid_bodies_list = [None] * MANY
skeletons_list = [None] * MANY

count_markers = 0
count_rigid_bodies = 0
count_skeletons = 0

while True:
    
    if READ_MARKERS:
        markers = get_data(markers_socket)
        if len(markers):
            
            print("acquired marker data, total number = ", len(markers))
            
            for i in markers:
                strs = 'ifff'
                data_ump = struct.unpack(strs, i)
                data_ump_l = list(data_ump)
                markers_list[count_markers] = data_ump_l
                count_markers = count_markers + 1
        #            print(data_ump_l)
                if not RECEINVING_FROM_DIFFERENT_MACHINE and STREAM_TO_DIFFERENT_MACHINE:
                    send_data(send_socket, data_ump, 'marker')
                
        
    if READ_RIGID_BODIES:
        rigid_bodies = get_data(rigid_bodies_socket)
        if len(rigid_bodies):
            print("acquired rigid bodies, total number = ", len(rigid_bodies))
            
            for i in rigid_bodies:
                strs = 'ifffffff'
                data_ump = struct.unpack(strs, i)
                data_ump_l = list(data_ump)
                rigid_bodies_list[count_rigid_bodies] = data_ump_l
                count_rigid_bodies = count_rigid_bodies + 1
    #            print(data_ump_l)
                if not RECEINVING_FROM_DIFFERENT_MACHINE and STREAM_TO_DIFFERENT_MACHINE:
                    send_data(send_socket, data_ump, 'rb')
        
        
    if READ_SKELETONS:
        skeletons = get_data(skeletons_socket)
        if len(skeletons):
            print("acquired skeletons, total number = ", len(skeletons))
            
            for i in skeletons:
                    
                strs = 'ifffffff'*RB_PER_SKELETON
                data_ump = struct.unpack(strs, i)
                data_ump_l = list(data_ump)
                skeletons_list[count_skeletons] = data_ump_l
                count_skeletons = count_skeletons + 1
    #            print(data_ump_l)
                if not RECEINVING_FROM_DIFFERENT_MACHINE and STREAM_TO_DIFFERENT_MACHINE:
                    send_data(send_socket, data_ump, 'sk')
            
    time.sleep(1e-3)
