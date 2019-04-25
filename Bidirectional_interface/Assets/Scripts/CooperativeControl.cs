using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CooperativeControl : MonoBehaviour
{
    private List<MagnetConnector> connectors;

    private GameObject handTarget;
    private GameObject[] droneTargets;

    public bool AllConnected
    {
        get 
        {
            bool detached = false;

            foreach (var connector in connectors)
            {
                // Check if any connector has no drone attached
                if (connector.ConnectedDroneController == null)
                    detached = true;
            }

            return !detached;
        }
    }

    void OnDrawGizmos()
    {
        Gizmos.color = new Color(1.0f, 0.5f, 0.0f);
        
        for (int i = 0; i < connectors.Count; i++)
        {
            // Instantiate target
            Gizmos.DrawCube(droneTargets[i].transform.position, Vector3.one * 0.025f);
        }
    }
    
    void Start()
    {
        connectors = new List<MagnetConnector>(GetComponents<MagnetConnector>());

        // Instantiate hand target
        handTarget = new GameObject("Hand Target");
        handTarget.transform.position = transform.position;
        handTarget.transform.rotation = transform.rotation;
        handTarget.transform.localScale = transform.localScale;

        droneTargets = new GameObject[connectors.Count];
        for (int i = 0; i < connectors.Count; i++)
        {
            // Instantiate target
            droneTargets[i] = new GameObject("Drone Target " + i.ToString());
            droneTargets[i].transform.position = connectors[i].AnchorPosition + Vector3.up * connectors[i].linkDistance;
        }
    }

    // Update is called once per frame
    void Update()
    {
        float targetYaw = 0.0f;
        float targetInclination = 0.0f;

        // Apply cooperative control
        if (AllConnected)
        {
            // Set targets position
            for (int i = 0; i < connectors.Count; i++)
            {
                droneTargets[i].transform.position = handTarget.transform.TransformPoint(connectors[i].anchor) + Vector3.up * connectors[i].linkDistance;

                if (connectors[i].ConnectedDroneController != null)
                {
                    connectors[i].ConnectedDroneController.target = droneTargets[i].transform;
                }
            }
        }
        else
        {
            // Set targets position
            for (int i = 0; i < connectors.Count; i++)
            {
                droneTargets[i].transform.position = handTarget.transform.TransformPoint(connectors[i].anchor) + Vector3.up * connectors[i].linkDistance;

                if (connectors[i].ConnectedDroneController != null)
                {
                    connectors[i].ConnectedDroneController.target = droneTargets[i].transform;
                }
            }
        }
    }
}
