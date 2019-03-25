using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VirtualHandClutch : MonoBehaviour
{
    public Vector3 handReachCube = 0.5f * Vector3.one;

    [Range(0, 1)]
    public float handInputScaling = 0.5f;

    private Vector3 handDisplacement = Vector3.zero;
    private Vector3 handClutchOffset = Vector3.zero;

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

        float x = h * handReachCube.x / 2.0f * handInputScaling;
        float y = a * handReachCube.y / 2.0f * handInputScaling;
        float z = v * handReachCube.z / 2.0f * handInputScaling;

        // Clutch
        if (Input.GetKey(KeyCode.Space))
        {
            handClutchOffset = handDisplacement;
            Input.ResetInputAxes();
        }
        else
        {
            handDisplacement = handClutchOffset + new Vector3(x, y, z);

            handDisplacement.x = Mathf.Clamp(handDisplacement.x, -0.5f * handReachCube.x, 0.5f * handReachCube.x);
            handDisplacement.y = Mathf.Clamp(handDisplacement.y, -0.5f * handReachCube.y, 0.5f * handReachCube.y);
            handDisplacement.z = Mathf.Clamp(handDisplacement.z, -0.5f * handReachCube.z, 0.5f * handReachCube.z);
        }
    }

    // Draw hand reach and hand position in Scene view
    void OnDrawGizmos()
    {
        if (!isActiveAndEnabled)
            return;

        Gizmos.color = Color.black;
        Gizmos.DrawWireCube(transform.position, handReachCube);
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireCube(transform.position + handClutchOffset, handReachCube * handInputScaling);
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(transform.position + handDisplacement, 0.05f);
    }
}
