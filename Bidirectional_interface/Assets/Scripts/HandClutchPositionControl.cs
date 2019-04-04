using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(PositionControl))]
[RequireComponent(typeof(VelocityControl))]
public class HandClutchPositionControl : MonoBehaviour
{
    public UDPCommandManager commandManager;
    private PositionControl dronePositionControl;
    private VelocityControl droneVelocityControl;
    private DroneCamera cameraPosition;

    public float handRoomScaling = 8.0f;

    [Tooltip("Rotate mocap input along y axis, for instance to align with observation angle")]
    public float inputRotation = 0.0f;

    public float rotationSpeedScaling = 0.02f;
    public bool drawHandTarget = true;

    [Tooltip("Read inputs from a controller instead of motion capture.")]
    public bool useController = false;
    public float controllerSpeed = 0.025f;
    public float controllerRotationSpeed = 0.5f;

    private GameObject handTarget;

    private Vector3 handOrigin;
    private Vector3 handClutchOffset;
    private Quaternion handReferenceOrientation;
    private float referenceYaw = 0.0f;
    private float cameraViewRotation = 0.0f;
    private float oldCameraViewRotation = 0.0f;

    void Start()
    {
        dronePositionControl = GetComponent<PositionControl>();
        droneVelocityControl = GetComponent<VelocityControl>();

        dronePositionControl.ignoreOrientation = false;

        // This one is optional, thus cameraPosition can be null
        cameraPosition = GetComponent<DroneCamera>();
        if (cameraPosition != null)
        {
            cameraViewRotation = cameraPosition.transform.eulerAngles.y;
            oldCameraViewRotation = cameraViewRotation;
        }

        // Instantiate hand target
        handTarget = GameObject.CreatePrimitive(PrimitiveType.Cube);
        Destroy(handTarget.GetComponent<Collider>());
        handTarget.name = "Hand Target";
        handTarget.transform.localScale = 2.0f * SimulationData.DroneSize * Vector3.one;

        oldCameraViewRotation = inputRotation;
    }

    void Update()
    {
        if (useController)
        {
            float h = Input.GetAxis("Horizontal");
            float v = Input.GetAxis("Vertical");
            float a = Input.GetAxis("Altitude");
            float r = Input.GetAxis("Rotation");

            handTarget.transform.position += Quaternion.Euler(0, inputRotation, 0) * new Vector3(h, a, v) * controllerSpeed;
            dronePositionControl.target = handTarget.transform;

            droneVelocityControl.desired_yaw = r * controllerRotationSpeed;

            if (cameraPosition != null && cameraPosition.FPS)
            {
                inputRotation = transform.eulerAngles.y;
            }
        }
        else // Mocap inputs
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
                    cameraViewRotation = transform.eulerAngles.y + 180;

                    // Recompute offset, because input rotation is changed
                    handClutchOffset = Quaternion.Euler(0, oldCameraViewRotation - cameraViewRotation, 0) * handClutchOffset;

                    oldCameraViewRotation = cameraViewRotation;
                }
            }

            // While clutch pressed, don't update target just rotation
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
        }

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
        Quaternion rotation = Quaternion.Euler(0, inputRotation + cameraViewRotation, 0);
        handPosition = rotation * handPosition;
        return handPosition * handRoomScaling;
    }

    private Quaternion GetHandRotation(Quaternion rawRotation)
    {
        // Order of multiplication is important !
        return Quaternion.Euler(0, cameraViewRotation, 0) * rawRotation * Quaternion.Inverse(handReferenceOrientation);
    }
}
