import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

import context
import HRI_communication as comm
import dataset_handling.user_data as user_data
from settings.settings import get_settings

settings = get_settings()

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(2, 2, 2)
ax1 = fig.add_subplot(2, 2, 4)

ax2 = fig.add_subplot(2, 2, 1)
ax21 = fig.add_subplot(2, 2, 3)

ts = []
xs = []
ys = []
zs = []
ws = []

rolls = []
pitchs = []
yaws = []

xraws = []
yraws = []
zraws = []
wraws = []

count = 0

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    global count

    # Read IMUs
    data = comm._read_imus()
    data_proc = comm._process_imus(data)

    if not comm._timeout(data_proc):

        input_data = user_data.imus(np.resize(data_proc, [len(settings['used_body_parts']), settings['n_elements_per_imu']]))
        data_processed = comm._skeleton_preprocessing(input_data).values[0]

        # Add x and y to lists
        count += 1
        ts.append(count)
        xs.append(data_processed[4])
        ys.append(data_processed[5])
        zs.append(data_processed[6])
        ws.append(data_processed[7])
        rolls.append(data_processed[8]/np.pi*180)
        pitchs.append(data_processed[9]/np.pi*180)
        yaws.append(data_processed[10]/np.pi*180)

        xraws.append(data_proc[4])
        yraws.append(data_proc[5])
        zraws.append(data_proc[6])
        wraws.append(data_proc[7])


        ts_plot = ts[-30:] 
        xs_plot = xs[-30:] 
        ys_plot = ys[-30:] 
        zs_plot = zs[-30:] 
        ws_plot = ws[-30:] 
        rolls_plot = rolls[-30:] 
        pitchs_plot = pitchs[-30:] 
        yaws_plot = yaws[-30:] 

        xraws_plot = xraws[-30:] 
        yraws_plot = yraws[-30:] 
        zraws_plot = zraws[-30:] 
        wraws_plot = wraws[-30:] 

        ####

        # Draw x and y lists
        ax.clear()
        ax.plot(ts_plot, xs_plot, label = 'q_x')
        ax.plot(ts_plot, ys_plot, label = 'q_y')
        ax.plot(ts_plot, zs_plot, label = 'q_z')
        ax.plot(ts_plot, ws_plot, label = 'q_w')

        # Format plot
        ax.grid()
        ax.legend(loc = 'upper left')
        ax.set_ylim([-1,1])
        # ax.set_xticks()
        ax.set_title('Quaternions')
        ax.set_ylabel('Quaternion value')

        ####
        
        # Draw x and y lists
        ax1.clear()
        ax1.plot(ts_plot, rolls_plot, label = 'roll_x')
        ax1.plot(ts_plot, pitchs_plot, label = 'pitch_y')
        ax1.plot(ts_plot, yaws_plot, label = 'yaw_z')

        # Format plot
        ax1.grid()
        ax1.legend(loc = 'upper left')
        ax1.set_ylim([-180,180])
        # ax.set_xticks()
        ax1.set_title('Euler Angles')
        ax1.set_ylabel('Euler Angles value')

        ####

        # Draw x and y lists
        ax2.clear()
        ax2.plot(ts_plot, xraws_plot, label = 'q_x')
        ax2.plot(ts_plot, yraws_plot, label = 'q_y')
        ax2.plot(ts_plot, zraws_plot, label = 'q_z')
        ax2.plot(ts_plot, wraws_plot, label = 'q_w')

        # Format plot
        ax2.grid()
        ax2.legend(loc = 'upper left')
        ax2.set_ylim([-1,1])
        # ax.set_xticks()
        ax2.set_title('Quaternions (raw)')
        ax2.set_ylabel('Quaternion value (raw)')


# setup sockets
comm.setup_sockets()


# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=100)
# ani2 = animation.FuncAnimation(fig2, animate, fargs=(xs, ys), interval=100)
plt.show()