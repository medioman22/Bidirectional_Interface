import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import time

import context
import HRI_communication as comm
import dataset_handling.user_data as user_data
from settings.settings import get_settings

settings = get_settings()

# Create figure for plotting
fig = plt.figure()
ax1 = fig.add_subplot(2, 2, 1)
ax11 = fig.add_subplot(2, 2, 3)

ax2 = fig.add_subplot(2, 2, 2)
ax21 = fig.add_subplot(2, 2, 4)

ts = []
xs = []
ys = []
zs = []
ws = []

rolls = []
pitchs = []
yaws = []

xs1 = []
ys1 = []
zs1 = []
ws1 = []

rolls1 = []
pitchs1 = []
yaws1 = []

count = 0

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    global count

    # Read IMUs
    data = comm._read_imus()
    data_proc = comm._process_imus(data)

    if not comm._timeout(data_proc):

        input_data = user_data.imus(np.resize(data_proc, [len(settings['used_body_parts']), settings['n_elements_per_imu']]))
        data_processed = comm._imus_preprocessing(input_data).values

        # Add x and y to lists
        count += 1
        ts.append(count)
        xs.append(data_processed[0][4])
        ys.append(data_processed[0][5])
        zs.append(data_processed[0][6])
        ws.append(data_processed[0][7])
        rolls.append(data_processed[0][8]/np.pi*180)
        pitchs.append(data_processed[0][9]/np.pi*180)
        yaws.append(data_processed[0][10]/np.pi*180)

        xs1.append(data_processed[1][4])
        ys1.append(data_processed[1][5])
        zs1.append(data_processed[1][6])
        ws1.append(data_processed[1][7])
        rolls1.append(data_processed[1][8]/np.pi*180)
        pitchs1.append(data_processed[1][9]/np.pi*180)
        yaws1.append(data_processed[1][10]/np.pi*180)


        ts_plot = ts[-30:] 
        xs_plot = xs[-30:] 
        ys_plot = ys[-30:] 
        zs_plot = zs[-30:] 
        ws_plot = ws[-30:] 
        rolls_plot = rolls[-30:] 
        pitchs_plot = pitchs[-30:] 
        yaws_plot = yaws[-30:] 

        xs1_plot = xs1[-30:] 
        ys1_plot = ys1[-30:] 
        zs1_plot = zs1[-30:] 
        ws1_plot = ws1[-30:] 
        rolls1_plot = rolls1[-30:] 
        pitchs1_plot = pitchs1[-30:] 
        yaws1_plot = yaws1[-30:] 

        ####

        # Draw x and y lists
        ax1.clear()
        ax1.plot(ts_plot, xs_plot, label = 'q_x')
        ax1.plot(ts_plot, ys_plot, label = 'q_y')
        ax1.plot(ts_plot, zs_plot, label = 'q_z')
        ax1.plot(ts_plot, ws_plot, label = 'q_w')

        # Format plot
        ax1.grid()
        ax1.legend(loc = 'upper left')
        ax1.set_ylim([-1,1])
        # ax.set_xticks()
        ax1.set_title('Quaternions')
        ax1.set_ylabel('Quaternion value')

        ####
        
        # Draw x and y lists
        ax11.clear()
        ax11.plot(ts_plot, rolls_plot, label = 'roll_x')
        ax11.plot(ts_plot, pitchs_plot, label = 'pitch_y')
        ax11.plot(ts_plot, yaws_plot, label = 'yaw_z')

        # Format plot
        ax11.grid()
        ax11.legend(loc = 'upper left')
        ax11.set_ylim([-180,180])
        # ax.set_xticks()
        ax11.set_title('Euler Angles')
        ax11.set_ylabel('Euler Angles value')

        ####

        # Draw x and y lists
        ax2.clear()
        ax2.plot(ts_plot, xs1_plot, label = 'q_x')
        ax2.plot(ts_plot, ys1_plot, label = 'q_y')
        ax2.plot(ts_plot, zs1_plot, label = 'q_z')
        ax2.plot(ts_plot, ws1_plot, label = 'q_w')

        # Format plot
        ax2.grid()
        ax2.legend(loc = 'upper left')
        ax2.set_ylim([-1,1])
        # ax.set_xticks()
        ax2.set_title('Quaternions')
        ax2.set_ylabel('Quaternion value')

        ####
        
        # Draw x and y lists
        ax21.clear()
        ax21.plot(ts_plot, rolls1_plot, label = 'roll_x')
        ax21.plot(ts_plot, pitchs1_plot, label = 'pitch_y')
        ax21.plot(ts_plot, yaws1_plot, label = 'yaw_z')

        # Format plot
        ax21.grid()
        ax21.legend(loc = 'upper left')
        ax21.set_ylim([-180,180])
        # 2x.set_xticks()
        ax11.set_title('Euler Angles')
        ax21.set_ylabel('Euler Angles value')

        # plt.close()

# setup sockets
comm.setup_sockets()


# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=100)

plt.show()
