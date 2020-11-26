﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Collider))]
[RequireComponent(typeof(Rigidbody))]
public class LogCheckPoint : MonoBehaviour
{
    public DataLogger logger;
    public GameObject restartPathPanel;
    public GameObject Drone;
    public UnityEngine.UI.Button restartPathButton;

    [Tooltip("If true, the logger will be activated when the drone exits the collider. If false, it will be deactivated when the drone enters the collider.")]
    public bool startRecording = true;
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

    private void Update()
    {
        if (Input.GetButtonDown("CloseEnough") || OVRInput.Get(OVRInput.Button.One) || (Input.GetKey(KeyCode.LeftShift) && Input.GetKeyDown(KeyCode.A)))
        {
            Done();
        }

    }

    void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Drone")
        {
            Done();
        }
    }

    void Done()
    {
        if (!startRecording)
        {
            logger.recording = false;
            restartPathPanel.SetActive(true);
            HandClutchPositionControl drone = Drone.GetComponent<HandClutchPositionControl>();
            restartPathButton.Select();
            StartCoroutine(WaitAndStopDrone(drone, SimulationData.startUpControlDelay / 3.0f));
        }

    }

    void OnTriggerExit(Collider other)
    {
        if (other.tag == "Drone")
        {
            if (startRecording)
                logger.recording = true;
        }
    }

    IEnumerator WaitAndStopDrone(HandClutchPositionControl drone, float time)
    {
        yield return new WaitForSeconds(time);
        drone.enabled = false;
    }
}
