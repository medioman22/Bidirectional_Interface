using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RoomGenerator : MonoBehaviour
{
    public float xDimension = 8;
    public float yDimension = 6;
    public float zDimension = 8;

    public float wallThickness = 0.2f;

    public Material wallMaterial;

    /// <summary>
    /// Call this function to generate the room of the adequate dimensions.
    /// This function will be called when the "Generate" button is clicked in the
    /// custom inspector (defined in RoomGeneratorEditor.cs).
    /// </summary>
    public void GenerateRoom()
    {
        // TODO: apply tags ?
        // apply right materials

        // Root object
        GameObject room = new GameObject("Room");

        // Ground
        GameObject ground = GameObject.CreatePrimitive(PrimitiveType.Cube);
        ground.name = "Ground";
        ground.transform.localScale = new Vector3(xDimension, wallThickness, zDimension);
        ground.transform.position = new Vector3(0, -wallThickness / 2, 0);
        ground.transform.parent = room.transform;

        // Wall (back in x-axis)
        GameObject wall1 = GameObject.CreatePrimitive(PrimitiveType.Cube);
        wall1.name = "Wall 1";
        wall1.transform.localScale = new Vector3(yDimension, wallThickness, zDimension);
        wall1.transform.position = new Vector3(-xDimension / 2 - wallThickness / 2, yDimension / 2, 0);
        wall1.transform.rotation = Quaternion.Euler(0, 0, 90);
        wall1.transform.parent = room.transform;
        wall1.GetComponent<Renderer>().material = wallMaterial;

        // Wall (front in z-axis)
        GameObject wall2 = GameObject.CreatePrimitive(PrimitiveType.Cube);
        wall2.name = "Wall 2";
        wall2.transform.localScale = new Vector3(xDimension, wallThickness, yDimension);
        wall2.transform.position = new Vector3(0, yDimension / 2, zDimension / 2 + wallThickness / 2);
        wall2.transform.rotation = Quaternion.Euler(90, 0, 0);
        wall2.transform.parent = room.transform;
        wall2.GetComponent<Renderer>().material = wallMaterial;

        // Wall (front in x-axis)
        GameObject wall3 = GameObject.CreatePrimitive(PrimitiveType.Cube);
        wall3.name = "Wall 3";
        wall3.transform.localScale = new Vector3(yDimension, wallThickness, zDimension);
        wall3.transform.position = new Vector3(xDimension / 2 + wallThickness / 2, yDimension / 2, 0);
        wall3.transform.rotation = Quaternion.Euler(0, 0, 90);
        wall3.transform.parent = room.transform;
        wall3.GetComponent<Renderer>().material = wallMaterial;

        // Wall (back in z-axis)
        GameObject wall4 = GameObject.CreatePrimitive(PrimitiveType.Cube);
        wall4.name = "Wall 4";
        wall4.transform.localScale = new Vector3(xDimension, wallThickness, yDimension);
        wall4.transform.position = new Vector3(0, yDimension / 2, -zDimension / 2 - wallThickness / 2);
        wall4.transform.rotation = Quaternion.Euler(90, 0, 0);
        wall4.transform.parent = room.transform;
        wall4.GetComponent<Renderer>().material = wallMaterial;

        // Ceiling
        GameObject ceiling = GameObject.CreatePrimitive(PrimitiveType.Cube);
        ceiling.name = "Ceiling";
        ceiling.transform.localScale = new Vector3(xDimension, wallThickness, zDimension);
        ceiling.transform.position = new Vector3(0, yDimension + wallThickness / 2, 0);
        ceiling.transform.parent = room.transform;
        ceiling.GetComponent<Renderer>().material = wallMaterial;

    }
}
