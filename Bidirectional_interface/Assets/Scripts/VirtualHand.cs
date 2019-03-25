using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VirtualHand : MonoBehaviour
{
    public Vector3 handReachCube = 0.5f * Vector3.one;

    private Vector3 handDisplacement = Vector3.zero;

    public Vector3 GetHandPosition()
    {
        Vector3 position = handDisplacement;
        position.y += handReachCube.y / 2.0f;
        return position;
    }
    
    void Update()
    {
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");
        float a = Input.GetAxis("Altitude");

        float x = h * handReachCube.x / 2.0f;
        float y = a * handReachCube.y / 2.0f;
        float z = v * handReachCube.z / 2.0f;

        handDisplacement = new Vector3(x, y, z);
    }

    // Draw hand reach and hand position in Scene view
    void OnDrawGizmos()
    {
        Gizmos.DrawWireCube(transform.position, handReachCube);
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(transform.position + handDisplacement, 0.1f);
    }
}
