using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(PositionControl))]
public class KeypointControl : MonoBehaviour
{
    public Transform[] keypoints;
    public float positionTolerance = 0.1f;

    private PositionControl posController;
    private int targetIndex;

    // Start is called before the first frame update
    void Start()
    {
        posController = GetComponent<PositionControl>();

        if (keypoints.Length > 0)
        {
            targetIndex = 0;
        }
        else
        {
            targetIndex = -1;
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (keypoints.Length == 0)
            targetIndex = -1;
        else if (keypoints.Length > 0 && targetIndex == -1)
            targetIndex = 0;
        else if (keypoints.Length > 0 && targetIndex >= keypoints.Length)
        {
            targetIndex = keypoints.Length - 1;
            posController.controlYaw = true;
        }
            

        if (targetIndex == -1)
            return;

        // Set target keypoint
        posController.target = keypoints[targetIndex];

        if (!posController.target)
        {
            while(!posController.target)
            {
                targetIndex++;
                posController.target = keypoints[targetIndex];
            }
        }

        // Move to the next keypoint
        if (Vector3.Magnitude(keypoints[targetIndex].position - transform.position) < positionTolerance)
        {
            targetIndex++;
        }
    }
}
