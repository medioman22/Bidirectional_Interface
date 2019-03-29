
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

UDP_IP = "127.0.0.1"
UDP_PORT_RIGID_BODIES = 9001

rigid_bodies_socket = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
rigid_bodies_socket.bind((UDP_IP, UDP_PORT_RIGID_BODIES))

"""SETTINGS"""

RECEINVING_FROM_DIFFERENT_MACHINE = False
STREAM_TO_DIFFERENT_MACHINE = True

READ_MARKERS = False
READ_RIGID_BODIES = True
READ_SKELETONS = False
    
if not RECEINVING_FROM_DIFFERENT_MACHINE:
    
    #CLIENT_IP = "128.179.140.168" # here your client's IP (run ifconfig to verify)
    CLIENT_IP_LIST = ["128.179.140.168", "128.179.195.151"] # Used to stream to multiple clients
    SERVER_PORT = 5425
    CLIENT_PORT = 5001 # here the port you want to communicate to
    
    str_marker = 'ifff' # one int, three floats
    
    def send_data(my_socket, data, data_type):
        if data_type == 'rb':
            #print("sent a rigid body")
        
            message = struct.pack('%sf' % len(data), *data)
            
            #my_socket.sendto(message, (CLIENT_IP, CLIENT_PORT))
            for client_ip in CLIENT_IP_LIST:
                my_socket.sendto(message, (client_ip, CLIENT_PORT))
    
    send_socket = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    # No binding because we send with this socket (server)

rigid_bodies_list = [None] * MANY

count_rigid_bodies = 0

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
                #print(data_ump_l)
                if not RECEINVING_FROM_DIFFERENT_MACHINE and STREAM_TO_DIFFERENT_MACHINE:
                    send_data(send_socket, data_ump, 'rb')
#        else:
#            if not RECEINVING_FROM_DIFFERENT_MACHINE and STREAM_TO_DIFFERENT_MACHINE:
#                print("Sending dummy data.")
#                strs = 'ifffffff'
#                message = struct.pack(strs, 1, 0.1, 0.1, 0.1, 1, 2, 3, 4)
#                data_ump = struct.unpack(strs, message)
#                send_data(send_socket, data_ump, 'rb')
        

            
    time.sleep(1e-3)
