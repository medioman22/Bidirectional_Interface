using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SimulationLoading : MonoBehaviour
{
    public HandClutchPositionControl drone;
    public GameObject subjectNamePanel;
    public GameObject restartPathPanel;
    public Text goLabel;

    private DataLogger logger;

    void Start()
    {
        restartPathPanel.SetActive(false);

        if (SimulationData.runNumber == 0)
        {
            // Show Name selection UI
            subjectNamePanel.SetActive(true);
        }
        else
        {
            subjectNamePanel.SetActive(false);
            logger = GetComponent<DataLogger>();
            logger.subjectName = SimulationData.subjectName;
            
            // Allow control of drone after 3 seconds
            drone.useController = SimulationData.useController;
            StartCoroutine(WaitAndActivateDrone(SimulationData.startUpControlDelay));
        }
    }

    IEnumerator WaitAndActivateDrone(float time)
    {
        yield return new WaitForSeconds(time);
        drone.enabled = true;
        StartCoroutine(AnimateGoLabel(1.0f));
    }

    IEnumerator AnimateGoLabel(float duration)
    {
        float dt = 1.0f / 25.0f;
        int steps = (int)(duration / dt);
        int fadeInStep = (int)(steps * 0.75f);

        goLabel.gameObject.SetActive(true);

        for (int i = 0; i < steps; i++)
        {
            if (i < fadeInStep)
            {
                Color color = goLabel.color;
                color.a = Mathf.Lerp(0.0f, 1.0f, (float)i / (float)fadeInStep);
                goLabel.color = color;
                yield return new WaitForSeconds(dt);
            }
            else
            {
                Color color = goLabel.color;
                color.a = Mathf.Lerp(1.0f, 0.0f, (float)(i - fadeInStep) / (float)(steps - fadeInStep));
                goLabel.color = color;
                yield return new WaitForSeconds(dt);
            }
        }
        
        goLabel.gameObject.SetActive(false);
    }
}
