using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class UpdateHandTarget : MonoBehaviour
{
    public float controllerSpeed = 0.025f;
    public float observationInputRotation = 0.0f;
    public bool useController = true;
    public GameObject handTarget;
    public List<GameObject> allDrones;
    public float K_coh = 0.2f;
    public float K_sep = 0.08f;
    public float P = 0.38f;
    public float D = 2.4f;

    private Vector3 CenterOfMass;
    private float AccelerationMax = 0.5f;

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
                if (drone.name == "Master")
                {
                    drone.GetComponent<VelocityControl>().isSlave = false;
                    handTarget.transform.position = drone.transform.position;
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

            handTarget.transform.position += Quaternion.Euler(0, observationInputRotation, 0) * direction * controllerSpeed;
            foreach (GameObject drone in allDrones)
            {
      
                if (drone.name == "Master")
                {
                    //position control for the master
                    drone.GetComponent<PositionControl>().target = handTarget.transform;
                }
                else
                {
                    //The combination of the reynolds elements is an acceleration
                    var dt = Time.fixedDeltaTime;
                    var accelerationReynolds = K_coh* Cohesion(drone) + K_sep* Separation(drone);
                    var velocityReynolds = accelerationReynolds / dt;
                    desiredVelocity += velocityReynolds;

                    //accelerationReynolds = Vector3.Max(accelerationReynolds,  - AccelerationMax*Vector3.one);
                    //accelerationReynolds = Vector3.Min(accelerationReynolds,  AccelerationMax*Vector3.one);

                    //Velocity control for the slaves (P D controller)
                    drone.GetComponent<VelocityControl>().desiredVelocity = P* desiredVelocity + D* accelerationReynolds ;
                    Debug.DrawLine(drone.transform.position, (drone.transform.position + 5.0f*drone.transform.TransformDirection(accelerationReynolds)));
                }
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
            }
        }
        return  Drone.transform.InverseTransformDirection(SeparationVector);
    }
    Vector3 Alignement()
    {
        Vector3 AlignementVector = new Vector3(0, 0, 0);
        foreach (GameObject drone in allDrones)
        {
            AlignementVector += (handTarget.transform.position - drone.GetComponent<PositionControl>().transform.position) / (handTarget.transform.position - drone.GetComponent<PositionControl>().transform.position).magnitude;
        }
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
}
