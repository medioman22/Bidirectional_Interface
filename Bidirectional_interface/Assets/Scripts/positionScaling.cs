using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(UDPCommandManager))]
public class PositionScaling : MonoBehaviour
{
    UDPCommandManager UDPCommand;
    public Transform drone;
    public Vector3 boxSize = new Vector3(0.5f,0.5f,0.5f);
    // Positions
    Vector3 currentHandPos;
    Vector3 scaledHandPos;
    // angle
    Quaternion currentHandRotation;
    // control the drone position
    public PositionControl dronePosition;
    public GameObject target;
    private float scalingFactorXZ;
    private float scalingFactorY;

    private void Start()
    {
        UDPCommand = GetComponent<UDPCommandManager>();
        ComputeScaleFactor();
    }

    // Update is called once per frame
    private void Update()
    {
        currentHandPos = UDPCommand.GetPosition();
        // TODO : Implement yaw control (not yaw rate)
        //currentHandRotation = UDPCommand.GetQuaternion();

        scaledHandPos = ScalePosition(currentHandPos);
        target.transform.position = scaledHandPos;
        dronePosition.target = target.transform;
    }

    private Vector3 ScalePosition(Vector3 position)
    {
        // TODO : Fix the referentials of the hand and drone to apply scaling.
        return position;
    }

    private void ComputeScaleFactor()
    {
        Vector3 roomSize = SimulationData.RoomDimensions;
        scalingFactorXZ = roomSize[0]/boxSize[0];
        scalingFactorY = roomSize[1]/boxSize[1];
    }
}