<p align="center">
  <img src=https://github.com/AntoineWeber/Bidirectional_Interface/blob/master/readme_images/epfl_logo.png>
</p>

# Bidirectional Interface I & II
Repository containing the work performed for the semester project entitle "Bidirectional wearable interface for mobile robot teleoperation" performed at the LIS (EPFL).

## Authors 

* **Antoine Weber**
* **Thomas Havy**

## Structure
The master branch contains the common work of both the authors. Indeed, the first part of this project was to implement a hand control interface to control a drone in position.
The pose of the hand was captured using an OptiTrack system, and was then sent to the Unity game engine that embedded a drone simulator.
The master branch also includes different arenas in Unity that were tested during thist first common part.

## Haptics branch
**Antoine Weber**  
This branch contains the work performed to add haptic feedback to the developed hand interface.
Haptic feedback were added to the interface to try to improve and accelerate the learning procedure of the interface. For the sake of this project, the feedback was implemented on a glove and was representing the distance to obstacles in all 6 3D directions.

## Use the BBG
Hence, this branch contains a different arena tested exclusively to validate the haptic device. Moreover, it also contains different python scripts that were used to communicate the different distances of the drone to the walls to a BBG card which was connected to the motor drives used for the tactile feedback.

### Setup the connection
1) Connect the BBG to a power supply & let it start
2) After a while, you will see a new WiFi appear being the board. Connect to it
3) Once connected, you can ssh to it. The IP is fixed :
```
ssh debian@192.168.7.2
```
Then type the password which will actually appear on your screen.
## twoDrones branch
**Thomas Havy**  
This branch contains preliminary work for controlling two drones with two hands.  
The existing code was adapted to track two hands with the motion capture system and control two drones.  
A cooperative task where the two hands are used together to control 2 drones carrying a beam has been implemented.

### Make the motors vibrate
1) Navigate in your SSH terminal to the Firmware folder of the wearable directory and launch the main (should require super-user rights) :
```
cd Wearable-Software/Firmware/src/
sudo python Main.py
```
3) Now there are 2 ways to make the motor vibrate : You should know that serveral libraries are required to make these scripts work. There is a .yml file in the Interface folder which can be used to directly create an environment with the right libraries.

##### In both cases, you need to define a python environment with all the required libraries. There is a [.yml file](Bidirectional_interface/Haptics/Interface/) that you can use to actually create the right environment if you're under MacOS. If under windows, there is also a text file containing the requirements to create the right environment.

#### Possibility 1 : Use the UI
1) In your local clone of the repo, go to the Interface folder and launch the main.py present in the src folder 
```
cd Bidirectional_interface/Haptics/Interface/src/
python main.py
```
It should make a UI pop up. Select the device in the list and change the PWM values to make the motor vibrate.

#### Possibility 2 : Use the python API
1) You can use the `main.py` script in the API_Calls folder as an example. This script will read the data sent by Unity and send the vibration queries to the BBG card.

