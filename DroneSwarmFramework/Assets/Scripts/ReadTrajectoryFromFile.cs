using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ReadTrajectoryFromFile : MonoBehaviour
{
    public TextAsset data;
    public KeypointControl droneKeypointControl;
    public PositionControl dronePositionControl;

    public Material targetMaterial;

    [Tooltip("Follow the data in real-time, or follow a simplified keypoint trajectory")]
    public bool online;

    public float simplifyTrajectoryTolerance = 0.1f;

    List<Vector3> rawPositions;
    private GameObject handTarget;

    void Start()
    {
        handTarget = new GameObject("Hand Target");

        string[] splitted = data.text.Split(new char[] { ' ', ',', '[', ']' }, System.StringSplitOptions.RemoveEmptyEntries);
        int nbPositions = splitted.Length / SimulationData.nbParametersMocap;

        rawPositions = new List<Vector3>(nbPositions);
        List<Vector3> filteredPositions = new List<Vector3>();

        for (int i = 0; i < nbPositions; i++)
        {
            rawPositions.Add(new Vector3(float.Parse(splitted[SimulationData.nbParametersMocap * i + 1]), 
                                         float.Parse(splitted[SimulationData.nbParametersMocap * i + 2]), 
                                         float.Parse(splitted[SimulationData.nbParametersMocap * i + 3])));
        }

        LineUtility.Simplify(rawPositions, simplifyTrajectoryTolerance, filteredPositions);
        nbPositions = filteredPositions.Count;

        Transform[] targets = new Transform[nbPositions];

        GameObject targetParent = new GameObject("Targets");

        // Read positions from parsed file
        for (int i = 0; i < nbPositions; i++)
        {
            GameObject target = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            Destroy(target.GetComponent<Collider>());
            target.name = "Target " + i.ToString();
            target.transform.localScale = 0.5f * SimulationData.DroneSize * Vector3.one;

            target.transform.parent = targetParent.transform;
            target.transform.position = filteredPositions[i];

            target.GetComponent<Renderer>().material = targetMaterial;

            targets[i] = target.transform;
        }

        droneKeypointControl.keypoints = targets;
    }

    void Update()
    {
        int index = (int)(Time.time / SimulationData.MocapUpdateDeltaTime);

        if (index >= rawPositions.Count)
            index = rawPositions.Count - 1;

        handTarget.transform.position = rawPositions[index];

        if (online)
        {
            droneKeypointControl.enabled = false;
            dronePositionControl.target = handTarget.transform;
        }
        else
        {
            droneKeypointControl.enabled = true;
        }

    }

    // Draw hand position
    void OnDrawGizmos()
    {
        if (online && handTarget != null)
        {
            Gizmos.color = Color.red;
            Gizmos.DrawWireSphere(handTarget.transform.position, SimulationData.DroneSize);
        }
    }
}