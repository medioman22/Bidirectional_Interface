using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(VelocityControl))]
public class PositionControl : MonoBehaviour
{
    public Transform target;

    [Tooltip("Specify if the drone rotates.")]
    public bool ignoreOrientation = false;

    [Tooltip("If this value is set, the drone will try to be oriented towards this target. (ignoreOrientation must be set to false)")]
    public Transform lookAtTarget;

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

        if (ignoreOrientation)
        {
            // Drone does not rotate
            vc.desired_yaw = 0f;
        }
        else
        {
            Quaternion targetOrientation = transform.rotation;

            // Follow target for orientation
            if (lookAtTarget != null)
            {
                
            }
            // Otherwise orient the drone towards position target
            else
            {
                // Avoid exception thrown if positionError = 0;
                if (positionError.magnitude > 0.01f)
                {
                    // Define the target orientation to face the next keypoint
                    targetOrientation = Quaternion.LookRotation(positionError);
                }

                float yawError = Mathf.DeltaAngle(transform.eulerAngles.y, targetOrientation.eulerAngles.y);
                vc.desired_yaw = yawError / yawTimeConstant;
            }
        }

        // as the drone may not be aligned with the referential of the world, transform.
        positionError = transform.InverseTransformDirection(positionError);

        vc.desiredVx = positionError.x / positionTimeConstant + dFactor * (positionError.x - lastPositionError.x) / Time.fixedDeltaTime;
        vc.desiredVz = positionError.z / positionTimeConstant + dFactor * (positionError.z - lastPositionError.z) / Time.fixedDeltaTime; ;
        vc.desiredHeight = target.position.y;

        lastPositionError = positionError;
    }
}

        if (ignoreOrientation)
        {
            // Drone does not rotate
            vc.desired_yaw = 0f;
        }

        // as the drone may not be aligned with the referential of the world, transform.
        positionError = transform.InverseTransformDirection(positionError);

        vc.desiredVx = positionError.x / positionTimeConstant + dFactor * (positionError.x - lastPositionError.x) / Time.fixedDeltaTime;
        vc.desiredVz = positionError.z / positionTimeConstant + dFactor * (positionError.z - lastPositionError.z) / Time.fixedDeltaTime; ;
        vc.desiredHeight = target.position.y;

        lastPositionError = positionError;