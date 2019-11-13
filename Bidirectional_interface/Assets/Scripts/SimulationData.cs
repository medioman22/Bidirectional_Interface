﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// This class contains constant values of the simulation parameters.
/// It contains information about the drone, the room, the mocap system, etc.
/// These constants can be accessed from any script as follows: SimulationData.VariableName
/// </summary>
public static class SimulationData
{
    public const float DroneSize = 0.09f; // [m], roughly square 9x9cm
    public const float DroneWeight = 0.027f; // [kg]

    public const float MocapUpdateDeltaTime = 0.008f; // [s], a new data point every 8ms
    public const int nbParametersMocap = 8; // index, pos (3), quaternion (4)

    public static readonly Vector3 RoomDimensions = new Vector3(8, 6, 8); // [m^3]

    public const int nbDistanceSensors = 6;

    public const float startUpControlDelay = 1.5f; // s

    // This variable is incremented every time the simulation path is reloaded
    public static int runNumber = 0; 

    // This variable is used to store the name of the current subject
    public static string subjectName = "";

    // This variable is used to store if the drone is controlled via controller or mocap
    public static bool useController = false;

    public static float takeoffHeight = 0.5f;


    //Value to be send to the user for feedback
    public static float heightError = 0.0f;
    public static Vector3 distanceToWaypoint = new Vector3(0.0f, 0.0f, 0.0f);
    public static float extensionError = 0.0f;
    public static float contractionError = 0.0f;
}

