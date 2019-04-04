﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class DataLogger : MonoBehaviour
{
    // all the classes to get informations
    public UDPCommandManager mocap;
    public HandAbsolutePositionControl handControl;
    public PositionControl positionCtrl;
    public VelocityControl velocityCtrl;
    public CameraPosition cameraPos;
    //public CollisionChecker collision;
    public Rigidbody drone;

    // -------------------------------------------------------------------

    // string being the subject name
    public string subjectName;

    // enum to handle the type of experiment
    public enum TypeOfExpermiment
    {
        Controller,
        MotionCapture
    }
    public TypeOfExpermiment currentExperiment;
    private string[] typeNames = {"Controller", "MotionCapture"};


    // class containing the data to be logged
    [System.Serializable]
    public struct Logger
    {
        public float absoluteTime;
        public float differentialTime;
        // Input 
        public Vector3 controlPosition;
        public Vector3 controlSpeed;
        public float desiredYawRate;
        public bool resetOrigin;
        public bool clutch;
        public Vector3 mocapPosition;
        public Quaternion mocapQuaternion;
        // Output
        public Vector3 dronePosition;
        public Vector3 droneSpeed;
        public bool collision;
    }
    private Logger currentLog = new Logger();

    [System.Serializable]
    public class LoggerCollection
    {
        public List<Logger> allLogs;

        public LoggerCollection()
        {
            allLogs = new List<Logger>();
        }
    }
    private LoggerCollection cumulatedLogs;

    // -------------------------------------------------------------------

    public string save_path = "c:/Users/aweber/Desktop/Simulation_Logs/";
    private string final_path;

    private void Start()
    {
        if (!Directory.Exists(save_path))
        {
            Directory.CreateDirectory(save_path);
        }

        if (!Directory.Exists(save_path+subjectName))
        {
            Directory.CreateDirectory(save_path + subjectName);
        }

        string typeOfCamera;
        if (cameraPos.FPS)
        {
            typeOfCamera = "FPS";
        }
        else
        {
            typeOfCamera = "TPS";
        }
        final_path = save_path + subjectName + "/" + typeNames[(int)currentExperiment] + "_" + typeOfCamera + ".json";
        if (File.Exists(final_path))
        {
            final_path = MakeUnique(final_path);
        }

        cumulatedLogs = new LoggerCollection();
    }

    // Update is called once per frame
    void LateUpdate()
    {
        // Input
        currentLog.absoluteTime = Time.time;
        currentLog.differentialTime = Time.deltaTime;
        currentLog.controlPosition = positionCtrl.target.position;
        currentLog.controlSpeed = new Vector3(velocityCtrl.desiredVx, 0.0f, velocityCtrl.desiredVz);
        currentLog.desiredYawRate = velocityCtrl.desired_yaw;
        if ((int)currentExperiment == 1)
        {
            currentLog.mocapPosition = mocap.GetPosition();
            currentLog.mocapQuaternion = mocap.GetQuaternion();
        }

        // Output
        currentLog.dronePosition = drone.position;
        currentLog.droneSpeed = drone.velocity;
        //currentLog.collision = collision.IsColliding;
        cumulatedLogs.allLogs.Add(currentLog);
    }

    private void OnApplicationQuit()
    {
        string json = JsonUtility.ToJson(cumulatedLogs);
        File.AppendAllText(final_path, json);
    }


    private string MakeUnique(string path)
    {
        string dir = Path.GetDirectoryName(path);
        string fileName = Path.GetFileNameWithoutExtension(path);
        string fileExt = Path.GetExtension(path);

        for (int i = 1; ; ++i)
        {
            if (!File.Exists(path))
                return path;

            path = Path.Combine(dir, fileName + "_" + i + fileExt);
        }
    }
}
