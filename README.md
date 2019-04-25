<p align="center">
  <img src=https://github.com/AntoineWeber/Bidirectional_Interface/blob/master/readme_images/epfl_logo.png>
</p>

# Bidirectional Interface I & II
Repository containing the work performed for the semester project entitle "Bidirectional wearable interface for mobile robot teleoperation" performed at the LIS (EPFL).


## Structure
This project contains different subparts. First a common part being to control a drone with one hand by variating its position in space which will be decoded into a drone position.

Then the workflow splitted into two main parts : The first beeing to implement the control of two different drones at the same time using two hands and the second part being to add haptics feedback to the users hand to detect whether the drone is close to an object or not to avoid collisions.

## Use the BBG

### Setup the connection
1) Connect the BBG to a power supply & let it start
2) After a while, you will see a new WiFi appear being the board. Connect to it
3) Once connected, you can ssh to it. The IP is fixed :
```
ssh debian@192.168.7.2
```
Then type the password which will actually appear on your screen.

### Make the motors vibrate
1) Navigate in your SSH terminal to the Firmware folder of the wearable directory and launch the main (should require super-user rights) :
```
cd Wearable-Software/Firmware/src/
sudo python Main.py
```
3) Now there are 2 ways to make the motor vibrate : You should know that serveral libraries are required to make these scripts work. There is a .yml file in the Interface folder which can be used to directly create an environment with the right libraries.

### In both cases, you need to define a python environment with all the required libraries. There is a [.yml file](Bidirectional_interface/Haptics/Interface/) that you can use to actually create the right environment.

#### Possibility 1 : Use the UI
1) In your local clone of the repo, go to the Interface folder and launch the main.py present in the src folder 
```
cd Bidirectional_interface/Haptics/Interface/src/
python main.py
```
It should make a UI pop up. Select the device in the list and change the PWM values to make the motor vibrate.

#### Possibility 2 : Use the python API
1) You can use the `test.py` script in the API_Calls folder as an example. Navigate to the last line and modify as you wish the "dim" variable being the identifier for the motors, and the "value" being the actual PWM value.

