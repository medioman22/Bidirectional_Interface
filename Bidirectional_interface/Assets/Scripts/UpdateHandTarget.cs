﻿using System.Collections.Generic;
using System.Linq;
using UnityEngine;


public class UpdateHandTarget : MonoBehaviour
{

    const int LANDED = 0;
    const int TAKING_OFF = 1;
    const int REACHING_HEIGHT = 2;
    const int FLYING = 3;
    const int LANDING = 4;
    const int GAME_OVER = 9;

    const int GO_TO_FIRST_WAYPOINT = 5;
    const int EXTENSION = 6;
    const int WAYPOINT_NAV = 7;
    const int CONTRACTION = 8;

    public enum Feedback{Glove, Bracelets, Visual};

    public Feedback feedback;
    public bool runningExperiment = false;
    public bool useController = true;

    public float controllerSpeed = 0.0025f;
       
    public GameObject handTarget;
    public List<GameObject> allDrones;
    public List<GameObject> slaves;
    public GameObject master;

    public float K_coh = 0.3f;
    private float K_coh_lower_bound = 0.05f;
    private float K_coh_upper_bound = 0.5f;
    public float K_sep = 0.08f;
    public float K_align = 0.1f;
    public float P = 0.38f;
    public float D = 2.4f;

    [HideInInspector]
    public int droneState = LANDED;
    [HideInInspector]
    public int experimentState = TAKING_OFF;

    public float handRoomScaling = 8.0f;

    public int handRigidbodyID = 1;
    public bool drawHandTarget = true;

    public bool clutchActivated = false;

    [HideInInspector]
    public int stopAllMotors = 0;
    public float mocapInputRotation = 90.0f;

    [HideInInspector]
    [Range(0.0f, 1.0f)]
    public float Flatness =1.0f;

    [System.NonSerialized]
    public bool flying = false;
    [HideInInspector]
    public float observationInputRotation = 0.0f;

    //Value to be send to the user for feedback
    [HideInInspector]
    public float heightError = 0.0f;
    [HideInInspector]
    public Vector3 distanceToWaypoint = new Vector3(0.0f, 0.0f, 0.0f);
    [HideInInspector]
    public float extensionError = 0.0f;
    [HideInInspector]
    public float extension;

    [HideInInspector]
    public float targetExtension = 1.5f;
    [HideInInspector]
    public Vector3 nextWaypoint;

    public float experimentTime = 0.0f;
    public float firstWaypointTime = 0.0f;
    public float extensionTime = 0.0f;
    public float secondWaypointTime = 0.0f;
    public float thirdWaypointTime = 0.0f;
    public float contractionTime = 0.0f;
    public float reachingHeightTime = 0.0f;

    //This is the target to be reached during the experiment
    private float targetHeight = SimulationData.target_height;
    private float maxLandingRadius = 0.9f;
    private int currentWaypoint = 1;

    public Vector3 CenterOfMass;
    private float AccelerationMax = 0.5f;
    private bool masterExist = false;
    private float delta_K_coh = 0.01f;
    private float take_off_height = 0.50f;
    private GameObject[] droneTargets = new GameObject[5];
    private GameObject[] allWaypoints;
    private static float fullTime = 3.0f;
    private float stabilizationTime = fullTime;

    private Vector3 rawHandPosition = Vector3.zero;
    private Quaternion rawHandRotation = Quaternion.identity;
    private Vector3 oldRawHandPosition;
    private float referenceYaw = 0.0f;

    private OptitrackStreamingClient streamingClient;
    private DroneCamera cameraPosition;

    private float fixedYaw = 0.0f;


