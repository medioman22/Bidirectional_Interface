using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DroneCamera : MonoBehaviour
{
    public Camera fixedCamera;
    public Camera firstPersonCamera;
    public bool FPS = true;

    public void LateUpdate()
    {
        if (FPS)
        {
            fixedCamera.enabled = false;
            firstPersonCamera.enabled = true;

            // Camera position
            firstPersonCamera.transform.position = transform.position;

            // Camera angles
            firstPersonCamera.transform.rotation = Quaternion.Euler(0, transform.eulerAngles.y, 0);
        }
        else
        {
            fixedCamera.enabled = true;
            firstPersonCamera.enabled = false;
        }
    }

}