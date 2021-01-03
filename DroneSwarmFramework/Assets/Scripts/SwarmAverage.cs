using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SwarmAverage : MonoBehaviour
{
    //private int nbDrones;
    private Vector3 all;
    Transform avg;

    public void Start()
    {
        avg = this.transform;

        foreach (Transform t in transform)
        {
            all = t.position;
        }

        avg.position = all;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
