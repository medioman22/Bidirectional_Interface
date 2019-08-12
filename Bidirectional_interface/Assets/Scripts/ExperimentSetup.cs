using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public enum expType
{
    Learning = 0,
    Haptics = 1
}

public enum hapticType
{
    ApproachX = 0,
    ApproachY = 1,
    ApproachZ = 2,
    GoThroughX = 3,
    GoThroughY = 4,
    GoThroughZ = 5,
}


public class ExperimentSetup : MonoBehaviour
{

    public expType ExperimentType;
    public hapticType HapticType;
    public bool Practice = false;

    public GameObject haptics;
    public GameObject learning;
    public GameObject drone;
    public GameObject light;

    GameObject panelX;
    GameObject panelY;
    GameObject panelZ;
    GameObject gateX;
    GameObject gateY;
    GameObject gateZ;


    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKey(KeyCode.LeftShift) && Input.GetKeyDown(KeyCode.Tab))
        {
            int eType = (int)ExperimentType;
            eType = (eType + 1) % 2;
            ExperimentType = (expType)eType;

            Debug.Log("changing scene to " + ExperimentType.ToString());
            SetupExperiment();
        }
        else if (!Input.GetKey(KeyCode.LeftShift) && Input.GetKeyDown(KeyCode.Tab))
        {
            int hType = (int)HapticType;
            hType = (hType + 1) % 6;
            HapticType = (hapticType)hType;

            Debug.Log("changing haptics scene to " + HapticType.ToString());
            SetupExperiment();
        }
    }

    public void SetupExperiment()
    {
        panelX = haptics.transform.Find("Obstacles").gameObject.transform.Find("PanelX").gameObject;
        panelY = haptics.transform.Find("Obstacles").gameObject.transform.Find("PanelY").gameObject;
        panelZ = haptics.transform.Find("Obstacles").gameObject.transform.Find("PanelZ").gameObject;
        gateX = haptics.transform.Find("Obstacles").gameObject.transform.Find("GateX").gameObject;
        gateY = haptics.transform.Find("Obstacles").gameObject.transform.Find("GateY").gameObject;
        gateZ = haptics.transform.Find("Obstacles").gameObject.transform.Find("GateZ").gameObject;

        Light lightObject = light.GetComponent<Light>();

        if (ExperimentType==expType.Learning)
        {
            lightObject.shadows = LightShadows.Soft;

            haptics.SetActive(false);
            learning.SetActive(true);
            drone.transform.position = new Vector3(-3f, 0.4f, -3f);
            drone.transform.rotation = Quaternion.Euler(0, 90, 0);
        }
        else if (ExperimentType == expType.Haptics)
        {
            lightObject.shadows = LightShadows.None;

            haptics.SetActive(true);
            learning.SetActive(false);
            drone.transform.position = new Vector3(0.0f, 0.4f, 0.0f);
            drone.transform.rotation = Quaternion.Euler(0, 90, 0);
            DeactivateAllHapticObstacles();

            GameObject is_active;

            if (HapticType == hapticType.ApproachX)
            {
                is_active = panelX;
            }
            else if (HapticType == hapticType.ApproachY)
            {
                is_active = panelY;
            }
            else if (HapticType == hapticType.ApproachZ)
            {
                is_active = panelZ;
            }
            else if (HapticType == hapticType.GoThroughX)
            {
                is_active = gateX;
            }
            else if (HapticType == hapticType.GoThroughY)
            {
                is_active = gateY;
            }
            else if (HapticType == hapticType.GoThroughZ)
            {
                is_active = gateZ;
            }
            else
            {
                is_active = panelX;
            }

            is_active.SetActive(true);
            GameObject stop = is_active.transform.Find("StopLogger").gameObject;
            if (Practice)
            {
                stop.SetActive(false);
            }
            else
            {
                stop.SetActive(true);
            }
        }
    }

    void DeactivateAllHapticObstacles()
    {
        panelX.SetActive(false);
        panelY.SetActive(false);
        panelZ.SetActive(false);
        gateX.SetActive(false);
        gateY.SetActive(false);
        gateZ.SetActive(false);
    }
}
