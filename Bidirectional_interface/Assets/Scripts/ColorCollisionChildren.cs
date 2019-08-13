using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//[RequireComponent(typeof(Collider))]
public class ColorCollisionChildren : MonoBehaviour
{
    public Material collisionMaterial;
    public Material crossedMaterial;
    public Material standardMaterial;

    public bool KeepColor = false;

    private Renderer[] rend;
    private IAmColliding[] coll;
    private IAmCrossed[] cross;

    // Start is called before the first frame update
    void Start()
    {
        rend = GetComponentsInChildren<Renderer>();
        coll = GetComponentsInChildren<IAmColliding>();
        cross = GetComponentsInChildren<IAmCrossed>();
    }

    // Update is called once per frame
    void Update()
    {
        if (!KeepColor) turnAllStandard();
        foreach (IAmCrossed i in cross)
        {
            if (i.Crossed)
            {
                turnAllGreen();
            }
        }
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

    void turnAllGreen()
    {
        foreach (Renderer i in rend)
        {
            i.material = crossedMaterial;
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
