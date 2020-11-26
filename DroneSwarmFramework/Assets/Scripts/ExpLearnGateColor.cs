using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//[RequireComponent(typeof(Collider))]
public class ExpLearnGateColor : MonoBehaviour
{
    public Material collidedMaterial;
    public Material standardMaterial;
    public Material crossedMaterial;
    public Material crossedCollidedMaterial;

    private Renderer[] rend;
    private IAmColliding[] coll;
    private IAmCrossed[] cross;

    private bool collided = false;
    private bool crossed = false;

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
        foreach (IAmColliding i in coll)
        {
            if (i.Colliding)
            {
                collided = true;
            }
        }
        foreach (IAmCrossed i in cross)
        {
            if (i.Crossed)
            {
                crossed = true;
            }
        }
        UpdateColor();
    }

    void UpdateColor()
    {
        if (crossed && collided)
        {
            turnAllBlue();
        }
        else if (crossed)
        {
            turnAllGreen();
        }
        else if (collided)
        {
            turnAllRed();
        }
    }

    void turnAllRed()
    {
        foreach (Renderer i in rend)
        {
            i.material = collidedMaterial;
        }
    }

    void turnAllGreen()
    {
        foreach (Renderer i in rend)
        {
            i.material = crossedMaterial;
        }
    }

    void turnAllBlue()
    {
        foreach (Renderer i in rend)
        {
            i.material = crossedCollidedMaterial;
        }
    }
}
