using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SimulationLoading : MonoBehaviour
{
    public GameObject subjectNamePanel;
    public GameObject restartPathPanel;

    public Text goLabel;

    private DataLogger logger;

    void Start()
    {
        GameObject swarm = GameObject.Find("Swarm");
        bool experiment = swarm.GetComponent<UpdateHandTarget>().runningExperiment;
        if (experiment)
        {
            // Show Name selection UI
            subjectNamePanel.SetActive(true);
        }
    }

}
