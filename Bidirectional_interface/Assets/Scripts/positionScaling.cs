using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(UDPCommandManager))]
public class positionScaling : MonoBehaviour
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
        computeScaleFactor();
    }

    // Update is called once per frame
    private void Update()
    {
        currentHandPos = UDPCommand.getPosition();
        // TODO : Implement yaw control (not yaw rate)
        //currentHandRotation = UDPCommand.getQuaternion();

        scaledHandPos = scalePosition(currentHandPos);
        target.transform.position = scaledHandPos;
        dronePosition.target = target.transform;
    }

    private Vector3 scalePosition(Vector3 position)
    {
        // TODO : Fix the referentials of the hand and drone to apply scaling.
        return position;
    }

    private void computeScaleFactor()
    {
        Vector3 roomSize = SimulationData.RoomDimensions;
        scalingFactorXZ = roomSize[0]/boxSize[0];
        scalingFactorY = roomSize[1]/boxSize[1];
    }
}