using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraPosition : MonoBehaviour
{
    public Camera Camera;
    public bool FPS = true;

    private Vector3 cameraOffset = new Vector3(0.0f, -0.1f, 0.5f);

    public void LateUpdate()
    {
        if (FPS)
        {
            // Camera position
            Camera.transform.position = transform.position;

            // Camera angles
            Camera.transform.rotation = transform.rotation;
        }
        else
        {
            // Camera position
            Camera.transform.position = transform.TransformDirection(transform.InverseTransformDirection(transform.position) - cameraOffset);
            // Camera angles
            Camera.transform.eulerAngles = transform.eulerAngles;
        }
    }

}