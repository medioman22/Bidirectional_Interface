import json
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import scipy
from scipy.interpolate import make_interp_spline, BSpline

# Folder where logs are saved
save_path = 'C:\\Users\\m-wue\\Desktop\\MA 3\\Project\\DroneSwarmFramework\\DroneSwarmFramework\\ClutchSimulationLogs'


def import_data(subject_name, motion_tracking):
    # go to subject folder
    if motion_tracking == 'y':
        subject_name += '_MotionCapture'
    else:
        subject_name += '_Controller'
    path = save_path + '\\' + subject_name
    os.chdir(path)

    # selects all runs to analyze
    runs = []
    for file_name in os.listdir(path):
        print(file_name)
        f = open(file_name)
        runs.append(json.load(f))

    return runs


def plot_data(data):
    for run in data:
        x_hist = []
        z_hist = []
        x_hist_slave = []
        z_hist_slave = []
        target_x = []
        target_z = []
        spread = []
        time = []

        for elm in run['allLogs']:

            # Master drone target
            target = elm.get("controlPosition")
            x = target['x']
            z = target['z']
            # Truncate while not moving
            if [x, z] == [0.0, 0.0]:
                continue
            target_x.append(x)
            target_z.append(z)

            # Master drone position
            pos = elm.get("dronePosition")
            x_hist.append(pos['x'])
            z_hist.append(pos['z'])

            # Slave drone position
            pos = elm.get("slaveDronePosition")
            x_hist_slave.append(pos['x'])
            z_hist_slave.append(pos['z'])

            spread.append(elm.get("spread"))

            time.append(elm.get("absoluteTime"))

        # Slice data set, 2300, 5100 (useless) 6800, 8100
        start_elm = 6800
        end_elm = 8100
        target_x = target_x[start_elm:end_elm]
        target_z = target_z[start_elm:end_elm]
        x_hist = x_hist[start_elm:end_elm]
        z_hist = z_hist[start_elm:end_elm]
        x_hist_slave = x_hist_slave[start_elm:end_elm]
        z_hist_slave = z_hist_slave[start_elm:end_elm]
        spread = spread[start_elm:end_elm]
        time = time[start_elm:end_elm]

        # plot target and drone positions
        fig1, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)

        ax1.scatter(z_hist, x_hist, s=15, c=time, vmin=time[0], vmax=time[-1])
        ax1.set_title('Drone Position', size=15)
        ax1.set_xlabel('z')
        ax1.set_ylabel('x')
        ax1.set_aspect(1)

        im = ax2.scatter(target_z, target_x, s=15, c=time, vmin=time[0], vmax=time[-1])
        ax2.set_title('Target Postition', size=15)
        ax2.set_xlabel('z')
        ax2.set_ylabel('x')
        ax2.set_aspect(1)

        # Axis as topdown view in Unity: x: -z, y: x
        ax1.invert_xaxis()

        # plt.subplots_adjust(wspace=0, hspace=0.5)
        fig1.subplots_adjust(right=0.8)
        cbar_ax = fig1.add_axes([0.85, 0.15, 0.04, 0.7])
        fig1.colorbar(im, cax=cbar_ax, label='Time')

        # plot master and slave positions
        fig2, (ax3, ax4) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)

        ax3.scatter(z_hist, x_hist, s=15, c=time, vmin=time[0], vmax=time[-1])
        ax3.set_title('Master Position', size=15)
        ax3.set_xlabel('z')
        ax3.set_ylabel('x')
        ax3.set_aspect(1)

        im = ax4.scatter(z_hist_slave, x_hist_slave, s=15, c=time, vmin=time[0], vmax=time[-1])
        ax4.set_title('Slave Postition', size=15)
        ax4.set_xlabel('z')
        ax4.set_ylabel('x')
        ax4.set_aspect(1)

        # Axis as topdown view in Unity: x: -z, y: x
        ax3.invert_xaxis()

        # plt.subplots_adjust(wspace=0, hspace=0.5)
        fig2.subplots_adjust(right=0.8)
        cbar_ax = fig2.add_axes([0.85, 0.15, 0.04, 0.7])
        fig2.colorbar(im, cax=cbar_ax, label='Time')

        # Plot spread
        plt.figure()
        plt.scatter(time, spread)
        plt.title('Spread')
        plt.xlabel('Time')
        plt.ylabel('Spread')

        # Moving average
        n = 50
        spread = moving_avg(spread, n)
        time = moving_avg(time, n)
        plt.scatter(time, spread, s=1, c='red')

    plt.show()


# define moving average function
def moving_avg(x, n):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[n:] - cumsum[:-n]) / float(n)


def main():
    # specify data to plot
    # subject_name = input("Subject Name: ")
    # motion_tracking = input("Did you use the motion tracking system? (y/n)")

    data = import_data('Run11', 'y')
    # for run in data:
    plot_data(data)


main()
