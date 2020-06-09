using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(PositionControl))]
[RequireComponent(typeof(VelocityControl))]
public class HandClutchPositionControl : MonoBehaviour
{
    public int handRigidbodyID = 1;
    private OptitrackStreamingClient streamingClient;
    private PositionControl dronePositionControl;
    private VelocityControl droneVelocityControl;
    private DroneCamera cameraPosition;
    private UDPCommandManager udp;

    public float handRoomScaling = 8.0f;
    [HideInInspector]
    public bool clutchActivated = false;

    // mocapInputRotation = 90 --> you are facing the wall, and have the computers to your left and the entrance door to your right.
    // mocapInputRotation = -90 --> you are facing the wall, and have the computers to your right.
    // mocapInputRotation = 180 --> you are facing the computers
    // mocapInputRotation = 0 --> you have the computers behind you
    [Tooltip("Change forward direction (z-axis) for mocap")]
    public float mocapInputRotation = 90.0f;
    public float observationInputRotation = 0.0f;

    public float rotationSpeedScaling = 0.02f;
    public bool drawHandTarget = true;

    [Tooltip("Read inputs from a controller instead of motion capture.")]
    public bool useController = false;
    public float IMU1Scale = 10.0f;
    public float IMU2Scale = 10.0f;
    public float controllerSpeed = 0.025f;
    public float controllerRotationSpeed = 0.5f;

    private GameObject handTarget;

    private float cameraViewRotation = 0.0f;
    private float oldCameraViewRotation = 0.0f;

    private Vector3 rawHandPosition = Vector3.zero;
    private Quaternion rawHandRotation = Quaternion.identity;
    private Vector3 oldRawHandPosition;
    private float referenceYaw = 0.0f;

    private float fixedYaw = 0.0f;
    private Vector3 initPos;

    // For logger
    public Vector3 MocapHandPosition
    {
        get
        {
            return rawHandPosition;
        }
    }

    // For logger
    public Quaternion MocapHandRotation
    {
        get
        {
            return rawHandRotation;
        }
    }

    void Start()
    {
        udp = GetComponent<UDPCommandManager>();

        dronePositionControl = GetComponent<PositionControl>();
        droneVelocityControl = GetComponent<VelocityControl>();

        // This one is optional, thus cameraPosition can be null
        cameraPosition = GetComponent<DroneCamera>();
        cameraViewRotation = 0.0f;
        if (cameraPosition != null)
        {
            cameraViewRotation = cameraPosition.transform.eulerAngles.y;
            oldCameraViewRotation = cameraViewRotation;

            if (cameraPosition.FPS)
                dronePositionControl.controlYaw = false;
            else
            {
                dronePositionControl.controlYaw = true;
                fixedYaw = transform.eulerAngles.y;
                dronePositionControl.targetYaw = fixedYaw;
            }
        }

        // Instantiate hand target
        handTarget = new GameObject("Hand Target");
        handTarget.transform.localScale = 2.0f * SimulationData.DroneSize * Vector3.one;
        handTarget.transform.position = dronePositionControl.transform.position;

        initPos = dronePositionControl.transform.position;

        streamingClient = OptitrackStreamingClient.FindDefaultClient();

        // If we still couldn't find one, disable this component.
        if (streamingClient == null)
        {
            Debug.LogError("Streaming client not found, place a streaming client in the scene.");
        }
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

            if (cameraPosition != null && cameraPosition.FPS)
                droneVelocityControl.desiredYawRate = r * controllerRotationSpeed;
            else if (cameraPosition != null && !cameraPosition.FPS)
                dronePositionControl.targetYaw = fixedYaw;
        }
        else // IMU inputs
        {
            Debug.Log("imu1=" + udp.GetIMU1());
            Debug.Log("imu2=" + udp.GetIMU2());

            var imu1 = udp.GetIMU1();
            var imu2 = udp.GetIMU2();

            float h = 0.0f;
            float v = 0.0f;
            float a = 0.0f;
            float r = 0.0f;

            h = imu1.y / IMU1Scale;
            a = -imu2.y / IMU2Scale;

            Vector3 direction = new Vector3(h, a, 0);

            // Update observation input rotation if FPS mode
            if (cameraPosition != null && cameraPosition.FPS)
            {
                observationInputRotation = transform.eulerAngles.y;
            }

            handTarget.transform.position = initPos + Quaternion.Euler(0, observationInputRotation, 0) * direction;

            dronePositionControl.target = handTarget.transform;

            if (cameraPosition != null && cameraPosition.FPS)
                droneVelocityControl.desiredYawRate = r * controllerRotationSpeed;
            else if (cameraPosition != null && !cameraPosition.FPS)
                dronePositionControl.targetYaw = fixedYaw;
        }
    }
}