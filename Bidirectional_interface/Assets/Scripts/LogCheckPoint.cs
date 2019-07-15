using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Collider))]
[RequireComponent(typeof(Rigidbody))]
public class LogCheckPoint : MonoBehaviour
{
    public DataLogger logger;

    [Tooltip("If true, the logger will be activated when the drone passes through the obstacle. If false, it will be deactivated")]
    public bool recordOnCollision = true;
    public bool hideObjectInPlayMode = true;

    void Start()
    {
        if (hideObjectInPlayMode)
        {
            Renderer renderer = GetComponent<Renderer>();

            if (renderer != null)
            {
                renderer.enabled = false;
            }
        }
    }
    
    void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Drone")
            logger.recording = recordOnCollision;
    }
}
