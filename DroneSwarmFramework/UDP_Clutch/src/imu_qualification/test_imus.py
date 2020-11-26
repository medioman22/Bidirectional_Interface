import context
import HRI_communication as comm

from settings.settings import get_settings

import datetime
import time

import numpy as np
import os

settings = get_settings()

comm.setup_sockets()

f = 25 # seconds
acq_min = 0.1 # total minutes

duration = 60*acq_min

imu_data = []

start = time.clock()
last_read = start

stop = False

count = 0

while not stop:

    t = time.clock()
    elapsed = t-last_read

    if elapsed > 1/f:

        data_temp = comm._read_imus()
        if not(comm._timeout(data_temp)):
            imu_data.append(comm._read_imus())
            last_read = t
            count +=1
            print('read input #{}'.format(count))

    total_elapsed = t-start
    if total_elapsed > duration:
        stop = True

# postprocess
head = settings['headers']

# create empty numpy array to store data
n_imus = int(len(imu_data[0])/settings['n_bytes_per_imu'])
n_data = int(n_imus * settings['n_elements_per_imu'])
input_data_num = np.empty([len(imu_data), n_data])      # 1 skel = [n_rigid_bodies_in_skeleton] * [n_elements_in_rigid_body] (see header for details)

for i in range(0, len(imu_data)):

    # process list of binaries into numpy array
    imus_np_t = comm._process_imus(imu_data[i])
    imus_np_t.resize(1, imus_np_t.size)

    input_data_num[i] = imus_np_t

    print('input processed ' + str(i) + ' of ' + str(len(imu_data)))

for i in range(n_imus):
    n = np.char.array([('_' + str(i+1))])
    if i==0:
        imu_header = head['imus_base'] + (n)
    else:
        imu_header = np.r_[imu_header, head['imus_base'] + (n)]


acquired_data = np.vstack([imu_header, input_data_num])

np.savetxt(os.path.join('.', 'data', 'imu_qualif_data' + '_' + datetime.datetime.now().strftime("%Y_%b_%d_%I_%M_%S%p") + '.csv'), (acquired_data), delimiter=",", fmt="%s")