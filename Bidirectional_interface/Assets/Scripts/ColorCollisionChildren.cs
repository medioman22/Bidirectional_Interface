using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//[RequireComponent(typeof(Collider))]
public class ColorCollisionChildren : MonoBehaviour
{
    public Material collisionMaterial;
    public Material standardMaterial;

    public bool KeepRed = false;

    private Renderer[] rend;
    private IAmColliding[] coll;

    // Start is called before the first frame update
    void Start()
    {
        rend = GetComponentsInChildren<Renderer>();
        coll = GetComponentsInChildren<IAmColliding>();
    }

    // Update is called once per frame
    void Update()
    {
        if (!KeepRed) turnAllStandard();
        foreach (IAmColliding i in coll)
        {
            if (i.Colliding)
            {
                turnAllRed();
            }
        }
    }

    void turnAllRed()
    {
        foreach (Renderer i in rend)
        {
            i.material = collisionMaterial;
        }
    }

    void turnAllStandard()
    {
        foreach (Renderer i in rend)
        {
            i.material = standardMaterial;
        }
    }

    // Update is called once per frame
    void OnTriggerExit(Collider other)
    {
        if (other.tag == "Drone")
        {
            foreach (Renderer i in rend)
            {
                i.material = standardMaterial;
            }
        }
    }
}
