using System.Collections.Generic;
using UnityEngine;
using System.Linq;
using System.Text;
using System.IO;
using System;


public class UpdateHandTarget : MonoBehaviour
{
    public float controllerSpeed = 0.025f;
    public float observationInputRotation = 0.0f;
    public bool useController = true;
    public GameObject handTarget;
    public List<GameObject> allDrones;

    public float K_coh = 0.2f;
    public float K_sep = 0.08f;
    public float K_align = 0.1f;
    public float P = 0.38f;
    public float D = 2.4f;
    public int droneState = LANDED;
    public int experimentState = LANDED;

    public float handRoomScaling = 8.0f;

    //This is the target height to be reached during the experiment
    public float desiredHeight = 1.0f;
    public float maxLandingRadius = 1.0f;
    public float minExtensionForExp = 2.0f;
    public float marginFromCenterOfWaypoint = 0.5f;

    public int handRigidbodyID = 1;
    public bool drawHandTarget = true;

    public bool clutchActivated = false;

    public float mocapInputRotation = 90.0f;


    [Range(0.0f, 1.0f)]
    public float Flatness =1.0f;

    [System.NonSerialized]
    public bool flying = false;


    //Value to be send to the user for feedback
    public float heightError = SimulationData.heightError;
    public Vector3 distanceToWaypoint = SimulationData.distanceToWaypoint;
    public float extensionError = SimulationData.extensionError;
    public float contractionError = SimulationData.contractionError;

    const int LANDED = 0;
    const int TAKING_OFF = 1;
    const int REACHING_HEIGHT = 2;
    const int FLYING = 3;
    const int LANDING = 4;

    const int GO_TO_FIRST_WAYPOINT = 5;
    const int EXTENSION = 6;
    const int WAYPOINT_NAV = 7;
    const int CONTRACTION = 8;

