using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MagnetConnector : MonoBehaviour
{
    public float linkDistance = 0.2f;
    public Vector3 anchor = Vector3.zero;

    private SphereCollider magnetCollider;

    // Start is called before the first frame update
    void Start()
    {
        magnetCollider = gameObject.AddComponent(typeof(SphereCollider)) as SphereCollider;
        magnetCollider.center = anchor;
        magnetCollider.radius = linkDistance;
        magnetCollider.isTrigger = true;
    }

    void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Drone")
            Debug.Log("Drone");
    }
}
