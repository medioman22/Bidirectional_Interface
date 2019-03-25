using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(PositionControl))]
public class HandClutchPositionControl : MonoBehaviour
{
    public bool drawHand = true;

    private PositionControl dronePositionControl;
    private GameObject handTarget;

    void Start()
    {
        dronePositionControl = GetComponent<PositionControl>();

        handTarget = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        Destroy(handTarget.GetComponent<Collider>());
        handTarget.name = "Hand Target";
        handTarget.transform.localScale = 0.5f * SimulationData.DroneSize * Vector3.one;
    }
    
    void Update()
    {
        handTarget.transform.position = Vector3.zero; // Get position from mocap

        dronePositionControl.target = handTarget.transform;

        if (drawHand)
            handTarget.SetActive(true);
        else
            handTarget.SetActive(false);
    }
}
