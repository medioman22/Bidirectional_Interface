using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(PositionControl))]
public class HandClutchPositionControl : MonoBehaviour
{
    public UDPCommandManager commandManager;

    public float handRoomScaling = 8.0f;

    [Tooltip("Rotate mocap input along y axis, for instance to align with observation angle")]
    public float inputRotation = 0.0f;
    public bool drawHandTarget = true;

    private PositionControl dronePositionControl;
    private GameObject handTarget;

    private Vector3 handOrigin;
    private Vector3 handClutchOffset;

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
        Vector3 rawHandPosition = commandManager.GetPosition();
        
        // Reset referential for hand
        if (Input.GetKey(KeyCode.R))
        {
            SetHandOrigin(rawHandPosition);
            handClutchOffset = Vector3.zero;
        }

        // Position of the hand relative to the origin point of the "box"
        Vector3 handBoxPosition = rawHandPosition - handOrigin;

        // Clutch activated
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            handClutchOffset = handBoxPosition;
        }
        // Clutch deactivated
        else if (Input.GetKeyUp(KeyCode.Mouse0))
        {
            SetHandOrigin(rawHandPosition);
            handBoxPosition = Vector3.zero;
        }

        // While clutch pressed, don't update target
        if (Input.GetKey(KeyCode.Mouse0))
            return;

        Vector3 targetPosition = ScaleHandPosition(handBoxPosition + handClutchOffset); 
        handTarget.transform.position = targetPosition; 

        dronePositionControl.target = handTarget.transform;

        if (drawHandTarget)
            handTarget.SetActive(true);
        else
            handTarget.SetActive(false);
    }

    private void SetHandOrigin(Vector3 origin)
    {
        // Make sure the center of the box corresponds to the center of the room
        handOrigin = origin;
    }

    private Vector3 ScaleHandPosition(Vector3 handPosition)
    {
        Quaternion rotation = Quaternion.Euler(0, inputRotation, 0);
        handPosition = rotation * handPosition;
        return handPosition * handRoomScaling;
    }
}
