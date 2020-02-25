
<p align="center">
  <img src=https://github.com/AntoineWeber/Bidirectional_Interface/blob/master/readme_images/epfl_logo.png>
</p>

# Haptic swarm information transmission in Simulation
Repository containing the work performed for the Master project entitled "Evaluation of swarm information transmission with haptic and visual feedback systems" performed at the LIS (EPFL).

## Author

* **Hugo Kohli**

## Structure
The master branch contains the current state of this work. All the previous commits can be found in the branch `origin/flocking-creation`
The pose of the hand was captured using an OptiTrack system, and was then sent to the Unity game engine that embedded a drone simulator.

## Unity
The simulation is done in the game development platform Unity.
To select the adequate Unity version, **[Unity Hub](https://docs.unity3d.com/Manual/GettingStartedInstallingHub.html)** can be used.
For this project, we used the version 2019.2.5f1
### Scripts
The scripts used to create the swarm and the experiment environment can be found in the folder `Bidirectional_interface/Assets/Scripts`

In each script, a `Start()` method is executed once when the game is launched, and a `FixedUpdate()` or `Update()` is called in a loop. The [Unity documentation](https://learn.unity.com/) can be of great help at the beginning.

These are the main scripts that are used:
 - `UpdateHandTarget.cs`, to control of the swarm and the experiment statE
 - `SocketSender.cs`, to send information to the haptic control python script
 - `SubjectNameUI.cs`, to handle the UI at the beginning of the experiment
 - `updateUI.cs`, to control the visual feedback system
 - `Log.cs`, to save the desired variables at the end of a flight

The drone physics are based on the simulator created in the following repo :  
[`UAVs-at-Berkeley/UnityDroneSim`](https://github.com/UAVs-at-Berkeley/UnityDroneSim)
The control of the drone is done using the scripts from the Brekeley simulation at the following location:
`/Bidirectional_interface/Assets/Berkeley_simu/Scripts/Velocity_control`
The drones can either be control with velocity control (`VelocityControl.cs`) or with position control (`PositionControl.cs`).

## Haptic feedback systems
Two different haptic interfaces are used and their control is done in a python script: 
`Bidirectional_interface/Haptics/API_calls/main.py`. . 

### Glove
The first one is a glove embedding 6 vibrating motors controlled with a Beagle Bone Green Wireless microcontroller. The communication with the PC is done using WIFI. The instruction on how to connect it can be found in this repo : [`medioman22/Bidirectional_Interface`](https://github.com/medioman22/Bidirectional_Interface)

### Bracelets
The second one is composed of two bracelets embedding 4 vibrating motors each, and controlled with an Arduino Pro Mini with an additional Bluetooth module.

To connect the bracelets, follow these steps:

 - Turn on the bracelets with the red slider
 - Connect the bluetooth device to your PC
 - Check which COM port is used
 - Repeat the operation for the second bracelets
 - Replace the 2 COM port with the correct ones in the file `Bidirectional_interface/Haptics/API_calls/param_bracelets.yaml`:
> COM:
	>> right_arm: 16
	left_arm: 15

To control the motors, bluetooth serial communication is used with the python module [pySerial](https://pypi.org/project/pyserial/). For each bracelets, a list of character has to be sent, with the following style : 
 `'S, intensity_motor_1, intensity_motor_2, intensity_motor_3, intensity_motor_4, E'`
 

 - The first letter is a 'S' as 'Start'. It has to be converted into an integer representing the Unicode character, using the function `ord()` in python
 - The intensity of each of the 4 motors is an int
 - The last letter is an 'E' as 'End'. It has to in Unicode as the first letter

The Arduino code can be found at this location: `Bidirectional_interface/Haptics/Serial_communication/motor_control/motor_control.ino`

