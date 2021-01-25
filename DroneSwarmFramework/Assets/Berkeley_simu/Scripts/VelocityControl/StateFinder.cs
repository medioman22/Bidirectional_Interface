using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class StateFinder : MonoBehaviour {
//	public float Pitch; // The current pitch for the given transform in radians
//	public float Roll; // The current roll for the given transform in radians
//	public float Yaw; // The current Yaw for the given transform in degrees
	public float Altitude; // The current altitude from the zero position
	public Vector3 Angles;
	public Vector3 VelocityVector; // Velocity vector
	public Vector3 AngularVelocityVector; // Angular Velocity
	public Vector3 Inertia;
	public float Mass;

	private VelocityControl vc;
    private Transform vcTranform;
    private Rigidbody vcRigidbody;

    void Start()
    {
        vc = GetComponent<VelocityControl>();
        vcTranform = vc.transform;
        vcRigidbody = vc.GetComponent<Rigidbody>();
    }

    public void GetState()
    {
        Vector3 worldDown = vc.transform.InverseTransformDirection(Vector3.down);
        float Pitch = worldDown.z; // Small angle approximation
        float Roll = -worldDown.x; // Small angle approximation
        float Yaw = Mathf.Rad2Deg * vc.transform.rotation.y;
        Angles = new Vector3(Pitch, Yaw, Roll);
        //Debug.Log("Angles: " + Angles);

        Altitude = vc.transform.position.y;

		VelocityVector = vcRigidbody.velocity;
		VelocityVector = vcTranform.InverseTransformDirection(VelocityVector);

		AngularVelocityVector = vcRigidbody.angularVelocity;
		AngularVelocityVector = vcTranform.InverseTransformDirection(AngularVelocityVector);

		Inertia = vcRigidbody.inertiaTensor;
        Mass = vcRigidbody.mass;
	}

}
