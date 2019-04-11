<p align="center">
  <img src=https://github.com/AntoineWeber/Bidirectional_Interface/blob/master/readme_images/epfl_logo.png>
</p>

# Bidirectional Interface I & II
Repository containing the work performed for the semester project entitle "Bidirectional wearable interface for mobile robot teleoperation" performed at the LIS (EPFL).


## Structure
This project contains different subparts. First a common part being to control a drone with one hand by variating its position in space which will be decoded into a drone position.

Then the workflow splitted into two main parts : The first beeing to implement the control of two different drones at the same time using two hands and the second part being to add haptics feedback to the users hand to detect whether the drone is close to an object or not to avoid collisions.

## TODO

Items that are not critical but should be handled eventually:
* Implement control angle in PositionControl script
* ~~Implement more general data logger based on Interface~~ Don't do
* Use collision layers in CollisionChecker script (useful to ignore some collision, e.g. floor, other drones, ... )
* Rename variables in PositionControl script (e.g. desired_yaw --> desiredYawRate as it is an angular speed and not and angle)
