using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//[RequireComponent(typeof(Collider))]
public class ColorCollision : MonoBehaviour
{
    public Material collisionMaterial;
    public Material standardMaterial;

    public bool KeepRed = false;

    private Renderer rend;
    // Start is called before the first frame update
    void Start()
    {
        rend = GetComponent<Renderer>();
    }

    // Update is called once per frame
    void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Drone")
        {
            rend.material = collisionMaterial;
        }
    }

    // Update is called once per frame
    void OnTriggerExit(Collider other)
    {
        if (!KeepRed)
        {
            if (other.tag == "Drone")
            {
                rend.material = standardMaterial;
            }
        }
    }
}
