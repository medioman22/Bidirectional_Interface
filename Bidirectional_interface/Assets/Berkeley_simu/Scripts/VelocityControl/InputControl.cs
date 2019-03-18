using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(VelocityControl))]
public class InputControl : MonoBehaviour
{
    public Transform target;

    private VelocityControl vc;
    private Rigidbody rb;

    private float positionTimeConstant = 1.0f;

	// Use this for initialization
	void Start ()
    {
        vc = GetComponent<VelocityControl>();
        rb = GetComponent<Rigidbody>();
	}
	
	void FixedUpdate ()
    {
        Vector3 positionError = target.position - transform.position;

        vc.desiredVx = positionError.x / positionTimeConstant;
        vc.desiredVz = positionError.z / positionTimeConstant;
        vc.desiredHeight = target.position.y;
    }
}
