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

    [Range(0.0f, 1.0f)]
    public float Flatness;

    [System.NonSerialized]
    public bool flying = false;

    static int LANDED = 0;
    static int TAKING_OFF = 1;
    static int FLYING = 2;
    static int LANDING  = 3;


    private Vector3 CenterOfMass;
    private float AccelerationMax = 0.5f;
    private bool masterExist = false;
    private float delta_K_coh = 0.01f;
    private float droneState = LANDED;
    private float take_off_height = 1.0f;

    // Start is called before the first frame update
    void Start()
    {
        handTarget = new GameObject("Hand target");
        foreach (Transform child in transform)
        {
            if (child.gameObject.tag == "Drone")
            {   
                allDrones.Add(child.gameObject);
                var drone = allDrones.Last();
                if (!masterExist)
                {
                    drone.GetComponent<VelocityControl>().isSlave = false;
                    handTarget.transform.position = drone.transform.position;// + new Vector3(0.0f , 1.0f, 0.0f);
                    masterExist = true;
                }
                else drone.GetComponent<VelocityControl>().isSlave = true;
            }

        }
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        CenterOfMass = AveragePosition();
        if (useController)
        {
            float h = Input.GetAxis("Horizontal");
            float v = Input.GetAxis("Vertical");
            float a = Input.GetAxis("Altitude");
            float r = Input.GetAxis("Rotation");
            Vector3 desiredVelocity = new Vector3 (0.0f,0.0f,0.0f);
     
            Vector3 direction = new Vector3(h, a, v);

            //handTarget.transform.position += Quaternion.Euler(0, observationInputRotation, 0) * direction * controllerSpeed;
            foreach (GameObject drone in allDrones)
            {
                if (droneState == TAKING_OFF)
                {
                    //drone.GetComponent<PositionControl>().target = handTarget.transform;
                    Vector3 takeOffPosition = drone.transform.position;
                    takeOffPosition.y = take_off_height;
                    drone.GetComponent<PositionControl>().target.position = takeOffPosition;

                    Vector3 CoG = AveragePosition();
                    if (Mathf.Abs(CoG.y - take_off_height) < 0.05)
                    {
                        droneState = FLYING;
                        handTarget.transform.position = CoG;
                        flying = true;
                    }

                }

                else if (droneState == FLYING)
                {
                    if (!drone.GetComponent<VelocityControl>().isSlave)
                    {
                        //position control for the master
                        drone.GetComponent<PositionControl>().target = handTarget.transform;
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
                else if (droneState == LANDING)
                {
                }
            }
        }
        if (Input.GetKeyUp(KeyCode.M))
            if (Flatness + 0.05 >= 1) Flatness = 1;
            else Flatness += 0.05f;
        if (Input.GetKeyUp(KeyCode.N))
            if (Flatness - 0.05 <= 0) Flatness = 0;
        else Flatness -= 0.05f;


        if (Input.GetAxis("Mouse ScrollWheel") > 0f) // forward
        {
            K_coh += delta_K_coh;
        }
        else if (Input.GetAxis("Mouse ScrollWheel") < 0f) // forward
        {
            K_coh -= delta_K_coh;
        }

        if (Input.GetKeyDown(KeyCode.Mouse1))
        {
            if (droneState == LANDED || droneState == TAKING_OFF)
            {
                droneState = TAKING_OFF;
            }
            else if (droneState == FLYING)
            {
                droneState = LANDING;
            }
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
                var diff = Drone.transform.position- neighbour.transform.position;
                var difflen = diff.magnitude;
                SeparationVector += diff / (difflen*difflen);
                SeparationVector[1] *= (1-Flatness) ;
            }
        }
        return  Drone.transform.InverseTransformDirection(SeparationVector);
    }
    Vector3 Alignement(GameObject Drone)
    {
        Vector3 AlignementVector = new Vector3(0, 0, 0);
       AlignementVector = AverageVelocity() - Drone.GetComponent<VelocityControl>().state.VelocityVector;
       return AlignementVector;
    }

    Vector3 AveragePosition()
    {
        Vector3 Positions = new Vector3 (0,0,0);
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
}
    