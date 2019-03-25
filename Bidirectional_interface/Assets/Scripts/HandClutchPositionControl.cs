using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(PositionControl))]
public class HandClutchPositionControl : MonoBehaviour
{
    public VirtualHandClutch hand;
    public bool drawHandTarget = true;

    private PositionControl dronePositionControl;
    private GameObject handTarget;
    private Vector3 handRoomScaling;

    void Start()
    {
        dronePositionControl = GetComponent<PositionControl>();

        handTarget = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        Destroy(handTarget.GetComponent<Collider>());
        handTarget.name = "Hand Target";
        handTarget.transform.localScale = 0.5f * SimulationData.DroneSize * Vector3.one;

        handRoomScaling.x = SimulationData.RoomDimensions.x / hand.handReachCube.x;
        handRoomScaling.y = SimulationData.RoomDimensions.y / hand.handReachCube.y;
        handRoomScaling.z = SimulationData.RoomDimensions.z / hand.handReachCube.z;
    }

    void Update()
    {
        Vector3 targetPosition = Vector3.Scale(hand.GetHandPosition(), handRoomScaling);
        handTarget.transform.position = targetPosition; // Get position from mocap

        dronePositionControl.target = handTarget.transform;

        if (drawHandTarget)
            handTarget.SetActive(true);
        else
            handTarget.SetActive(false);
    }
}
