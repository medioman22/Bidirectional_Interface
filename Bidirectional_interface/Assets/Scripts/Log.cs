using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text;
using UnityEngine;

public class Log : MonoBehaviour
{
    public bool saveLog = true;

    private List<string[]> LogList = new List<string[]>();

    //Saving positions to export them in a csv
    private List<Vector3> LogPositions = new List<Vector3>();
    private List<Vector3> LogTargetPositions = new List<Vector3>();
    private List<Vector3> LogSpeed = new List<Vector3>();
    private List<Vector3> LogTargetSpeed = new List<Vector3>();
    private List<Vector3> LogTheta = new List<Vector3>();
    private List<Vector3> LogTargetTheta = new List<Vector3>();
    private List<Vector3> LogTargetAcceleration = new List<Vector3>();
    private string LogSlave;

    // Start is called before the first frame update
    void Start()
    {
        var title = NameInto3DArray(new List<string>() { "position", "targetPosition", "velocity", "targetVelocity", "targetAcceleration", "theta", "targetTheta" });
        LogList.Add(title);
    }

    // Update is called once per frame
    void Update()
    {
        var vc = GetComponent<VelocityControl>();
        var pc = GetComponent<PositionControl>();
        LogPositions.Add(pc.transform.position);
        LogTargetPositions.Add(pc.target.position);
        LogSpeed.Add(vc.state.VelocityVector);
        LogTargetSpeed.Add(vc.desiredVelocity);
        LogTheta.Add(vc.state.Angles);
        LogTargetTheta.Add(vc.desiredTheta);
        LogTargetAcceleration.Add(vc.desiredAcceleration);
        if (vc.isSlave) LogSlave = "Slave";
        else LogSlave = "Master";

    }

    void OnApplicationQuit()
    {
        Debug.Log("Application ending after " + Time.time + " seconds");

            
            for (int i = 0; i < LogPositions.Count; i++)
            {
                var array = positionInto3DArray(new List<Vector3> { LogPositions[i], LogTargetPositions[i], LogSpeed[i], LogTargetSpeed[i], LogTargetAcceleration[i], LogTheta[i], LogTargetTheta[i] });
                array[array.Length - 1] = LogSlave;
                LogList.Add(array);
            }
            if (saveLog) printCSV();
        
    }

    private string[] positionInto3DArray(List<Vector3> swarmMetrics)
    {
        string[] metricsArray = new string[swarmMetrics.Count * 3 + 1];

        var i = 0;
        foreach (Vector3 metric in swarmMetrics)
        {
            metricsArray[0 + i] = metric.x.ToString();
            metricsArray[1 + i] = metric.y.ToString();
            metricsArray[2 + i] = metric.z.ToString();
            i += 3;
        }
        return metricsArray;
    }
    private string[] NameInto3DArray(List<string> names)
    {
        //*3 because in 3D, +1 to leave one space for "master" or "slave"
        string[] nameArray = new string[names.Count * 3 + 1];
        var i = 0;
        foreach (string name in names)
        {
            nameArray[0 + i] = name + "_x";
            nameArray[1 + i] = name + "_y";
            nameArray[2 + i] = name + "_z";
            i += 3;
        }
        nameArray[nameArray.Length - 1] = "MasterOrSlave";
        return nameArray;
    }

    private string getPath(string subjectName)
    {
#if UNITY_EDITOR
        return Application.dataPath + "/Logs/" + subjectName + "_" + DateTime.Now.ToString("h_mm_ss") + ".csv";
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
