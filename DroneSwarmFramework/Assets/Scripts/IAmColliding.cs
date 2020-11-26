using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class IAmColliding : MonoBehaviour
{
    public bool Colliding;

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Drone")
        {
            Colliding = true;
        }
    }

    // Update is called once per frame
    void OnTriggerExit(Collider other)
    {
        if (other.tag == "Drone")
        {
            Colliding = false;
        }
    }
}
