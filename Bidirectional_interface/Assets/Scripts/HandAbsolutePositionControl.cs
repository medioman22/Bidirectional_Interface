using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HandAbsolutePositionControl : MonoBehaviour
{
    public TextAsset data;
    public KeypointControl droneKeypointControl;

    public float simplifyTrajectoryTolerance = 0.2f;

    private const int nbParameters = 8; // id + position + quaternion

    void Start()
    {
        string[] splitted = data.text.Split(new char[] { ' ', ',', '[', ']' }, System.StringSplitOptions.RemoveEmptyEntries);
        int nbPositions = splitted.Length / nbParameters;

        Debug.Log(nbPositions);

        List<Vector3> rawPositions = new List<Vector3>(nbPositions);
        List<Vector3> filteredPositions = new List<Vector3>();

        for (int i = 0; i < nbPositions; i++)
        {
            rawPositions.Add(new Vector3(float.Parse(splitted[nbParameters * i + 1]), float.Parse(splitted[nbParameters * i + 2]), float.Parse(splitted[nbParameters * i + 3])));
        }

        LineUtility.Simplify(rawPositions, simplifyTrajectoryTolerance, filteredPositions);
        nbPositions = filteredPositions.Count;

        Debug.Log(nbPositions);

        Transform[] targets = new Transform[nbPositions];

        GameObject targetParent = new GameObject("Targets");

        // Read positions from parsed file
        for (int i = 0; i < nbPositions; i++)
        {
            GameObject target = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            target.name = "Target " + i.ToString();
            target.transform.localScale = new Vector3(0.05f, 0.05f, 0.05f);

            //GameObject target = new GameObject("Target " + i.ToString());
            target.transform.parent = targetParent.transform;
            target.transform.position = filteredPositions[i];

            targets[i] = target.transform;
        }

        droneKeypointControl.keypoints = targets;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
