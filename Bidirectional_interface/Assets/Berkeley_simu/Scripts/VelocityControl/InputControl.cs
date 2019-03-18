using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Thomas je pense que le contrôle en position tu pourras directement l'implémenter ici.
/// </summary>

[RequireComponent(typeof(VelocityControl))]
public class InputControl : MonoBehaviour {

	private VelocityControl vc;

	private float abs_height = 1;

	// Use this for initialization
	void Start () {
        vc = GetComponent<VelocityControl>();
	}
	
	// Update is called once per frame

	void FixedUpdate () {
//		vc.desiredVx = Input.GetAxisRaw ("Pitch")*4.0f;
//		vc.desired_vy = Input.GetAxisRaw ("Roll")*4.0f;
//		vc.desired_yaw = Input.GetAxisRaw ("Yaw")*0.5f;
//		abs_height += Input.GetAxisRaw("Throttle") * 0.1f;
//
//		vc.desired_height = abs_height;
	}
}
