using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(StateFinder))]
public class VelocityControl : MonoBehaviour
{
    private StateFinder state;
    private StateFinder refState;
    private Rigidbody rb;
    private LeapInputUDP leap;

    private float gravity = Physics.gravity.magnitude;
    private float time_constant_y_velocity = 1.0f; // Normal-person coordinates
    private float time_constant_acceleration = 0.5f;
    private float time_constant_omega_xz_rate = 0.1f; // Normal-person coordinates (roll/pitch)
    private float time_constant_alpha_xz_rate = 0.05f; // Normal-person coordinates (roll/pitch)
    private float time_constant_alpha_y_rate = 0.05f; // Normal-person coordinates (yaw)

    private float max_pitch = 0.175f; // 10 Degrees in radians, otherwise small-angle approximation dies 
    private float max_roll = 0.175f; // 10 Degrees in radians, otherwise small-angle approximation dies
    private float max_alpha = 10.0f;

    private float max_thrust = 2.0f * Physics.gravity.magnitude;

    private Vector3 offset = new Vector3();

    // For flocking behavior
    [Header("Flocking Behavior")]
    public float leap_scale_factor = 1;
    [SerializeField] private float K_sep; 
    public float K_coh;
    public float K_align;
    public bool is_Slave;
    private float min_inter_distance = 0.1f;

    public GameObject masterDrone;
    public Transform swarm;

    private float flatness = 1.0f;
    private float P = 6.0f;
    private float D = 0.0f;

    // Velocity and other state attributes
    [Header("State")]
    public float desiredHeight = 0.0f;
    public float desiredVx = 0.0f;
    public float desiredVy = 0.0f;
    public float desiredVz = 0.0f;
    public float desiredYawRate = 0.0f;

    [Header("Animation")]
    public GameObject propFL;
    public GameObject propFR;
    public GameObject propRR;
    public GameObject propRL;
    private float speedScale = 500.0f; // for propeller animation (graphic only)

    // Use this for initialization
    void Start()
    {
        state = GetComponent<StateFinder>();
        rb = GetComponent<Rigidbody>();
        leap = masterDrone.GetComponent<LeapInputUDP>();
        offset = rb.transform.position;
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        state.GetState();

        //Debug.Log(this.gameObject.name + "at position: " + rb.transform.position);

        if (is_Slave)
        {
            // Get spread from Leap input
            float closeness = 1 - leap.spread; // 0: far apart, 1: close together
            K_sep = Mathf.Max(closeness, min_inter_distance)*leap_scale_factor; 

            // Get Master reference
            refState = masterDrone.GetComponent<StateFinder>();
            refState.GetState();

            Vector3 masterVelocity = refState.VelocityVector;
            Vector3 masterPosition = masterDrone.transform.position;

            Vector3 centerOfMass = masterPosition;
            float dt = Time.fixedDeltaTime;
            var drone = state.gameObject;
            var accelerationReynolds = K_coh * Cohesion(drone, masterPosition) + K_sep * Separation(drone) + K_align * Alignement(state, masterVelocity);

            Vector3 velocityReynolds = P * accelerationReynolds * dt + D * accelerationReynolds;
            desiredVx += velocityReynolds[0];
            desiredVz += velocityReynolds[2];
            desiredVy += velocityReynolds[1];
        }

        CalculateForces();
    }

    void CalculateForces()
    {
        // NOTE: I'm using stupid vector order (sideways, up, forward) at the end
        Vector3 desiredTheta;
        Vector3 desiredOmega;

        float heightError = state.Altitude - desiredHeight;

        Vector3 desiredVelocity = new Vector3(desiredVx, -heightError / time_constant_y_velocity, desiredVz);
        Vector3 velocityError = state.VelocityVector - desiredVelocity;

        Vector3 desiredAcceleration = -velocityError / time_constant_acceleration;

        // pitch is rotation about x-axis, thus it corresponds to an acceleration in z, similarly for roll
        desiredTheta = new Vector3(desiredAcceleration.z / gravity, 0.0f, -desiredAcceleration.x / gravity);
        desiredTheta.x = Mathf.Clamp(desiredTheta.x, -max_pitch, max_pitch);
        desiredTheta.z = Mathf.Clamp(desiredTheta.z, -max_roll, max_roll);

        // Angular error
        Vector3 thetaError = state.Angles - desiredTheta;

        // Angular velocities
        desiredOmega = -thetaError / time_constant_omega_xz_rate;
        desiredOmega.y = desiredYawRate;

        Vector3 omegaError = state.AngularVelocityVector - desiredOmega;

        // Angular acceleration
        Vector3 desiredAlpha = Vector3.Scale(omegaError, new Vector3(-1.0f / time_constant_alpha_xz_rate, -1.0f / time_constant_alpha_y_rate, -1.0f / time_constant_alpha_xz_rate));
        // Clamp all angles between [-max_alpha; max_alpha]
        desiredAlpha = Vector3.Min(desiredAlpha, Vector3.one * max_alpha);
        desiredAlpha = Vector3.Max(desiredAlpha, -Vector3.one * max_alpha);

        float desiredThrust = (Physics.gravity.magnitude + desiredAcceleration.y) / (Mathf.Cos(state.Angles.z) * Mathf.Cos(state.Angles.x));
        desiredThrust = Mathf.Clamp(desiredThrust, 0.0f, max_thrust);

        Vector3 desiredTorque = Vector3.Scale(desiredAlpha, state.Inertia);
        Vector3 desiredForce = new Vector3(0.0f, desiredThrust, 0.0f);

        rb.AddRelativeTorque(desiredTorque, ForceMode.Force);
        rb.AddRelativeForce(desiredForce, ForceMode.Force);

        //prop transforms
        propFL.transform.Rotate(Vector3.forward * Time.deltaTime * desiredThrust * speedScale);
        propFR.transform.Rotate(Vector3.forward * Time.deltaTime * desiredThrust * speedScale);
        propRR.transform.Rotate(Vector3.forward * Time.deltaTime * desiredThrust * speedScale);
        propRL.transform.Rotate(Vector3.forward * Time.deltaTime * desiredThrust * speedScale);
    }

    // Reynold's Flocking algorithm
    Vector3 Cohesion(GameObject Drone, Vector3 centerPosition)
    {
        //In global coordinates
        Vector3 _CohesionVector = centerPosition - Drone.transform.position;
        return Drone.transform.InverseTransformDirection(_CohesionVector);
    }

    Vector3 Separation(GameObject Drone)
    {
        Vector3 SeparationVector = new Vector3(0.0f, 0.0f, 0.0f);
        foreach (Transform child in swarm)
        {
            if (child.gameObject.name == masterDrone.name)
                continue;

            if (child.gameObject.name != Drone.name)
            {
                var diff = Drone.transform.position - child.position;
                var difflen = diff.magnitude;
                SeparationVector += diff / (difflen * difflen);
                SeparationVector[1] *= (1 - flatness);
            }
        }
        return Drone.transform.InverseTransformDirection(SeparationVector);
    }

    Vector3 Alignement(StateFinder state, Vector3 averageVelocity)
    {
        Vector3 AlignementVector = new Vector3(0, 0, 0);
        AlignementVector = averageVelocity - state.VelocityVector;
        return AlignementVector;
    }
}