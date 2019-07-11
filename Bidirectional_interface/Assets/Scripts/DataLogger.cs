using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using System.IO;

public class DataLogger : MonoBehaviour
{
    public GameObject drone;

    // all the classes to get informations
    private PositionControl positionCtrl;
    private VelocityControl velocityCtrl;
    private DroneCamera cameraPos;
    private CollisionChecker collision;
    private Rigidbody droneRgbd;
    private HandClutchPositionControl handControl;
    private LaserSensors sensors;

    // -------------------------------------------------------------------

    public string subjectName;
    public string save_path = "c:/Users/aweber/Desktop/Simulation_Logs/";
    private string final_path;

    public bool recording = true;

    // -------------------------------------------------------------------

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

        public float frontObstacle;
        public float backObstacle;
        public float leftObstacle;
        public float rightObstacle;
        public float upObstacle;
        public float downObstacle;

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

    private void Start()
    {
        // all the classes to get informations
        positionCtrl = drone.GetComponent<PositionControl>();
        velocityCtrl = drone.GetComponent<VelocityControl>();
        cameraPos = drone.GetComponent<DroneCamera>();
        collision = drone.GetComponent<CollisionChecker>();
        droneRgbd = drone.GetComponent<Rigidbody>();
        handControl = drone.GetComponent<HandClutchPositionControl>();
        sensors = drone.GetComponent<LaserSensors>();

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

        string experimentType;
        if (handControl.useController)
        {
            experimentType = "Controller";
        }
        else
        {
            experimentType = "MotionCapture";
        }

        final_path = save_path + subjectName + "/" + experimentType + "_" + typeOfCamera + "_" + SceneManager.GetActiveScene().name + ".json";
        final_path = MakeUnique(final_path);

        currentLog = new Logger();
        cumulatedLogs = new LoggerCollection();
    }

    // Update is called once per frame
    void LateUpdate()
    {
        if (recording)
        {
            // Input
            currentLog.absoluteTime = Time.time;
            currentLog.differentialTime = Time.deltaTime;
            currentLog.controlPosition = positionCtrl.target.position;
            currentLog.controlSpeed = new Vector3(velocityCtrl.desiredVx, 0.0f, velocityCtrl.desiredVz);
            currentLog.desiredYawRate = velocityCtrl.desiredYawRate;
            if (!handControl.useController)
            {
                currentLog.clutch = handControl.clutchActivated;
                currentLog.mocapPosition = handControl.MocapHandPosition;
                currentLog.mocapQuaternion = handControl.MocapHandRotation;
            }

            // Output
            currentLog.dronePosition = droneRgbd.position;
            currentLog.droneSpeed = droneRgbd.velocity;
            currentLog.collision = collision.IsColliding;
            // sensors
            currentLog.frontObstacle = sensors.allDistances.frontObstacle;
            currentLog.backObstacle = sensors.allDistances.backObstacle;
            currentLog.leftObstacle = sensors.allDistances.leftObstacle;
            currentLog.rightObstacle = sensors.allDistances.rightObstacle;
            currentLog.upObstacle = sensors.allDistances.upObstacle;
            currentLog.downObstacle = sensors.allDistances.downObstacle;

            cumulatedLogs.allLogs.Add(currentLog);
        }
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
        string initialPath = path;
        string dir = Path.GetDirectoryName(path);
        string fileName = Path.GetFileNameWithoutExtension(path);
        string fileExt = Path.GetExtension(path);

        for (int i = 0; i < 1000; ++i)
        {
            path = Path.Combine(dir, fileName + "_" + i + fileExt);

            if (!File.Exists(path))
                return path;
        }

        Debug.LogError("Could not create unique log file.");
        return initialPath;
    }
}
