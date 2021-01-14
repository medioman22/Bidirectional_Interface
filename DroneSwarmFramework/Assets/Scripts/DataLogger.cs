using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using System.IO;

public class DataLogger : MonoBehaviour
{
    public GameObject drone;
    public GameObject masterDrone;

    // all the classes to get informations
    private PositionControl positionCtrl;
    private VelocityControl velocityCtrl;
    private CollisionChecker collision;
    private Rigidbody droneRgbd;
    private Rigidbody slaveDroneRgbd;
    private InputManager handControl;
    private LaserSensors sensors;
    private ExperimentSetup expSetup;

    // -------------------------------------------------------------------

    private expType eType;
    private hapticType hType;

    public string subjectName;
    public string savePath = "./SimulationLogs/";

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
        public Vector3 slaveDronePosition;
        public Vector3 droneSpeed;
        public Vector3 slaveDroneSpeed;
        public float spread;

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
        // Master drone properties: position (target, actual) and velocity
        positionCtrl = masterDrone.GetComponent<PositionControl>();
        droneRgbd = masterDrone.GetComponent<Rigidbody>();
        handControl = masterDrone.GetComponent<InputManager>();

        // Slave drone: positon, speed, spread, sensor distances, collision detection
        velocityCtrl = drone.GetComponent<VelocityControl>();
        slaveDroneRgbd = drone.GetComponent<Rigidbody>();
        collision = drone.GetComponent<CollisionChecker>();
        sensors = drone.GetComponent<LaserSensors>();
        expSetup = this.GetComponent<ExperimentSetup>();

        eType = expSetup.ExperimentType;
        hType = expSetup.HapticType;

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
            if (handControl.motionControl)
                currentLog.clutch = handControl.clutchActivated;

            // Master Output
            currentLog.controlPosition = positionCtrl.target.position;
            currentLog.dronePosition = droneRgbd.position;
            currentLog.droneSpeed = droneRgbd.velocity;

            // Slave drone
            currentLog.slaveDronePosition = slaveDroneRgbd.position;
            currentLog.slaveDroneSpeed = slaveDroneRgbd.velocity;
            currentLog.controlSpeed = new Vector3(velocityCtrl.desiredVx, 0.0f, velocityCtrl.desiredVz);
            currentLog.spread = velocityCtrl.closeness;
            currentLog.collision = collision.IsColliding;

            //sensors
            currentLog.frontObstacle = sensors.allDistances.frontObstacle;
            currentLog.backObstacle = sensors.allDistances.backObstacle;
            currentLog.leftObstacle = sensors.allDistances.leftObstacle;
            currentLog.rightObstacle = sensors.allDistances.rightObstacle;

            cumulatedLogs.allLogs.Add(currentLog);
        }
    }

    private void OnApplicationQuit()
    {
        // OnApplicationQuit() is called even when the script is disabled, thus we must make sure it is not.
        if (enabled)
        {
            SaveResults();
        }
    }

    public void SaveResults()
    {

        // Create filename
        string experimentType;
        if (!handControl.motionControl)
        {
            experimentType = "Controller";
        }
        else
        {
            experimentType = "MotionCapture";
        }

        subjectName = subjectName + "_" + experimentType;

        // Create folders if needed
        if (!Directory.Exists(savePath))
        {
            Directory.CreateDirectory(savePath);
        }

        if (!Directory.Exists(savePath+subjectName))
        {
            Directory.CreateDirectory(savePath + subjectName);
        }

        string pathName = "";

        pathName = eType.ToString();

        if (eType==expType.Haptics)
        {
            pathName = pathName + "_" + hType.ToString();
        }

        // Create a formatted time stamp with the current time
        string timeStamp = System.DateTime.Now.ToString("yyyy_MM_dd_HH_mm_ss");

        string finalPath = savePath + subjectName + "/" + pathName + "_" + timeStamp + ".json";

        // Save results
        string json = JsonUtility.ToJson(cumulatedLogs);
        File.AppendAllText(finalPath, json);
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
