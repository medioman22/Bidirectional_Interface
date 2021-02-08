import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import select
import socket
import struct
import time
import numpy as np

previous_data = None

subject = 'subject_hand_19' #enter subject id
t0 = time.time()
filename = "Range_{}_{}.txt".format(subject,t0)
file = open(filename,"w") #create file in same loc as script
                          #time included in title so we store every version
header = ['Roll','Pitch','Yaw','Roll velocity','Pitch velocity','Yaw velocity','Norm velocity','time']
for h in header:                #fill header csv style
    if h==header[-1]:
        file.write(h+'\n')
    else:
        file.write(h+',')
file.close()



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


roll = []
pitch = []
yaw = []
roll_vel = []
pitch_vel = []
yaw_vel = []
norm_vel = []
ts = 0
dt = 0
print('Acquisition started')
while True:
    t = time.time()
    t1 = time.clock()
    
    data = read_last(sock)

    if data != 't':
        #print(data)

        how_many = int(len(data)/64)

        strs = "dddd"#*how_many

        data_ump = struct.unpack(strs, data)
        # data_ump = [timestamp, roll, pitch, yaw]
        roll = data_ump[1]
        pitch = data_ump[2]
        yaw = data_ump[3]
        te = time.time()
        if ts!=0:
            dt = abs(ts - te)
        ts = te
        
        if previous_data is not None and dt!=0:
            vr = (data_ump[1]-previous_data[1])/dt #dynamics acquisition deg/sec
            vp = (data_ump[2]-previous_data[2])/dt
            vy = (data_ump[3]-previous_data[3])/dt
            vn = np.sqrt(vr**2+vp**2+vy**2)
            #velocity for all 3 angles + for the norm of all 3: sqrt(v1**2+v2**2+v3**2)
            #write data in file
            file = open(filename,"a") #append mode
            file.write(str(roll)+','+str(pitch)+','+str(yaw)+','+str(vr)+','+str(vp)+','\
                       +str(vy)+','+str(vn)+','+str(ts)+'\n')
        
        previous_data = data_ump
        file.close()
    
    time.sleep(0.01)
        
    




