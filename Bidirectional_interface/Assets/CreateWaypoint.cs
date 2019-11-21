using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CreateWaypoint : MonoBehaviour
{
    // Start is called before the first frame update
    public int waypointNumber;
    public float waypointHeight;
    void Start()
    {
        GameObject waypoint = new GameObject(waypointNumber.ToString());
        waypoint.transform.parent = gameObject.transform;
        waypoint.transform.localPosition = new Vector3(0.0f, waypointHeight/(gameObject.transform.localScale.y), 0.0f);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
