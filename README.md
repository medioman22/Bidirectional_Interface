<p align="center">
  <img src=https://github.com/medioman22/Bidirectional_Interface/tree/Matthias/ReadMe>
</p>

# Bidirectional Interface for Drone Swarm
Repository containing the work performed for the semester project titled "Framework development to control drone
swarms using wearable interfaces" performed at the LIS (EPFL) in autumn 2020.

## Author

**Matthias Wüst**

## Framework Setup
Read the report "SemesterProject_MatthiasWüst.pdf" under ./ReadMe for more information about general functionalities and communication pipelines.

### Leap
Install the latest Leap Motion Controller Software: https://developer.leapmotion.com/sdk-leap-motion-controller/ (tested with Orion 4.1.0+52211)
Create a Python virtual environment (using Python 2 and Anaconda) from yml file in ./PythonEnvironments: conda env create -n <name> -f conda_leap.yml
Run the file ./Leap/Leap_send_data.py to acquire data from the sensor
Default UDP port is 5005. Make sure the terminal is selected during aquisition and that the power cable is plugged in if using a laptop.

### Xsens
Install the latest Qt Community and under build-settings select the ./Xsens/[...]Qt_5_15_1_MSVC2019[...] folder as a build directory.
Open ./Xsens/IMU_read/awindamonitor.pro as a project.
Get the sensor drivers from https://www.xsens.com/software-downloads (MTw Awinda) and install them.
When IMUs are turned on (blinking red) and connected run the project in Qt. A GUI should open displaying the real-time orientation values.

### Xsens communication
Go to ./DroneSwarmFramework/UDP_Clutch/src/settings and in "settings.py" change line 139 (settings['data_folder']) to local user path.
Also have a look at "settings.ini", which defines all communication ports, the type of experiment, input values, etc. (Leap is seperate).
To communicate the Xsens values to the simulation go to ./DroneSwarmFramework/UDP_Clutch/src/test and run "acquire_init_pose.py" for initial calibration (and whenever needed again).
Then, under ./DroneSwarmFramework/UDP_Clutch run "clutch_stream_IMU.py". The values should be displayed as two vectors for the two sensors.

### Unity
Download version 2019.2.5f1 and open the project folder ./DroneSwarmFramework.
In the folder Assets/Scenes load "Swarm" scene.
Under SimulationManager you can activate logging and easily change the maze enviroment.

### Clutches
The Arduino control board with 16 clutch states was programmed and tested with "clutch_control.ino" in the folder ./ArduinoClutchControl. The file "clutch_control_shortened.py" is the basis for a different control board.
Under ./DroneSwarmFramework/Haptics/API_Calls run "UDP_client_clutch.py" during the simulation. The minimal distances in all directions (4 values) should be printed.

### Other
The ./Evaluation folder contains a script to plot the log files stored in ./DroneSwarmFramework/ClutchSimulationLogs.
