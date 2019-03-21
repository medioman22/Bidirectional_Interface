using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(VelocityControl))]
public class PositionControl : MonoBehaviour
{
    public Transform target;
    public bool ignoreOrientation = false;

    private VelocityControl vc;
    private Rigidbody rb;

    private float positionTimeConstant = 1.0f;
    private float yawTimeConstant = 30.0f;

    private float toleratedAnglesError = 5.0f; // 5 degrees error tolerated

    // Use this for initialization
    void Start ()
    {
        vc = GetComponent<VelocityControl>();
        rb = GetComponent<Rigidbody>();
	}
	
	void FixedUpdate ()
    {
        // Define the error in position (x,y,z)
        Vector3 positionError = target.position - transform.position;
        // Define the target orientation to face the next keypoint
        Quaternion targetOrientation = Quaternion.LookRotation(positionError);

        float yawError = targetOrientation.eulerAngles.y - transform.eulerAngles.y;

        // condition to avoid unstability when should be static on a single keypoint
        if (ignoreOrientation)
            vc.desired_yaw = 0f;
        else
            vc.desired_yaw = yawError / yawTimeConstant;

        // as the drone may not be aligned with the referential of the world, transform.
        positionError = transform.InverseTransformDirection(positionError);

        vc.desiredVx = positionError.x / positionTimeConstant;
        vc.desiredVz = positionError.z / positionTimeConstant;
        vc.desiredHeight = target.position.y;
        
    }
}
