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
    public float LeapScale = 10.0f;
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

    public enum imu_control
    {
        ROLL = 0,   //like turn
        PITCH = 1, //like speed
        YAW = 2,
        THRUST = 3,
        MINUS_ROLL = 4,   //like turn
        MINUS_PITCH = 5, //like speed
        MINUS_YAW = 6,
        MINUS_THRUST = 7,
    };

    public enum leap_control
    {
        ROLL = 0,   //like turn
        PITCH = 1, //like speed
        YAW = 2,
        THRUST = 3,
        MINUS_ROLL = 4,   //like turn
        MINUS_PITCH = 5, //like speed
        MINUS_YAW = 6,
        MINUS_THRUST = 7,
    };

    public bool verticalTask = false;

    public imu_control IMU_FOREARM_CONTROLS = imu_control.PITCH;
    public imu_control IMU_HAND_CONTROLS = imu_control.THRUST;
    //public leap_control LEAP_CONTROLS = leap_control.PITCH;

    public bool lock_roll = false;

    public Vector3 imu1_init;
    public Vector3 imu2_init;
    public Vector3 leap_init;

    public Vector3 imu1;
    public Vector3 imu2;
    public Vector3 leap;

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

            // used with fps
            /*
            if (cameraPosition.FPS)
                dronePositionControl.controlYaw = false;
            else
            {
                dronePositionControl.controlYaw = true;
                fixedYaw = transform.eulerAngles.y;
                dronePositionControl.targetYaw = fixedYaw;
            }*/

            dronePositionControl.controlYaw = true;
            fixedYaw = transform.eulerAngles.y;
            dronePositionControl.targetYaw = fixedYaw;
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


        imu1_init = udp.GetIMU1();
        imu2_init = udp.GetIMU2();
        //leap_init = udp.GetLEAP();
    }

    void Update()
    {
        if (useController)
        {
            float v = -Input.GetAxis("Horizontal");
            float h = Input.GetAxis("Vertical");
            float a = Input.GetAxis("Altitude");
            float r = Input.GetAxis("Rotation");

            Vector3 direction = new Vector3(h, a, v);

            // Update observation input rotation if FPS mode
            if (cameraPosition != null)
            {
                observationInputRotation = transform.eulerAngles.y;
            }

            handTarget.transform.position += Quaternion.Euler(0, observationInputRotation, 0) * direction * controllerSpeed;

            dronePositionControl.target = handTarget.transform;

            if (cameraPosition != null)
                // used in fps
                //droneVelocityControl.desiredYawRate = r * controllerRotationSpeed;
                dronePositionControl.targetYaw = fixedYaw;
        }
        else // IMU / Leap inputs, 
        {
            Debug.Log("imu1=" + udp.GetIMU1());
            Debug.Log("imu2 = " + udp.GetIMU2());

            imu1 = udp.GetIMU1() - imu1_init;
            imu2 = udp.GetIMU2() - imu2_init;

            float pitch = 0.0f;
            float roll = 0.0f;
            float thrust = 0.0f;
            float yaw = 0.0f;

            float imu1_val = -imu1.z / IMU1Scale;
            float imu2_val = -imu2.y / IMU2Scale;
            if (verticalTask)
            {
                imu1_val = -imu1.y / IMU2Scale;
            }

            //float leap_val = -leap.z / LeapScale;

            //switch (LEAP_CONTROLS)
            //{
            //    case leap_control.ROLL:
            //        roll = leap_val;
            //        break;
            //    case leap_control.PITCH:
            //        pitch = leap_val;
            //        break;
            //    case leap_control.YAW:
            //        yaw = leap_val;
            //        break;
            //    case leap_control.THRUST:
            //        thrust = leap_val;
            //        break;
            //    case leap_control.MINUS_ROLL:
            //        roll = -leap_val;
            //        break;
            //    case leap_control.MINUS_PITCH:
            //        pitch = -leap_val;
            //        break;
            //    case leap_control.MINUS_YAW:
            //        yaw = -leap_val;
            //        break;
            //    case leap_control.MINUS_THRUST:
            //        thrust = -leap_val;
            //        break;
            //}

            switch (IMU_FOREARM_CONTROLS)
            {
                case imu_control.ROLL:
                    roll = imu1_val;
                    break;
                case imu_control.PITCH:
                    pitch = imu1_val;
                    break;
                case imu_control.YAW:
                    yaw = imu1_val;
                    break;
                case imu_control.THRUST:
                    thrust = imu1_val;
                    break;
                case imu_control.MINUS_ROLL:
                    roll = -imu1_val;
                    break;
                case imu_control.MINUS_PITCH:
                    pitch = -imu1_val;
                    break;
                case imu_control.MINUS_YAW:
                    yaw = -imu1_val;
                    break;
                case imu_control.MINUS_THRUST:
                    thrust = -imu1_val;
                    break;
            }

            switch (IMU_HAND_CONTROLS)
            {
                case imu_control.ROLL:
                    roll = imu2_val;
                    break;
                case imu_control.PITCH:
                    pitch = imu2_val;
                    break;
                case imu_control.YAW:
                    yaw = imu2_val;
                    break;
                case imu_control.THRUST:
                    thrust = imu2_val;
                    break;
                case imu_control.MINUS_ROLL:
                    roll = -imu2_val;
                    break;
                case imu_control.MINUS_PITCH:
                    pitch = -imu2_val;
                    break;
                case imu_control.MINUS_YAW:
                    yaw = -imu2_val;
                    break;
                case imu_control.MINUS_THRUST:
                    thrust = -imu2_val;
                    break;
            }

            if (lock_roll)
            {
                roll = 0;
            }

            Vector3 direction = new Vector3(pitch, thrust, roll);

            // Update observation input rotation if FPS mode
            if (cameraPosition != null)
            {
                observationInputRotation = transform.eulerAngles.y;
            }

            handTarget.transform.position = initPos + Quaternion.Euler(0, observationInputRotation, 0) * direction;

            dronePositionControl.target = handTarget.transform;

            if (cameraPosition != null)
                // used in fps
                //droneVelocityControl.desiredYawRate = yaw * controllerRotationSpeed;
                dronePositionControl.targetYaw = fixedYaw;
        }
    }
}