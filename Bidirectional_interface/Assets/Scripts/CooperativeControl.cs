using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CooperativeControl : MonoBehaviour
{
    private List<MagnetConnector> connectors;

    private GameObject beamTarget;
    private GameObject[] droneTargets;

    public UDPCommandManager commandManager;

    public float handRoomScaling = 8.0f;
    [Tooltip("Change forward direction (z-axis) for mocap")]
    public float mocapInputRotation = 0.0f;
    public float observationInputRotation = 0.0f;

    public bool drawTargets = true;

    [Tooltip("Read inputs from a controller instead of motion capture.")]
    public bool useController = false;
    public float controllerSpeed = 0.025f;
    public float controllerRotationSpeed = 3.0f;
    private float yawController = 0.0f;
    private float pitchController = 0.0f;

    private Vector3 oldRawHandCentroid = Vector3.zero;

    public bool AllConnected
    {
        get 
        {
            bool detached = false;

            foreach (var connector in connectors)
            {
                // Check if any connector has no drone attached
                if (connector.ConnectedDroneController == null)
                    detached = true;
            }

            return !detached;
        }
    }

    void OnDrawGizmos()
    {
        if (!drawTargets)
            return;

        if (connectors != null)
        {
            Gizmos.color = new Color(1.0f, 0.5f, 0.0f);
            
            for (int i = 0; i < connectors.Count; i++)
            {
                Gizmos.color = new Color(1.0f, 0.5f, 0.0f);
                Gizmos.DrawCube(droneTargets[i].transform.position, Vector3.one * 0.025f);
            }
        }

        if  (beamTarget != null)
        {
            Gizmos.color = new Color(1.0f, 0.5f, 1.0f);
            Gizmos.matrix = beamTarget.transform.localToWorldMatrix;
            Gizmos.DrawCube(Vector3.zero, Vector3.one);
        }
    }
    
    void Start()
    {
        connectors = new List<MagnetConnector>(GetComponents<MagnetConnector>());

        // Instantiate hand target
        beamTarget = new GameObject("Beam Target");
        beamTarget.transform.position = transform.position;
        beamTarget.transform.rotation = transform.rotation;
        beamTarget.transform.localScale = transform.localScale;
        yawController = beamTarget.transform.rotation.eulerAngles.y;
        pitchController = beamTarget.transform.rotation.eulerAngles.x;

        droneTargets = new GameObject[connectors.Count];
        for (int i = 0; i < connectors.Count; i++)
        {
            // Instantiate target
            droneTargets[i] = new GameObject("Drone Target " + i.ToString());
            droneTargets[i].transform.position = connectors[i].AnchorPosition + Vector3.up * connectors[i].linkDistance;
        }
    }

    void FixedUpdate()
    {
        // Apply cooperative control
        if (AllConnected)
        {
            CooperativeControlCommand();
        }
        else
        {
            beamTarget.transform.position = transform.position;
            beamTarget.transform.rotation = transform.rotation;
            
            // Set targets position
            for (int i = 0; i < connectors.Count; i++)
            {
                droneTargets[i].transform.position = connectors[i].AnchorPosition + Vector3.up * connectors[i].linkDistance;

                if (connectors[i].ConnectedDroneController != null)
                {
                    connectors[i].ConnectedDroneController.target = droneTargets[i].transform;
                }
            }
        }
    }

    void CooperativeControlCommand()
    {
        if (useController)
        {
            // TODO: proper initialization of angles + view dependent tilt direction

            float h = Input.GetAxis("Horizontal");
            float v = Input.GetAxis("Vertical");
            float a = Input.GetAxis("Altitude");
            float r = Input.GetAxis("Rotation");
            float t = Input.GetAxis("Pitch");

            Vector3 direction = new Vector3(h, a, v);

            beamTarget.transform.position += Quaternion.Euler(0, observationInputRotation, 0) * direction * controllerSpeed;

            yawController += controllerRotationSpeed * r;
            pitchController += controllerRotationSpeed * t;

            pitchController = Mathf.Clamp(pitchController, -45.0f, 45.0f);

            beamTarget.transform.rotation = Quaternion.Euler(pitchController, yawController, 0.0f);

            // Set drone targets
            for (int i = 0; i < connectors.Count; i++)
            {
                droneTargets[i].transform.position = beamTarget.transform.TransformPoint(connectors[i].anchor) + Vector3.up * connectors[i].linkDistance;

                if (connectors[i].ConnectedDroneController != null)
                {
                    connectors[i].ConnectedDroneController.target = droneTargets[i].transform;
                }
            }
        }
        else // Mocap inputs
        {
            Vector3 rawRightHandPosition = commandManager.GetPosition(UDPCommandManager.TrackedTargets.RightHand);
            Vector3 rawLeftHandPosition = commandManager.GetPosition(UDPCommandManager.TrackedTargets.LeftHand);

            Quaternion handsRotation = Quaternion.FromToRotation(Vector3.left, rawLeftHandPosition - rawRightHandPosition);
            float yaw = handsRotation.eulerAngles.y;
            float pitch = handsRotation.eulerAngles.x;

            Vector3 rawHandCentroid = 0.5f * (rawLeftHandPosition + rawRightHandPosition);

            Vector3 deltaHandCentroid = rawHandCentroid - oldRawHandCentroid;

            oldRawHandCentroid = rawHandCentroid;

            // Ignore too large displacements (noise)
            if (deltaHandCentroid.magnitude > 1.0f)
                return;

            // Clutch triggered, stop drones there
            if (Input.GetKeyDown(KeyCode.Mouse0))
            {
                // Stop target at current position
                beamTarget.transform.position = transform.position;

                // Set drone targets
                for (int i = 0; i < connectors.Count; i++)
                {
                    droneTargets[i].transform.position = beamTarget.transform.TransformPoint(connectors[i].anchor) + Vector3.up * connectors[i].linkDistance;

                    if (connectors[i].ConnectedDroneController != null)
                    {
                        connectors[i].ConnectedDroneController.target = droneTargets[i].transform;
                    }
                }
            }

            // Clutch not activated
            if (!Input.GetKey(KeyCode.Mouse0))
            {
                // Update beam target
                beamTarget.transform.position += Quaternion.Euler(0, observationInputRotation + mocapInputRotation, 0) * deltaHandCentroid * handRoomScaling;
                beamTarget.transform.rotation = Quaternion.Euler(pitch, yaw, 0.0f);

                // Set drone targets
                for (int i = 0; i < connectors.Count; i++)
                {
                    droneTargets[i].transform.position = beamTarget.transform.TransformPoint(connectors[i].anchor) + Vector3.up * connectors[i].linkDistance;

                    if (connectors[i].ConnectedDroneController != null)
                    {
                        connectors[i].ConnectedDroneController.target = droneTargets[i].transform;
                    }
                }
            }
        }
    }
}
