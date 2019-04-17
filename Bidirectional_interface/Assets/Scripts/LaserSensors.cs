using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LaserSensors : MonoBehaviour
{
    public float frontObstacle;
    public float backObstacle;
    public float upObstacle;
    public float downObstacle;
    public float leftObstacle;
    public float rightObstacle;

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
            frontObstacle = frontHit.distance;
        }
        if (Physics.Raycast(transform.position, transform.forward * -1, out backHit)) {
            backObstacle = backHit.distance;
        }
        if (Physics.Raycast(transform.position, transform.up, out upHit)) {
            upObstacle = upHit.distance;
        }
        if (Physics.Raycast(transform.position, transform.up * -1, out downHit)) {
            downObstacle = downHit.distance;
        }
        if (Physics.Raycast(transform.position, transform.right * -1, out leftHit)) {
            leftObstacle = leftHit.distance;
        }
        if (Physics.Raycast(transform.position, transform.right, out rightHit)) {
            rightObstacle = rightHit.distance;
        }
    }
}
