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

    [Tooltip("Which hand (tracked by the Mocap) controls the drone")]
    public UDPCommandManager.TrackedTargets trackedHand;

    public float handRoomScaling = 8.0f;
    [HideInInspector]
    public bool clutchActivated = false;

    // mocapInputRotation = 0 --> you are facing the wall, and have the computers to your left and the entrance door to your right.
    // mocapInputRotation = -90 --> you are facing the computers
    // mocapInputRotation = 90 --> you have the computers behind you
    [Tooltip("Change forward direction (z-axis) for mocap")]
    public float mocapInputRotation = 0.0f;
    public float observationInputRotation = 0.0f;

    public float rotationSpeedScaling = 0.02f;
    public bool drawHandTarget = true;

    [Tooltip("Read inputs from a controller instead of motion capture.")]
    public bool useController = false;
    public float controllerSpeed = 0.025f;
    public float controllerRotationSpeed = 0.5f;

    private GameObject handTarget;
    
    private float cameraViewRotation = 0.0f;
    private float oldCameraViewRotation = 0.0f;

    private Vector3 oldRawHandPosition;
    private float referenceYaw = 0.0f;

    void Start()
    {
        dronePositionControl = GetComponent<PositionControl>();
        droneVelocityControl = GetComponent<VelocityControl>();

        dronePositionControl.controlYaw = false;

        // This one is optional, thus cameraPosition can be null
        cameraPosition = GetComponent<DroneCamera>();
        cameraViewRotation = 0.0f;
        if (cameraPosition != null)
        {
            cameraViewRotation = cameraPosition.transform.eulerAngles.y;
            oldCameraViewRotation = cameraViewRotation;
        }

        // Instantiate hand target
        handTarget = new GameObject("Hand Target");
        handTarget.transform.localScale = 2.0f * SimulationData.DroneSize * Vector3.one;
        handTarget.transform.position = dronePositionControl.transform.position;
    }

    void Update()
    {
        if (useController)
        {
            float h = Input.GetAxis("Horizontal");
            float v = Input.GetAxis("Vertical");
            float a = Input.GetAxis("Altitude");
            float r = Input.GetAxis("Rotation");

            Vector3 direction = new Vector3(h, a, v);

            // Update observation input rotation if FPS mode
            if (cameraPosition != null && cameraPosition.FPS)
            {
                observationInputRotation = transform.eulerAngles.y;
            }

            handTarget.transform.position += Quaternion.Euler(0, observationInputRotation, 0) * direction * controllerSpeed;

            dronePositionControl.target = handTarget.transform;
            droneVelocityControl.desiredYawRate = r * controllerRotationSpeed;
        }
        else // Mocap inputs
        {
            Vector3 rawHandPosition = commandManager.GetPosition(trackedHand);
            Quaternion rawHandRotation = commandManager.GetQuaternion(trackedHand);

            Vector3 deltaHandPosition = rawHandPosition - oldRawHandPosition;
            float handYaw = rawHandRotation.eulerAngles.y;

            oldRawHandPosition = rawHandPosition;

            if (deltaHandPosition.magnitude > 1.0f)
                return;

            // Update observation input rotation if FPS mode
            if (cameraPosition != null && cameraPosition.FPS)
            {
                observationInputRotation = transform.eulerAngles.y;
            }

            // Clutch triggered, set reference yaw
            if (Input.GetKeyDown(KeyCode.Mouse0))
            {
                dronePositionControl.target = transform;
                referenceYaw = handYaw;
            }

            // Clutch activated
            if (Input.GetKey(KeyCode.Mouse0))
            {
                clutchActivated = true;
                droneVelocityControl.desiredYawRate = Mathf.DeltaAngle(referenceYaw, handYaw) * rotationSpeedScaling;
            }
            else
            {
                // Update drone target
                clutchActivated = false;
                droneVelocityControl.desiredYawRate = 0.0f;
                handTarget.transform.position += Quaternion.Euler(0, observationInputRotation + mocapInputRotation, 0) * deltaHandPosition * handRoomScaling;
                dronePositionControl.target = handTarget.transform;
            }
        }

        if (drawHandTarget)
            handTarget.SetActive(true);
        else
            handTarget.SetActive(false);
    }
}
