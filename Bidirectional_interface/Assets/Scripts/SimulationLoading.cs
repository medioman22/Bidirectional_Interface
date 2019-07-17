using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SimulationLoading : MonoBehaviour
{
    public HandClutchPositionControl drone;
    public GameObject subjectNamePanel;

    private DataLogger logger;

    void Start()
    {
        if (SimulationData.runNumber == 0)
        {
            // Show Name selection UI
            subjectNamePanel.SetActive(true);
        }
        else
        {
            logger = GetComponent<DataLogger>();
            logger.subjectName = SimulationData.subjectName;
            
            // Allow control of drone after 3 seconds
            StartCoroutine(WaitAndActivateDrone(SimulationData.startUpControlDelay));
        }
    }

    IEnumerator WaitAndActivateDrone(float time)
    {
        yield return new WaitForSeconds(time);

        drone.enabled = true;
    }
}
