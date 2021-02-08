import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import select
import socket
import struct
import time
import numpy as np

# previous_data = None

# subject = 'X' #enter subject id
# t0 = time.time()
# filename = "Range_{}_{}.txt".format(subject,t0)
# file = open(filename,"w") #create file in same loc as script
#                           #time included in title so we store every version
# header = ['Roll','Pitch','Yaw','Roll velocity','Pitch velocity','Yaw velocity','Norm velocity','time']
# for h in header:                #fill header csv style
#     if h==header[-1]:
#         file.write(h+'\n')
#     else:
#         file.write(h+',')
# file.close()



def read_last(my_socket):

    data = 't'

    data_ready = False
    data_ready = select.select([my_socket],[],[],0)[0]

    while data_ready:
        
        data, addr = my_socket.recvfrom(1024) # buffer size is 1024 bytes

        data_ready = False
        data_ready = select.select([my_socket],[],[],0)[0]

    return data


UDP_IP = "127.0.0.1"
UDP_PORT = 29000

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


# roll = []
# pitch = []
# yaw = []
# roll_vel = []
# pitch_vel = []
# yaw_vel = []
# norm_vel = []
# ts = 0
# dt = 0

data_lenght = 104   # 2 long long for timestamp (*bug, should be one)
                    # 8 char for ID
                    # 3 garbage (*bug, coming from ID)
                    # 3 floats for Euler
                    # 4 floats for Quaternion

str_base = 'qqccccccccdddddddddd'
str_l = len(str_base)

print('Acquisition started')
while True:
    t = time.time()
    t1 = time.clock()
    
    data = read_last(sock)

    if data != 't':

        how_many = int(len(data)/data_lenght)

        strs = str_base*how_many


        data_unp = struct.unpack(strs, data)

        imus = []


        for i in range(how_many):
            imus.append({})

            idx = str_l*i

            imus[-1]['ts'] = data_unp[idx+0]
            imus[-1]['ID'] = data_unp[idx+2].decode("utf-8") + data_unp[idx+3].decode("utf-8") + data_unp[idx+4].decode("utf-8") + data_unp[idx+5].decode("utf-8") + data_unp[idx+6].decode("utf-8") +  data_unp[idx+7].decode("utf-8") + data_unp[idx+8].decode("utf-8") + data_unp[idx+9].decode("utf-8")
            imus[-1]['Euler'] = data_unp[idx+13:idx+16]
            imus[-1]['Quat'] = data_unp[idx+16:idx+20]

            print('IMU {} : Euler = [{:.1f} {:.1f} {:.1f}], Quaternions = [{:.1f} {:.1f} {:.1f} {:.1f}]'.format(i+1, imus[-1]['Euler'][0], imus[-1]['Euler'][1], imus[-1]['Euler'][2], imus[-1]['Quat'][0], imus[-1]['Quat'][1], imus[-1]['Quat'][2], imus[-1]['Quat'][3]))
        
        print("")

        a = 1
    
    time.sleep(0.01)
        
    




