using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
[RequireComponent(typeof(CooperativeControl))]
public class MagnetConnector : MonoBehaviour
{
    public float linkDistance = 0.2f;
    public Vector3 anchor = Vector3.zero;

    private Rigidbody rgbd;
    private CooperativeControl controller;

    private SphereCollider magnetCollider;
    private SpringJoint joint;
    private bool connected = false;
    private HandClutchPositionControl connectedMocapController;
    private PositionControl _connectedDroneController;

    public PositionControl ConnectedDroneController
    {
        get 
        {
            return _connectedDroneController;
        }
    }

    public Vector3 AnchorPosition
    {
        get
        {
            return transform.TransformPoint(anchor);
        }
    }

    // Start is called before the first frame update
    void Start()
    {
        rgbd = GetComponent<Rigidbody>();
        controller = GetComponent<CooperativeControl>();

        magnetCollider = gameObject.AddComponent(typeof(SphereCollider)) as SphereCollider;
        magnetCollider.center = anchor;
        magnetCollider.radius = linkDistance;
        magnetCollider.isTrigger = true;
    }

    void Update()
    {
        // Check if joint is broken
        if (joint == null)
        {
            connected = false;

            // Enable mocap control if previously attached to a drone
            if (connectedMocapController != null)
            {
                connectedMocapController.enabled = true;
                connectedMocapController = null;
                _connectedDroneController = null;
            }
        }
    }

    void OnDrawGizmos()
    {
        Gizmos.color = Color.green;
        Gizmos.DrawCube(transform.TransformPoint(anchor), Vector3.one * 0.025f);
    }

    void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Drone")
        {
            if (!connected)
            {
                if (CreateLink(other.gameObject))
                    connected = true;
                else
                    connected = false;
            }
        }
    }

    // Creates a spring joint between this object and the colliding drone, if the drone has no joint yet
    // Return true if successful
    bool CreateLink(GameObject drone)
    {
        // Check if drone already connected
        if (drone.GetComponent<SpringJoint>() != null)
        {
            return false;
        }

        // Created link
        joint = drone.AddComponent(typeof(SpringJoint)) as SpringJoint;
        joint.autoConfigureConnectedAnchor = false;
        joint.connectedBody = rgbd;
        joint.connectedAnchor = anchor;
        joint.spring = 100f;
        joint.damper = 100f;
        joint.maxDistance = 0.2f;
        joint.tolerance = 0.01f;
        joint.breakForce = 2f;

        // Disable mocap control
        connectedMocapController = drone.GetComponent<HandClutchPositionControl>();
        connectedMocapController.enabled = false;
        _connectedDroneController = drone.GetComponent<PositionControl>();

        return true;
    }
}