    private Vector3 CenterOfMass;
    private float AccelerationMax = 0.5f;
    private bool masterExist = false;
    private float delta_K_coh = 0.01f;
    private float take_off_height = 1.0f;
    private GameObject[] droneTargets = new GameObject[5];
    private GameObject[] allWaypoints;
    private Vector3 nextWaypoint;
    private int currentWaypoint = 1;

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
                }
                else drone.GetComponent<VelocityControl>().isSlave = true;
                droneTargets[i] = new GameObject("drone" + i.ToString());
                droneTargets[i].transform.position = drone.transform.position;
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
        Vector3 desiredVelocity = new Vector3(0.0f, 0.0f, 0.0f);
        CenterOfMass = AveragePosition();

        if (useController)
        {
            float h = Input.GetAxis("Horizontal");
            float v = Input.GetAxis("Vertical");
            float a = Input.GetAxis("Altitude");
            float r = Input.GetAxis("Rotation");
            Vector3 direction = new Vector3(h, a, v);
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
                if (Input.GetKeyDown(KeyCode.Mouse0))
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
                if (!Input.GetKey(KeyCode.Mouse0))
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
                    i += 1;
                }
                droneState = REACHING_HEIGHT;
                break;

            case REACHING_HEIGHT:
                //print("The height error is " + Mathf.Abs(CenterOfMass.y - take_off_height));
                if (Mathf.Abs(CenterOfMass.y - take_off_height) < 0.05)
                {
                    droneState = FLYING;
                    experimentState = REACHING_HEIGHT;
                    handTarget.transform.position = CenterOfMass;
                    flying = true;
                }
                break;

            case FLYING:
                switch (experimentState)
                {
                    case REACHING_HEIGHT:
                        heightError = Mathf.Abs(CenterOfMass.y - desiredHeight);
                        //print("The height error is " + heightError);
                        if (heightError < 0.05) experimentState = GO_TO_FIRST_WAYPOINT;
                        break;

                    case GO_TO_FIRST_WAYPOINT:
                        int index = 0;
                        for (i = 0; i < allWaypoints.Length; i++)
                        {
                            if (allWaypoints[i].GetComponent<CreateWaypoint>().waypointNumber == currentWaypoint) index = i;
                        }
                        nextWaypoint = allWaypoints[index].transform.GetChild(0).transform.position;
                        distanceToWaypoint = (nextWaypoint - CenterOfMass);
                        //print("The distance to next waypoint is " + distanceToWaypoint.magnitude);
                        if (distanceToWaypoint.magnitude < marginFromCenterOfWaypoint)
                        {
                            currentWaypoint += 1;
                            experimentState = EXTENSION;
                        }
                        break;

                    case EXTENSION:
                        float extension = AverageDistanceToNeighbour();
                        extensionError = minExtensionForExp - extension;
                        //print("The extension is " + extension);
                        if (extensionError < 0) experimentState = WAYPOINT_NAV;
                        break;

                    case WAYPOINT_NAV:
                        if (currentWaypoint <= allWaypoints.Length)
                        {
                            index = 0;
                            for (i = 0; i < allWaypoints.Length; i++)
                            {
                                if (allWaypoints[i].GetComponent<CreateWaypoint>().waypointNumber == currentWaypoint) index = i;
                            }
                            nextWaypoint = allWaypoints[index].transform.GetChild(0).transform.position;
                            distanceToWaypoint = (nextWaypoint - CenterOfMass);
                            //print("The distance to next waypoint is " + distanceToWaypoint.magnitude);
                            if (distanceToWaypoint.magnitude < marginFromCenterOfWaypoint) currentWaypoint += 1;
                        }
                        else experimentState = CONTRACTION;
                        break;

                    case CONTRACTION:
                        //print("MaxRadius is " + MaxRadiusOfSwarm());
                        contractionError = maxLandingRadius - MaxRadiusOfSwarm();
                        if (contractionError > 0) experimentState = LANDING;
                        break;
                }

                //Flocking behavior
                foreach (GameObject drone in allDrones)
                {
                    if (!drone.GetComponent<VelocityControl>().isSlave)
                    {
                        //position control for the master
                        if (experimentState != LANDING) drone.GetComponent<PositionControl>().target = handTarget.transform;
                        else drone.GetComponent<PositionControl>().target.position = AveragePosition();
                    }
                    else
                    {
                        //The combination of the reynolds elements is an acceleration
                        var dt = Time.fixedDeltaTime;
                        var accelerationReynolds = K_coh * Cohesion(drone) + K_sep * Separation(drone) + K_align * Alignement(drone);
                        var velocityReynolds = accelerationReynolds / dt;
                        desiredVelocity += velocityReynolds;

                        //Velocity control for the slaves (P D controller)
                        drone.GetComponent<VelocityControl>().desiredVelocity = P * desiredVelocity + D * accelerationReynolds;
                        Debug.DrawLine(drone.transform.position, (drone.transform.position + 5.0f * drone.transform.TransformDirection(accelerationReynolds)));
                    }
                }
                break;

            case LANDING:
                flying = false;
                int j = 0;
                foreach (GameObject drone in allDrones)
                {
                    droneTargets[j].transform.position = drone.transform.position;
                    Vector3 landPosition = droneTargets[j].transform.position;
                    landPosition.y = 0.0f;
                    droneTargets[j].transform.position = landPosition;
                    drone.GetComponent<PositionControl>().target = droneTargets[j].transform;
                    j += 1;
                }
                droneState = LANDED;
                break;
        }

        if (Input.GetAxis("Mouse ScrollWheel") > 0f) K_coh += delta_K_coh;// forward
        else if (Input.GetAxis("Mouse ScrollWheel") < 0f) K_coh -= delta_K_coh; // forward

        if (Input.GetKeyDown(KeyCode.Mouse1))
        {
            if (droneState == LANDED || droneState == TAKING_OFF) droneState = TAKING_OFF;
            else if ((droneState == FLYING && experimentState ==LANDING) || droneState == LANDING) droneState = LANDING;
        }
    }

    Vector3 Cohesion(GameObject Drone)
    {
        //In global coordinates
        Vector3 _CohesionVector = CenterOfMass - Drone.transform.position;
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

    float AverageDistanceToNeighbour()
    {
        float extension = 0.0f;
        float averageExtension = 0.0f;
        foreach (GameObject drone in allDrones)
        {
            foreach (GameObject neighbour in allDrones)
            {
                if (neighbour.name != drone.name)
                {
                    var diff = drone.transform.position - neighbour.transform.position;
                    var difflen = diff.magnitude;
                    extension += difflen;
                }
            }
            averageExtension /= (allDrones.Count() - 1);
            averageExtension += extension;
            extension = 0.0f;
        }
        averageExtension /= (allDrones.Count() - 1);
        return averageExtension;
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
