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

Hence, this branch contains a different arena tested exclusively to validate the haptic device. Moreover, it also contains different python scripts that were used to communicate the different distances of the drone to the walls to a BBG card which was connected to the motor drives used for the tactile feedback.

## twoDrones branch
**Thomas Havy**  
This branch contains preliminary work for controlling two drones with two hands.  
The existing code was adapted to track two hands with the motion capture system and control two drones.  
A cooperative task where the two hands are used together to control 2 drones carrying a beam has been implemented.
