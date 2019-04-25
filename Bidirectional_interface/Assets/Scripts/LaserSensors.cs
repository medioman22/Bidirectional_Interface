using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LaserSensors : MonoBehaviour
{
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
        allDistances = new ObstacleDistances();
    }

    // Update is called once per frame
    void Update()
    {
        RaycastHit frontHit;
        RaycastHit backHit;
        RaycastHit upHit;
        RaycastHit downHit;
        RaycastHit leftHit;
        RaycastHit rightHit;

        Debug.DrawRay(transform.position, transform.forward, Color.red);
        Debug.DrawRay(transform.position, transform.forward * -1, Color.red);
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
    }
}
