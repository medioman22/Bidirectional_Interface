import json
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

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
        target_x = []
        target_z = []
        spread = []
        time = []

        for elm in run['allLogs']:
            target = elm.get("controlPosition")
            x = target['x']
            z = target['z']
            # Truncate while not moving
            if [x, z] == [0.0, 0.0]:
                continue
            target_x.append(x)
            target_z.append(z)

            pos = elm.get("dronePosition")
            x_hist.append(pos['x'])
            z_hist.append(pos['z'])

            spread.append(elm.get("spread"))

            time.append(elm.get("absoluteTime"))
            # spread.append(elm.get("spread"))

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

        # Plot spread
        plt.figure()
        plt.scatter(time, spread)
        plt.title('Spread')
        plt.xlabel('Time')
        plt.ylabel('Spread')

    plt.show()


def main():
    # specify data to plot
    # subject_name = input("Subject Name: ")
    # motion_tracking = input("Did you use the motion tracking system? (y/n)")

    data = import_data('plot', 'n')
    # for run in data:
    plot_data(data)


main()