    // Start is called before the first frame update
    void Start()
    {
        handTarget = new GameObject("Hand target");

        int i = 0;
        foreach (Transform child in transform)
        {
            if (child.gameObject.tag == "Drone")
            {
                allDrones.Add(child.gameObject);
                var drone = allDrones.Last();
                if (!masterExist)
                {
                    drone.GetComponent<VelocityControl>().isSlave = false;
                    handTarget.transform.position = drone.transform.position;
                    masterExist = true;
                    master = child.gameObject;
                }
                else drone.GetComponent<VelocityControl>().isSlave = true;
                droneTargets[i] = new GameObject("drone" + i.ToString());
                droneTargets[i].transform.position = drone.transform.position;
                slaves.Add(child.gameObject);
                i += 1;
            }
        }
        allWaypoints = GameObject.FindGameObjectsWithTag("Waypoint");

        streamingClient = OptitrackStreamingClient.FindDefaultClient();

        // If we still couldn't find one, disable this component.
        if (streamingClient == null)
        {
            Debug.LogError("Streaming client not found, place a streaming client in the scene.");
        }
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        experimentTime += Time.fixedDeltaTime;
        print("real time (in updateHandTarget)" + experimentTime);
        Vector3 desiredVelocity = new Vector3(0.0f, 0.0f, 0.0f);
        CenterOfMass = AveragePosition();

        if (useController)
        {
            float h = Input.GetAxis("Horizontal");
            float v = Input.GetAxis("Vertical");
            float a = Input.GetAxis("Altitude");
            float r = Input.GetAxis("Rotation");
            Vector3 direction = new Vector3(v, a, -h);
            handTarget.transform.position += Quaternion.Euler(0, observationInputRotation, 0) * direction * controllerSpeed;
        }
        else // Mocap inputs
        {
            OptitrackRigidBodyState rgbdOptitrack = streamingClient.GetLatestRigidBodyState(handRigidbodyID);
            if (rgbdOptitrack == null)
            {
                Debug.LogError("Rigidbody not found...");
            }

            if (rgbdOptitrack != null)
            {
                rawHandPosition = rgbdOptitrack.Pose.Position;
                rawHandRotation = rgbdOptitrack.Pose.Orientation;

                Vector3 deltaHandPosition = rawHandPosition - oldRawHandPosition;
                float handYaw = rawHandRotation.eulerAngles.y;

                oldRawHandPosition = rawHandPosition;

                if (deltaHandPosition.magnitude > 1.0f)
                    return;

                //print("Raw hand position : " + rawHandPosition);

                // Update observation input rotation if FPS mode
                if (cameraPosition != null && cameraPosition.FPS)
                {
                    observationInputRotation = transform.eulerAngles.y;
                }

                // Clutch triggered, set reference yaw
                //if (OVRInput.GetUp(OVRInput.RawButton.RIndexTrigger))
                if (Input.GetMouseButton(0))
                {
                    referenceYaw = handYaw;
                }

                // In TPV, we keep the drone yaw fixed
                //if (cameraPosition != null && !cameraPosition.FPS)
                //{
                //    dronePositionControl.targetYaw = fixedYaw;
                //}

                // Clutch activated
                //if (OVRInput.Get(OVRInput.Axis1D.PrimaryIndexTrigger) < 0.5)

                //if (!OVRInput.Get(OVRInput.RawButton.RIndexTrigger))
                if (!Input.GetMouseButton(0))
                {
                    clutchActivated = true;
                    //if (cameraPosition != null && cameraPosition.FPS)
                    //    droneVelocityControl.desiredYawRate = Mathf.DeltaAngle(referenceYaw, handYaw) * rotationSpeedScaling;

                    //handTarget.transform.position = transform.position;
                }
                else
                {
                    // Update drone target
                    clutchActivated = false;

                    //if (cameraPosition != null && cameraPosition.FPS)
                    //    droneVelocityControl.desiredYawRate = 0.0f;

                    print("Delta hand position : " + deltaHandPosition);
                    handTarget.transform.position += Quaternion.Euler(0, observationInputRotation + mocapInputRotation, 0) * deltaHandPosition * handRoomScaling;
                }
            }
        }

        if (drawHandTarget)
            handTarget.SetActive(true);
        else
            handTarget.SetActive(false);

        switch (droneState)
            {
                case TAKING_OFF:
                    int i = 0;
                    foreach (GameObject drone in allDrones)
                    {
                        Vector3 t_o = new Vector3(0.0f, take_off_height, 0.0f);
                        droneTargets[i].transform.position += t_o;
                        drone.GetComponent<PositionControl>().target = droneTargets[i].transform;
                        print(drone.GetComponent<PositionControl>().target.transform.position);
                        i += 1;
                    }
                    droneState = REACHING_HEIGHT;
                    break;

                case REACHING_HEIGHT:
                //print("The height error is " + Mathf.Abs(CenterOfMass.y - take_off_height));
                
                if (Mathf.Abs(CenterOfMass.y - take_off_height) < 0.05)
                    {
                        droneState = FLYING;
                        experimentState = GO_TO_FIRST_WAYPOINT;
                        handTarget.transform.position = CenterOfMass;
                        flying = true;
                    }
                    experimentTime = 0;
                    break;

                case FLYING:

                    heightError = CenterOfMass.y - targetHeight;
                    extension = MaxRadiusOfSwarm();
                    switch (experimentState)
                    {
                        case GO_TO_FIRST_WAYPOINT:
                            if (Mathf.Abs(heightError) > 0.1 * SimulationData.max_height_error) reachingHeightTime += Time.deltaTime;
                            int index = 0;
                            for (i = 0; i < allWaypoints.Length; i++)
                            {
                                if (allWaypoints[i].GetComponent<CreateWaypoint>().waypointNumber == currentWaypoint) index = i;
                            }
                            nextWaypoint = allWaypoints[index].transform.GetChild(0).transform.position;
                            distanceToWaypoint = (nextWaypoint - CenterOfMass);
                            if (Mathf.Abs(distanceToWaypoint.x) < 0.1 * SimulationData.max_distance_error && Mathf.Abs(distanceToWaypoint.z) < 0.1 * SimulationData.max_distance_error)
                            {
                                stabilizationTime -= Time.deltaTime;
                                if (stabilizationTime < 0)
                                {
                                    currentWaypoint += 1;
                                    experimentState = EXTENSION;
                                    stabilizationTime = fullTime;
                                    firstWaypointTime = experimentTime;
                                }
                            }
                            else stabilizationTime = fullTime;
                            break;

                        case EXTENSION:
                            extensionError = targetExtension - MaxRadiusOfSwarm();
                            if (Mathf.Abs(extensionError) < 0.1f * SimulationData.max_contraction_error)
                            {
                                stabilizationTime -= Time.deltaTime;
                                if (stabilizationTime < 0)
                                {
                                    experimentState = WAYPOINT_NAV;
                                    extensionTime = experimentTime-firstWaypointTime;
                                    stabilizationTime = fullTime;
                                }
                            }
                            else stabilizationTime = fullTime;
                            break;

                        case WAYPOINT_NAV:
                        if (Mathf.Abs(heightError) > 0.1 * SimulationData.max_height_error) reachingHeightTime += Time.deltaTime;
                        if (currentWaypoint <= allWaypoints.Length)
                            {
                                index = 0;
                                for (i = 0; i < allWaypoints.Length; i++)
                                {
                                    if (allWaypoints[i].GetComponent<CreateWaypoint>().waypointNumber == currentWaypoint) index = i;
                                }
                                nextWaypoint = allWaypoints[index].transform.GetChild(0).transform.position;
                                targetHeight = nextWaypoint.y + 0.5f;
                                distanceToWaypoint = (nextWaypoint - CenterOfMass);
                                if (Mathf.Abs(distanceToWaypoint.x) < 0.1 * SimulationData.max_distance_error && Mathf.Abs(distanceToWaypoint.z) < 0.1 * SimulationData.max_distance_error)
                                {
                                    stabilizationTime -= Time.fixedDeltaTime;
                                    if (stabilizationTime < 0)
                                    {
                                        switch (currentWaypoint)
                                        {
                                            case 2:
                                                secondWaypointTime = experimentTime-extensionTime;
                                                break;
                                            case 3:
                                                thirdWaypointTime = experimentTime- secondWaypointTime;
                                                break;                                            
                                        }
                                        currentWaypoint += 1;
                                        stabilizationTime = fullTime;
                                    }
                                }
                            }
                            else
                            {
                                stabilizationTime = fullTime;
                                experimentState = CONTRACTION;
                            }
                            break;

                        case CONTRACTION:
                            Vector3 preLandingPosition = nextWaypoint;
                            preLandingPosition.y = targetHeight;
                            master.GetComponent<PositionControl>().target.position = preLandingPosition;
                            targetExtension = maxLandingRadius;
                            extensionError = targetExtension - MaxRadiusOfSwarm();
                            if (Mathf.Abs(extensionError) < 0.1 * SimulationData.max_contraction_error)
                            {
                                stabilizationTime -= Time.fixedDeltaTime;
                            if (stabilizationTime < 0)
                            {
                                experimentState = LANDING;
                                contractionTime = experimentTime - thirdWaypointTime;
                            }
                            }
                            else stabilizationTime = fullTime;
                            break;
                    }
                    //Flocking behavior
                    foreach (GameObject drone in allDrones)
                    {
                        if (!drone.GetComponent<VelocityControl>().isSlave)
                        {
                            //position control for the master
                            if (experimentState != LANDING || experimentState != CONTRACTION) drone.GetComponent<PositionControl>().target = handTarget.transform;
                        }
                        else
                        {
                            //The combination of the reynolds elements is an acceleration
                            Vector3 centerPosition;
                            if (experimentState == CONTRACTION) centerPosition = master.transform.position;
                            else centerPosition = CenterOfMass;
                            float dt = Time.fixedDeltaTime;
                            var accelerationReynolds = K_coh * Cohesion(drone, centerPosition) + K_sep * Separation(drone) + K_align * Alignement(drone);
                            var velocityReynolds = accelerationReynolds / dt;
                            desiredVelocity += velocityReynolds;

                            //Velocity control for the slaves (P D controller)
                            drone.GetComponent<VelocityControl>().desiredVelocity = P * desiredVelocity + D * accelerationReynolds;
                            Debug.DrawLine(drone.transform.position, (drone.transform.position + 5.0f * drone.transform.TransformDirection(accelerationReynolds)));
                        }
                    }
                    break;

                case LANDING:
                case GAME_OVER:
                    flying = false;
                    int j = 0;
                    foreach (GameObject drone in allDrones)
                    {
                        droneTargets[j].transform.position = drone.transform.position;
                        Vector3 landPosition = droneTargets[j].transform.position;
                        landPosition.y = -1.0f;
                        droneTargets[j].transform.position = landPosition;
                        drone.GetComponent<PositionControl>().target = droneTargets[j].transform;
                        j += 1;
                    }
                    droneState = GAME_OVER;
                    break;

                
           
        }
        if (Input.GetAxis("Mouse ScrollWheel") < 0f) K_coh += delta_K_coh;// forward
        else if (Input.GetAxis("Mouse ScrollWheel") > 0f) K_coh -= delta_K_coh; // forward
        if (K_coh < K_coh_lower_bound) K_coh = K_coh_lower_bound;
        else if (K_coh > K_coh_upper_bound) K_coh = K_coh_upper_bound;

        if (Input.GetMouseButton(1))
        {
            if (droneState == LANDED || droneState == TAKING_OFF)
            {
                droneState = TAKING_OFF;
                stopAllMotors = 0;
            }
            else if ((droneState == FLYING && experimentState ==LANDING) || droneState == LANDING) droneState = LANDING;
        }

        if (Input.GetKey(KeyCode.R))
        {
            int i = 0;
            foreach (GameObject drone in allDrones)
            {
                drone.transform.position = drone.GetComponent<PositionControl>().initialPosition;
                drone.GetComponent<PositionControl>().target.transform.position = drone.GetComponent<PositionControl>().initialPosition;
                drone.GetComponent<VelocityControl>().desiredVelocity = new Vector3(0.0f, 0.0f, 0.0f);
                droneTargets[i].transform.position = drone.transform.position;
                flying = false;
                experimentState = LANDED;
                droneState = LANDED;
                stopAllMotors = 1;
                i++;
            }
        }
    }






