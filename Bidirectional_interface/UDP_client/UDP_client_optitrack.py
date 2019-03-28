
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
LOCAL_IP = "127.0.0.1"
UDP_PORT_RIGID_BODIES = 5001 # receiving port

rigid_bodies_socket = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
rigid_bodies_socket.bind((UDP_IP, UDP_PORT_RIGID_BODIES))


"""SETTINGS"""
READ_RIGID_BODIES = True
unity_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
unity_port = 26000


rigid_bodies_list = [None] * MANY

count_rigid_bodies = 0

while True:     
    if READ_RIGID_BODIES:
        rigid_bodies = get_data(rigid_bodies_socket)
        if len(rigid_bodies):
            print("acquired rigid bodies, total number = ", len(rigid_bodies))
            
            for i in rigid_bodies:
                #strs = 'ifffffff'
                #data_ump = struct.unpack(strs, i)
                #data_ump_l = list(data_ump)
                #rigid_bodies_list[count_rigid_bodies] = data_ump_l
                #count_rigid_bodies = count_rigid_bodies + 1
                #print(data_ump_l)
                unity_socket.sendto(i, (LOCAL_IP, unity_port))

        
            
    time.sleep(1e-3)
