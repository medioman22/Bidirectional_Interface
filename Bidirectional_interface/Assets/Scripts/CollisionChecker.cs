using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Collider))]
public class CollisionChecker : MonoBehaviour
{
    // Call this function to know if the collider is currently in collision with anything
    public bool IsColliding
    {
        get { return collisionCount != 0; }
    }

    private int collisionCount;

    void Start()
    {
        collisionCount = 0;
    }

    private void OnCollisionEnter(Collision collision)
    {
        collisionCount++;
    }

    private void OnCollisionExit(Collision collision)
    {
        collisionCount--;

        // Sanity check
        if (collisionCount < 0)
            collisionCount = 0;
    }
}
