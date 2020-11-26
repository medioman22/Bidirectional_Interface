using UnityEngine;
using UnityEditor;

/// <summary>
/// Custom inspector for RoomGenerator script, to add the "Generate button".
/// </summary>
[CustomEditor(typeof(ExperimentSetup))]
public class ExperimentSetupEditor : Editor
{
    public override void OnInspectorGUI()
    {
        DrawDefaultInspector();

        ExperimentSetup myScript = (ExperimentSetup)target;
        if (GUILayout.Button("Setup Experiment"))
        {
            myScript.SetupExperiment();
        }
    }
}
