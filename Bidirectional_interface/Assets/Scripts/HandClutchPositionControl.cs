using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(PositionControl))]
[RequireComponent(typeof(VelocityControl))]
public class HandClutchPositionControl : MonoBehaviour
{
    public UDPCommandManager commandManager;

    public float handRoomScaling = 8.0f;

    [Tooltip("Rotate mocap input along y axis, for instance to align with observation angle")]
    public float inputRotation = 0.0f;

    public float rotationSpeedScaling = 0.02f;
    public bool drawHandTarget = true;

    private PositionControl dronePositionControl;
    private VelocityControl droneVelocityControl;
    private CameraPosition cameraPosition;

    private GameObject handTarget;

    private Vector3 handOrigin;
    private Vector3 handClutchOffset;
    private Quaternion handReferenceOrientation;
    private float referenceYaw = 0.0f;
    private float oldInputRotation = 0.0f;

    void Start()
    {
        dronePositionControl = GetComponent<PositionControl>();
        droneVelocityControl = GetComponent<VelocityControl>();

        // This one is optional, thus cameraPosition can be null
        cameraPosition = GetComponent<CameraPosition>();

        // Instantiate hand target
        handTarget = GameObject.CreatePrimitive(PrimitiveType.Cube);
        Destroy(handTarget.GetComponent<Collider>());
        handTarget.name = "Hand Target";
        handTarget.transform.localScale = 2.0f * SimulationData.DroneSize * Vector3.one;

        oldInputRotation = inputRotation;
    }

    void Update()
    {
        Vector3 rawHandPosition = commandManager.GetPosition();
        Quaternion rawHandRotation = commandManager.GetQuaternion();
        
        // Reset referential for hand
        if (Input.GetKey(KeyCode.Mouse1))
        {
            SetHandOrigin(rawHandPosition, rawHandRotation);
            handClutchOffset = Vector3.zero;
        }

        // Position of the hand relative to the origin point of the "box"
        Vector3 handBoxPosition = rawHandPosition - handOrigin;
        Quaternion handRotation = GetHandRotation(rawHandRotation);

        // Clutch activated
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            handClutchOffset += handBoxPosition;
            referenceYaw = handRotation.eulerAngles.y;
        }
        // Clutch deactivated
        else if (Input.GetKeyUp(KeyCode.Mouse0))
        {
            SetHandOrigin(rawHandPosition, rawHandRotation);
            handBoxPosition = Vector3.zero;

            if (cameraPosition != null && cameraPosition.FPS)
            {
                Debug.Log(transform.eulerAngles.y);
                inputRotation = transform.eulerAngles.y + 180;

                handClutchOffset = Quaternion.Euler(0, oldInputRotation - inputRotation, 0) * handClutchOffset;

                oldInputRotation = inputRotation;
            }
        }

        // While clutch pressed, don't update target
        if (Input.GetKey(KeyCode.Mouse0))
        {
            droneVelocityControl.desired_yaw = Mathf.DeltaAngle(referenceYaw, handRotation.eulerAngles.y) * rotationSpeedScaling;
            return;
        }
        else
        {
            droneVelocityControl.desired_yaw = 0.0f;
        }

        Vector3 targetPosition = ScaleHandPosition(handBoxPosition + handClutchOffset); 
        handTarget.transform.position = targetPosition; 

        
        handTarget.transform.rotation = GetHandRotation(rawHandRotation);

        dronePositionControl.target = handTarget.transform;

        if (drawHandTarget)
            handTarget.SetActive(true);
        else
            handTarget.SetActive(false);
    }

    private void SetHandOrigin(Vector3 origin, Quaternion orientation)
    {
        handOrigin = origin;
        handReferenceOrientation = orientation;
    }

    private Vector3 ScaleHandPosition(Vector3 handPosition)
    {
        Quaternion rotation = Quaternion.Euler(0, inputRotation, 0);
        handPosition = rotation * handPosition;
        return handPosition * handRoomScaling;
    }

    private Quaternion GetHandRotation(Quaternion rawRotation)
    {
        // Order of multiplication is important !
        return Quaternion.Euler(0, inputRotation, 0) * rawRotation * Quaternion.Inverse(handReferenceOrientation);
    }
}
