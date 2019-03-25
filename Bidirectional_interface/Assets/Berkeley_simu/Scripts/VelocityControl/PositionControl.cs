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
    private float dFactor = 0.1f;
    private float yawTimeConstant = 30.0f;

    private Vector3 lastPositionError = Vector3.zero;

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
        Quaternion targetOrientation = transform.rotation;

        // Avoid exception thrown if positionError = 0;
        if (positionError.magnitude > 0.01f)
        {
            // Define the target orientation to face the next keypoint
            targetOrientation = Quaternion.LookRotation(positionError);
        }

        float yawError = Mathf.DeltaAngle(transform.eulerAngles.y,targetOrientation.eulerAngles.y);

        // condition to avoid unstability when should be static on a single keypoint
        if (ignoreOrientation)
            vc.desired_yaw = 0f;
        else
            vc.desired_yaw = yawError / yawTimeConstant;

        // as the drone may not be aligned with the referential of the world, transform.
        positionError = transform.InverseTransformDirection(positionError);

        vc.desiredVx = positionError.x / positionTimeConstant + dFactor * (positionError.x - lastPositionError.x) / Time.fixedDeltaTime;
        vc.desiredVz = positionError.z / positionTimeConstant + dFactor * (positionError.z - lastPositionError.z) / Time.fixedDeltaTime; ;
        vc.desiredHeight = target.position.y;

        lastPositionError = positionError;
    }
}
