using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LaserSensors : MonoBehaviour
{
    private DroneCamera cameraPosition;
    private HandClutchPositionControl posControl;

    [System.Serializable]
    public class ObstacleDistances
    {
        public float frontObstacle;
        public float backObstacle;
        public float upObstacle;
        public float downObstacle;
        public float leftObstacle;
        public float rightObstacle;
    }

    public ObstacleDistances allDistances;

    void Start()
    {
        cameraPosition = GetComponent<DroneCamera>();
        posControl = GetComponent<HandClutchPositionControl>();
        allDistances = new ObstacleDistances();
    }

    // Update is called once per frame
    void Update()
    {
        float theta;

        RaycastHit frontHit;
        RaycastHit backHit;
        RaycastHit upHit;
        RaycastHit downHit;
        RaycastHit leftHit;
        RaycastHit rightHit;

        float tempRight;
        float tempLeft;
        float tempFront;
        float tempBack;

        Debug.DrawRay(transform.position, transform.forward * 0.5f, Color.red);
        Debug.DrawRay(transform.position, transform.forward * -0.5f, Color.red);
        Debug.DrawRay(transform.position, transform.up, Color.red);
        Debug.DrawRay(transform.position, transform.up * -1, Color.red);
        Debug.DrawRay(transform.position, transform.right * -1, Color.red);
        Debug.DrawRay(transform.position, transform.right, Color.red);

        if (Physics.Raycast(transform.position, transform.forward, out frontHit)) {
            allDistances.frontObstacle = frontHit.distance;
        }
        if (Physics.Raycast(transform.position, transform.forward * -1, out backHit)) {
            allDistances.backObstacle = backHit.distance;
        }
        if (Physics.Raycast(transform.position, transform.up, out upHit)) {
            allDistances.upObstacle = upHit.distance;
        }
        if (Physics.Raycast(transform.position, transform.up * -1, out downHit)) {
            allDistances.downObstacle = downHit.distance;
        }
        if (Physics.Raycast(transform.position, transform.right * -1, out leftHit)) {
            allDistances.leftObstacle = leftHit.distance;
        }
        if (Physics.Raycast(transform.position, transform.right, out rightHit)) {
            allDistances.rightObstacle = rightHit.distance;
        }

        /*
        // if in TPV, observator frame for feedback.
        if (!cameraPosition.FPS)
        {
            // angle between the observer angle (which is rotated by observationinputrotation with respect to unity frame) and the drone angle.
            theta = Mathf.DeltaAngle(posControl.observationInputRotation, transform.eulerAngles.y);

            // project the measured distance to represent the true distance with respect to the angle of observation
            if(theta > -45 && theta < 45)
            {
                allDistances.frontObstacle *= Mathf.Abs(Mathf.Cos(theta * Mathf.PI / 180));
                allDistances.rightObstacle *= Mathf.Abs(Mathf.Cos(theta * Mathf.PI / 180));
                allDistances.leftObstacle *= Mathf.Abs(Mathf.Cos(theta * Mathf.PI / 180));
                allDistances.backObstacle *= Mathf.Abs(Mathf.Cos(theta * Mathf.PI / 180));
            }
            else if (theta > -135 && theta < -45)
            {
                // to have right angles for projection
                theta += 90;

                tempFront = Mathf.Abs(Mathf.Cos(theta * Mathf.PI / 180)) * allDistances.rightObstacle;
                tempRight = Mathf.Abs(Mathf.Cos(theta * Mathf.PI / 180)) * allDistances.backObstacle;
                tempLeft = Mathf.Abs(Mathf.Cos(theta * Mathf.PI / 180)) * allDistances.frontObstacle;
                tempBack = Mathf.Abs(Mathf.Cos(theta * Mathf.PI / 180)) * allDistances.leftObstacle;

                allDistances.frontObstacle = tempFront;
                allDistances.backObstacle = tempBack;
                allDistances.leftObstacle = tempLeft;
                allDistances.rightObstacle = tempRight;
            }
            else if (theta > 45 && theta < 135)
            {
                // to have right angles for projection
                theta -= 90;

                tempFront = Mathf.Abs(Mathf.Cos(theta * Mathf.PI / 180)) * allDistances.leftObstacle;
                tempRight = Mathf.Abs(Mathf.Cos(theta * Mathf.PI / 180)) * allDistances.frontObstacle;
                tempLeft = Mathf.Abs(Mathf.Cos(theta * Mathf.PI / 180)) * allDistances.backObstacle;
                tempBack = Mathf.Abs(Mathf.Cos(theta * Mathf.PI / 180)) * allDistances.rightObstacle;

                allDistances.frontObstacle = tempFront;
                allDistances.backObstacle = tempBack;
                allDistances.leftObstacle = tempLeft;
                allDistances.rightObstacle = tempRight;
            }
            else if (Mathf.Abs(theta) > 135)
            {
                tempFront = Mathf.Abs(Mathf.Cos(theta * Mathf.PI / 180)) * allDistances.backObstacle;
                tempRight = Mathf.Abs(Mathf.Cos(theta * Mathf.PI / 180)) * allDistances.leftObstacle;
                tempLeft = Mathf.Abs(Mathf.Cos(theta * Mathf.PI / 180)) * allDistances.rightObstacle;
                tempBack = Mathf.Abs(Mathf.Cos(theta * Mathf.PI / 180)) * allDistances.frontObstacle;

                allDistances.frontObstacle = tempFront;
                allDistances.backObstacle = tempBack;
                allDistances.leftObstacle = tempLeft;
                allDistances.rightObstacle = tempRight;
            }
        }
        */
    }
}
