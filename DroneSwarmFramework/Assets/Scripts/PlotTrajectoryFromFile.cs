using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using System.IO;

public class PlotTrajectoryFromFile : MonoBehaviour
{
    public enum SpawnedObject
    {
        Cube,
        Sphere
    }

    public string filepath;
    public SpawnedObject plotObject = SpawnedObject.Cube;
    public Color color = Color.cyan;
    public float size = SimulationData.DroneSize;

    [Tooltip("If true: log the trajectory using the timestamp in the log file. Otherwise simply plots the whole trajectory")]
    public bool animated = false;
    public float startDelay = 1.0f;
    public float timeScale = 1.0f;

    private List<DataLogger.Logger> logs;
    private GameObject rootGO;
    private int animationFrame = 0;

    // Start is called before the first frame update
    void Start()
    {
        string json = File.ReadAllText(filepath);
        logs = JsonUtility.FromJson<DataLogger.LoggerCollection>(json).allLogs;

        if (logs == null)
            Debug.LogError("Unable to load the logs at filepath " + filepath);

        // Root object
        rootGO = new GameObject("Trajectory");

        if (!animated)
        {
            for (int i = 0; i < logs.Count; i++)
            {
                // Plot drone position
                GameObject dronePos;
                if (plotObject == SpawnedObject.Cube)
                    dronePos = GameObject.CreatePrimitive(PrimitiveType.Cube);
                else
                    dronePos = GameObject.CreatePrimitive(PrimitiveType.Sphere);

                dronePos.name = "Point" + i.ToString();
                dronePos.transform.localScale = Vector3.one * size;
                dronePos.transform.position = logs[i].dronePosition;
                dronePos.transform.parent = rootGO.transform;
                dronePos.GetComponent<Renderer>().material.color = color;
            }
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (animated)
        {
            for (int i = animationFrame; i < logs.Count; i++)
            {
                // Plot position according to simulation time
                if (logs[i].absoluteTime <= timeScale * (Time.time - startDelay))
                {
                    Debug.Log("animating");
                    // Plot drone position
                    GameObject dronePos;
                    if (plotObject == SpawnedObject.Cube)
                        dronePos = GameObject.CreatePrimitive(PrimitiveType.Cube);
                    else
                        dronePos = GameObject.CreatePrimitive(PrimitiveType.Sphere);

                    dronePos.name = "Point" + i.ToString();
                    dronePos.transform.localScale = Vector3.one * size;
                    dronePos.transform.position = logs[i].dronePosition;
                    dronePos.transform.parent = rootGO.transform;
                    dronePos.GetComponent<Renderer>().material.color = color;

                    animationFrame++;
                }
                else
                {
                    break;
                }
            }
        }
    }
}
