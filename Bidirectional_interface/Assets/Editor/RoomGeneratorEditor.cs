using UnityEngine;
using UnityEditor;

/// <summary>
/// Custom inspector for RoomGenerator script, to add the "Generate button".
/// </summary>
[CustomEditor(typeof(RoomGenerator))]
public class RoomGeneratorEditor : Editor
{
    public override void OnInspectorGUI()
    {
        DrawDefaultInspector();

        RoomGenerator myScript = (RoomGenerator)target;
        if (GUILayout.Button("Generate"))
        {
            myScript.GenerateRoom();
        }
    }
}
