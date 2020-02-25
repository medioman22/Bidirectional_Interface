using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text;
using UnityEngine;

public class LogExperiment : MonoBehaviour
{
    public bool saveLog = true;

    private UpdateHandTarget updHandTrgt;
    private List<Vector3> LogCenterOfMass = new List<Vector3>();
    private List<Vector3> LogNextWaypoint = new List<Vector3>();
    private List<float> LogExtension = new List<float>();
    private List<float> LogTargetExtension = new List<float>();
    private List<float> LogTime = new List<float>();
    private List<float> Log1stWaypointTime = new List<float>();
    private List<float> LogExtensionTime = new List<float>();
    private List<float> Log2ndWaypointTime = new List<float>();
    private List<float> Log3ndWaypointTime = new List<float>();
    private List<float> LogContractionTime = new List<float>();
    private List<float> LogHeightError = new List<float>();
    private List<float> LogDistanceError = new List<float>();
    private List<float> LogExtensionError = new List<float>();
    private List<float> LogHeightErrorTime = new List<float>();
    private List<string[]> LogList = new List<string[]>();

    const int GAME_OVER = 9;
    const int LANDED = 0;
    const int FLYING = 3;

    // Start is called before the first frame update
    void Start()
    {
        updHandTrgt = gameObject.GetComponent<UpdateHandTarget>();
        var title = new string[18]{"position_x", "position_y", "position_z", "target_position_x", "target_position_y", "target_position_z", "time", "extension", "target_extension", "1st_waypoint_time", "extension_time", "2nd_waypoint_time", "3rd_waypoint_time", "contraction_time",
            "height_error", "distance_to_waypoint", "extension_error", "reaching_height_time"};
        LogList.Add(title);
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        if (updHandTrgt.experimentState != GAME_OVER && updHandTrgt.droneState == FLYING)
        {
            LogCenterOfMass.Add(updHandTrgt.CenterOfMass);
            LogNextWaypoint.Add(updHandTrgt.nextWaypoint);
            LogTime.Add(updHandTrgt.experimentTime);
            LogExtension.Add(updHandTrgt.extension);
            LogTargetExtension.Add(updHandTrgt.targetExtension);

            Log1stWaypointTime.Add(updHandTrgt.firstWaypointTime);
            LogExtensionTime.Add(updHandTrgt.extensionTime);
            Log2ndWaypointTime.Add(updHandTrgt.secondWaypointTime);
            Log3ndWaypointTime.Add(updHandTrgt.thirdWaypointTime);
            LogContractionTime.Add(updHandTrgt.contractionTime);
            LogHeightError.Add(updHandTrgt.heightError);
            Vector2 distance = new Vector2(updHandTrgt.distanceToWaypoint.x, updHandTrgt.distanceToWaypoint.z);
            LogDistanceError.Add(distance.magnitude);
            LogExtensionError.Add(updHandTrgt.extensionError);
            LogHeightErrorTime.Add(updHandTrgt.reachingHeightTime);
        }
    }



    void OnApplicationQuit()
    {
        Debug.Log("Application ending after " + Time.time + " seconds");


        for (int i = 0; i < LogCenterOfMass.Count; i++)
        {
            string[] LogArray = positionInto3DArray(new List<Vector3> { LogCenterOfMass[i], LogNextWaypoint[i] });
            LogArray[6] = LogTime[i].ToString(); 
            LogArray[7] = LogExtension[i].ToString(); 
            LogArray[8] = LogTargetExtension[i].ToString();
            LogArray[9] = Log1stWaypointTime[i].ToString();
            LogArray[10] = LogExtensionTime[i].ToString();
            LogArray[11] = Log2ndWaypointTime[i].ToString();
            LogArray[12] = Log3ndWaypointTime[i].ToString();
            LogArray[13] = LogContractionTime[i].ToString();
            LogArray[14] = LogHeightError[i].ToString();
            LogArray[15] = LogDistanceError[i].ToString();
            LogArray[16] = LogExtensionError[i].ToString();
            LogArray[17] = LogHeightErrorTime[i].ToString();
            LogList.Add(LogArray);
        }

        if (saveLog) printCSV();

    }
    private string[] positionInto3DArray(List<Vector3> swarmMetrics)
    {
        var i = 0;
        string[] LogArray = new string[18];
        foreach (Vector3 metric in swarmMetrics)
        {
            LogArray[0 + i] = metric.x.ToString();
            LogArray[1 + i] = metric.y.ToString();
            LogArray[2 + i] = metric.z.ToString();
            i += 3;
        }
        return LogArray;
    }

    private string getPath(string subjectName)
    {
        string feedbackSystem = GameObject.Find("Swarm").GetComponent<UpdateHandTarget>().feedback.ToString();
#if UNITY_EDITOR
        return Application.dataPath + "/Logs/"  + DateTime.Now.ToString("h_mm_ss") + "_" + subjectName + "_"+ feedbackSystem + ".csv";
#elif UNITY_ANDROID
            return Application.persistentDataPath+"Saved_data.csv";
#elif UNITY_IPHONE
            return Application.persistentDataPath+"/"+"Saved_data.csv";
#else
            return Application.dataPath +"/"+"Saved_data.csv";
#endif
    }
    private void printCSV()
    {

        string[][] output = new string[LogList.Count][];

        for (int i = 0; i < output.Length; i++) output[i] = LogList[i];

        int length = output.GetLength(0);
        string delimiter = ",";

        StringBuilder sb = new StringBuilder();

        for (int index = 0; index < length; index++)
            sb.AppendLine(string.Join(delimiter, output[index]));

        string filePath = getPath(SimulationData.subjectName);
        //Directory.CreateDirectory(filePath);
        //print(filePath);
        StreamWriter outStream = System.IO.File.CreateText(filePath);
        outStream.WriteLine(sb);
        outStream.Close();
    }
}
