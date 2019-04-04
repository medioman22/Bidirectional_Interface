using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(PositionControl))]
public class HandAbsolutePositionControl : MonoBehaviour
{
    public UDPCommandManager commandManager;
    private PositionControl dronePositionControl;

    public Vector3 handReachCube = 0.7f * Vector3.one;

    [Tooltip("Rotate mocap input along y axis, for instance to align with observation angle")]
    public float inputRotation = 0.0f;
    //public VirtualHand hand;
    public bool drawHandTarget = true;

    [Tooltip("Read inputs from a controller instead of motion capture.")]
    public bool useController = false;
    public float controllerSpeed = 0.025f;

    // For motion capture inputs
    private GameObject handTarget;
    private Vector3 handRoomScaling;
    private Vector3 handOrigin;

    void Start()
    {
        dronePositionControl = GetComponent<PositionControl>();
        dronePositionControl.ignoreOrientation = true;

        handTarget = GameObject.CreatePrimitive(PrimitiveType.Cube);
        Destroy(handTarget.GetComponent<Collider>());
        handTarget.name = "Hand Target";
        handTarget.transform.localScale = 2.0f * SimulationData.DroneSize * Vector3.one;

        handRoomScaling.x = SimulationData.RoomDimensions.x / handReachCube.x;
        handRoomScaling.y = SimulationData.RoomDimensions.y / handReachCube.y;
        handRoomScaling.z = SimulationData.RoomDimensions.z / handReachCube.z;
    }
    
    void Update()
    {
        if (useController)
        {
            Debug.Log("H:" + Input.GetAxis("Horizontal"));
            Debug.Log("V:" + Input.GetAxis("Vertical"));
            Debug.Log("A:" + Input.GetAxis("Altitude"));
            Debug.Log("R:" + Input.GetAxis("Rotation"));
            Debug.Log("C:" + Input.GetAxis("Clutch"));

            float h = Input.GetAxis("Horizontal");
            float v = Input.GetAxis("Vertical");
            float a = Input.GetAxis("Altitude");

            handTarget.transform.position += Quaternion.Euler(0, inputRotation, 0) * new Vector3(h, a, v) * controllerSpeed;
            dronePositionControl.target = handTarget.transform;
        }
        else // Mocap inputs
        {
            Vector3 rawHandPosition = commandManager.GetPosition();

            // Reset referential for hand
            if (Input.GetKey(KeyCode.Mouse1))
            {
                SetHandOrigin(rawHandPosition);
            }

            // Position of the hand relative to the origin point of the "box"
            Vector3 handBoxPosition = rawHandPosition - handOrigin;

            Vector3 targetPosition = ScaleHandPosition(handBoxPosition);
            handTarget.transform.position = targetPosition; // Get position from mocap

            dronePositionControl.target = handTarget.transform;
        }

        if (drawHandTarget)
            handTarget.SetActive(true);
        else
            handTarget.SetActive(false);
    }

    private void SetHandOrigin(Vector3 origin)
    {
        // Make sure the center of the box corresponds to the center of the room
        origin.y -= handReachCube.y / 2;

        handOrigin = origin;
    }

    private Vector3 ScaleHandPosition(Vector3 handPosition)
    {
        handRoomScaling.x = SimulationData.RoomDimensions.x / handReachCube.x;
        handRoomScaling.y = SimulationData.RoomDimensions.y / handReachCube.y;
        handRoomScaling.z = SimulationData.RoomDimensions.z / handReachCube.z;

        Quaternion rotation = Quaternion.Euler(0, inputRotation, 0);
        handPosition = rotation * handPosition;
        return Vector3.Scale(handPosition, handRoomScaling);
    }
}
