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
            if (HapticType == hapticType.ApproachX)
            {
                panelX.SetActive(true);
            }
            else if (HapticType == hapticType.ApproachX)
            {
                panelX.SetActive(true);
            }
            else if (HapticType == hapticType.ApproachY)
            {
                panelY.SetActive(true);
            }
            else if (HapticType == hapticType.ApproachZ)
            {
                panelZ.SetActive(true);
            }
            else if (HapticType == hapticType.GoThroughX)
            {
                gateX.SetActive(true);
            }
            else if (HapticType == hapticType.GoThroughY)
            {
                gateY.SetActive(true);
            }
            else if (HapticType == hapticType.GoThroughZ)
            {
                gateZ.SetActive(true);
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
