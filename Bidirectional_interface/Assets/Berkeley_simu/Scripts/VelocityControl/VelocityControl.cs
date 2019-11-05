using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(StateFinder))]
public class VelocityControl : MonoBehaviour {

    public StateFinder state;

    public GameObject propFL;
    public GameObject propFR;
    public GameObject propRR;
    public GameObject propRL;
    public bool isSlave = true;

    public Vector3 desiredTheta;


    private float gravity = Physics.gravity.magnitude;
    private float time_constant_y_velocity = 1.0f; // Normal-person coordinates
    public float time_constant_acceleration = 0.5f;
    private float time_constant_omega_xz_rate = 0.1f; // Normal-person coordinates (roll/pitch)
    private float time_constant_alpha_xz_rate = 0.05f; // Normal-person coordinates (roll/pitch)
    private float time_constant_alpha_y_rate = 0.05f; // Normal-person coordinates (yaw)

    private float max_pitch = 0.175f; // 10 Degrees in radians, otherwise small-angle approximation dies 
    private float max_roll = 0.175f; // 10 Degrees in radians, otherwise small-angle approximation dies
    private float max_alpha = 10.0f;

    private float max_thrust = 2.0f * Physics.gravity.magnitude;

    //must set this
    public float desiredHeight = 2.0f;
    public float desiredVx = 0.0f;
    public float desiredVz = 0.0f;
    public float desiredYawRate = 0.0f;
    public Vector3 desiredVelocity = new Vector3 (0.0f, 0.0f, 0.0f);
    public Vector3 desiredAcceleration = new Vector3(0.0f, 0.0f, 0.0f);
    private float speedScale = 500.0f; // for propeller animation (graphic only)

    private Rigidbody rb;

    // Use this for initialization
    void Start ()
    {
        state = GetComponent<StateFinder>();
        rb = GetComponent<Rigidbody> ();
        //desiredHeight = state.Altitude;
    }

    // Update is called once per frame
    void FixedUpdate ()
    {
        if (Input.GetKeyDown("space")) isSlave = !isSlave;
            state.GetState ();
        
        // NOTE: I'm using stupid vector order (sideways, up, forward) at the end

        Vector3 desiredOmega;

        float heightError = state.Altitude - desiredHeight;


        if (!isSlave || !this.transform.parent.GetComponent<UpdateHandTarget>().flying) desiredVelocity = new Vector3(desiredVx, -heightError / time_constant_y_velocity, desiredVz);
       
        Vector3 velocityError = state.VelocityVector - desiredVelocity;
        
        desiredAcceleration = -velocityError / time_constant_acceleration;
        
        // pitch is rotation about x-axis, thus it corresponds to an acceleration in z, similarly for roll
        desiredTheta = new Vector3 (desiredAcceleration.z / gravity, 0.0f, -desiredAcceleration.x / gravity);
        desiredTheta.x = Mathf.Clamp(desiredTheta.x, -max_pitch, max_pitch);
        desiredTheta.z = Mathf.Clamp(desiredTheta.z, -max_roll, max_roll);

        // Angular error
        Vector3 thetaError = state.Angles - desiredTheta;

        // Angular velocities
        desiredOmega = -thetaError / time_constant_omega_xz_rate;
        desiredOmega.y = desiredYawRate;

        Vector3 omegaError = state.AngularVelocityVector - desiredOmega;

        // Angular acceleration
        Vector3 desiredAlpha = Vector3.Scale(omegaError, new Vector3(-1.0f/time_constant_alpha_xz_rate, -1.0f/time_constant_alpha_y_rate, -1.0f/time_constant_alpha_xz_rate));
        // Clamp all angles between [-max_alpha; max_alpha]
        desiredAlpha = Vector3.Min (desiredAlpha, Vector3.one * max_alpha);
        desiredAlpha = Vector3.Max (desiredAlpha, -Vector3.one * max_alpha);

        float desiredThrust = (Physics.gravity.magnitude + desiredAcceleration.y) / (Mathf.Cos (state.Angles.z) * Mathf.Cos (state.Angles.x));
        desiredThrust = Mathf.Clamp(desiredThrust, 0.0f, max_thrust);

        Vector3 desiredTorque = Vector3.Scale (desiredAlpha, state.Inertia);
        Vector3 desiredForce = new Vector3 (0.0f, desiredThrust, 0.0f);

        rb.AddRelativeTorque (desiredTorque, ForceMode.Force);
        rb.AddRelativeForce (desiredForce , ForceMode.Force);

        //prop transforms
        propFL.transform.Rotate(Vector3.forward * Time.deltaTime * desiredThrust * speedScale);
        propFR.transform.Rotate(Vector3.forward * Time.deltaTime * desiredThrust * speedScale);
        propRR.transform.Rotate(Vector3.forward * Time.deltaTime * desiredThrust * speedScale);
        propRL.transform.Rotate(Vector3.forward * Time.deltaTime * desiredThrust * speedScale);

      }
    public void Reset()
    {
        state.VelocityVector = Vector3.zero;
        state.AngularVelocityVector = Vector3.zero;

        desiredVx = 0.0f;
        desiredVz = 0.0f;
        desiredYawRate = 0.0f;

        enabled = true;
    }
}
