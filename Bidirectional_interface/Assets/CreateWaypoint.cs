using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CreateWaypoint : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        GameObject waypoint = new GameObject("waypointPosition");
        waypoint.transform.parent = gameObject.transform;
        waypoint.transform.localPosition = new Vector3(0.0f, SimulationData.desiredHeight/(gameObject.transform.localScale.y), 0.0f);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
