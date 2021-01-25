using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(PositionControl))]
[RequireComponent(typeof(VelocityControl))]
public class InputManager : MonoBehaviour
{
    private PositionControl dronePositionControl;
    private UDPCommandManager udp;

    [HideInInspector]
    public bool clutchActivated = false;

    [Tooltip("Read inputs from a controller instead of motion capture.")]
    public bool motionControl = true;
    public float IMU1Scale = 10.0f;
    public float IMU2Scale = 10.0f;
    public float controllerSpeed = 0.1f;
    public float controllerRotationSpeed = 0.5f;

    private GameObject target;

    private Vector3 rawHandPosition = Vector3.zero;
    private Quaternion rawHandRotation = Quaternion.identity;

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

    public bool verticalTask = false;

    public imu_control IMU_FOREARM_CONTROLS = imu_control.PITCH;
    public imu_control IMU_HAND_CONTROLS = imu_control.THRUST;

    public bool lock_roll = false;

    public Vector3 imu1_init;
    public Vector3 imu2_init;

    public Vector3 imu1;
    public Vector3 imu2;

    void Start()
    {
        udp = GetComponent<UDPCommandManager>();

        dronePositionControl = GetComponent<PositionControl>();

        // Instantiate hand target (for optitrack)
        target = new GameObject("Target");
        target.transform.localScale = 2.0f * SimulationData.DroneSize * Vector3.one;
        target.transform.position = dronePositionControl.transform.position;

        initPos = dronePositionControl.transform.position;

        imu1_init = udp.GetIMU1();
        imu2_init = udp.GetIMU2();
    }

    void Update()
    {
        if (!motionControl)
        {
            float h = Input.GetAxis("Horizontal");
            float v = -Input.GetAxis("Vertical");

            Vector3 direction = new Vector3(h, 0.0f, v);

            target.transform.position += direction * Time.deltaTime * controllerSpeed;
            //target.transform.position = initPos + Quaternion.Euler(0, 0, 0) * direction * controllerSpeed;
            Debug.DrawRay(target.transform.position, target.transform.forward, Color.green);
            Debug.DrawRay(target.transform.position, target.transform.right, Color.green);

            dronePositionControl.target = target.transform;
            Vector3 orientation = dronePositionControl.target.eulerAngles;
            dronePositionControl.target.eulerAngles = new Vector3(orientation.x, 0.0f, orientation.z);
        }

        else // IMU
        {
            //Debug.Log("IMU control received");
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

            target.transform.position = initPos + Quaternion.Euler(0, 0, 0) * direction;

            dronePositionControl.target = target.transform;

        }
    }
}