    Vector3 Cohesion(GameObject Drone, Vector3 centerPosition)
    {
        //In global coordinates
        Vector3 _CohesionVector = centerPosition - Drone.transform.position;
        //return in drone coordinates
        return Drone.transform.InverseTransformDirection(_CohesionVector);
    }
    Vector3 Separation(GameObject Drone)
    {
        Vector3 SeparationVector = new Vector3(0.0f, 0.0f, 0.0f);
        foreach (GameObject neighbour in allDrones)
        {
            if (neighbour.name != Drone.name)
            {
                var diff = Drone.transform.position - neighbour.transform.position;
                var difflen = diff.magnitude;
                SeparationVector += diff / (difflen * difflen);
                SeparationVector[1] *= (1 - Flatness);
            }
        }
        return Drone.transform.InverseTransformDirection(SeparationVector);
    }
    Vector3 Alignement(GameObject Drone)
    {
        Vector3 AlignementVector = new Vector3(0, 0, 0);
        AlignementVector = AverageVelocity() - Drone.GetComponent<VelocityControl>().state.VelocityVector;
        return AlignementVector;
    }
    Vector3 AveragePosition()
    {
        Vector3 Positions = new Vector3(0, 0, 0);
        foreach (GameObject drone in allDrones)
        {
            Positions += drone.transform.position;
        }
        Positions /= allDrones.Count;
        return Positions;
    }
    Vector3 AverageVelocity()
    {
        Vector3 Veloctiy = new Vector3(0, 0, 0);
        foreach (GameObject drone in allDrones)
        {
            Veloctiy += drone.GetComponent<VelocityControl>().state.VelocityVector;
        }
        Veloctiy /= allDrones.Count;
        return Veloctiy;
    }
    float MaxRadiusOfSwarm()
    {
        float maxRadius = 0.0f;
        
        Vector3 CoG = AveragePosition();
        foreach (GameObject drone in allDrones)
        {
            float radius = (drone.transform.position - CoG).magnitude;
            if (radius > maxRadius) maxRadius = radius;
        }
        return maxRadius;
    }
}
