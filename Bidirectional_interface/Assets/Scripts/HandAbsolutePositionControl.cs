using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HandAbsolutePositionControl : MonoBehaviour
{
    public TextAsset data;
    public KeypointControl droneKeypointControl;

    private const int nbParameters = 8; // id + position + quaternion

    void Start()
    {
        string text = data.text;  //this is the content as string
        string[] splitted = text.Split(new char[] { ' ', ',', '[', ']' }, System.StringSplitOptions.RemoveEmptyEntries);

        int nbPositions = splitted.Length / (nbParameters);
        Transform[] targets = new Transform[nbPositions];

        GameObject targetParent = new GameObject("Targets");

        // Read positions from parsed file
        for (int i = 0; i < nbPositions; i++)
        {
            Vector3 position = new Vector3(float.Parse(splitted[nbParameters * i + 1]), float.Parse(splitted[nbParameters * i + 2]), float.Parse(splitted[nbParameters * i + 3]));

            GameObject target = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            target.name = "Target " + i.ToString();
            target.transform.localScale = new Vector3(0.05f, 0.05f, 0.05f);

            //GameObject target = new GameObject("Target " + i.ToString());
            target.transform.parent = targetParent.transform;
            target.transform.position = position;

            targets[i] = target.transform;
        }

        droneKeypointControl.keypoints = targets;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
