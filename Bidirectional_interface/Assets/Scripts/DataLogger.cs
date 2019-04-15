using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class DataLogger : MonoBehaviour
{
    // all the classes to get informations
    public UDPCommandManager mocap;
    public PositionControl positionCtrl;
    public VelocityControl velocityCtrl;
    public DroneCamera cameraPos;
    public CollisionChecker collision;
    public Rigidbody drone;
    public HandClutchPositionControl handControl;

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
        public bool clutch;
        public Vector3 mocapPosition;
        public Quaternion mocapQuaternion;
        // Output
        public Vector3 dronePosition;
        public Vector3 droneSpeed;
        public bool collision;
    }
    private Logger currentLog;

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

        currentLog = new Logger();
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
        currentLog.desiredYawRate = velocityCtrl.desiredYawRate;
        if ((int)currentExperiment == 1)
        {
            currentLog.clutch = handControl.clutchActivated;
            currentLog.mocapPosition = mocap.GetPosition(UDPCommandManager.TrackedTargets.RightHand);
            currentLog.mocapQuaternion = mocap.GetQuaternion(UDPCommandManager.TrackedTargets.RightHand);
        }

        // Output
        currentLog.dronePosition = drone.position;
        currentLog.droneSpeed = drone.velocity;
        currentLog.collision = collision.IsColliding;
        cumulatedLogs.allLogs.Add(currentLog);
    }

    private void OnApplicationQuit()
    {
        // OnApplicationQuit() is called even when the script is disabled, thus we must make sure it is not.
        if (enabled)
        {
            string json = JsonUtility.ToJson(cumulatedLogs);
            File.AppendAllText(final_path, json);
        }
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
