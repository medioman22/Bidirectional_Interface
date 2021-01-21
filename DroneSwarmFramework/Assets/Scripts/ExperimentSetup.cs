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
    Maze1 = 0,
    Maze2 = 1,
    Maze3 = 2,
    Maze4 = 3,
    Maze5 = 4,
    Maze6 = 5,
    Maze7 = 6,
    Maze8 = 7,
}


public class ExperimentSetup : MonoBehaviour
{

    public expType ExperimentType;
    public hapticType HapticType;
    public bool Practice = false;

    public GameObject haptics;
    public GameObject learning;
    public GameObject drone;

    GameObject Maze1;
    GameObject Maze2;
    GameObject Maze3;
    GameObject Maze4;
    GameObject Maze5;
    GameObject Maze6;
    GameObject Maze7;
    GameObject Maze8;
    //GameObject Playground;


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
        Maze1 = haptics.transform.Find("Mazes").gameObject.transform.Find("Maze1").gameObject; ; //.gameObject.transform.Find("PanelX").gameObject;
        Maze2 = haptics.transform.Find("Mazes").gameObject.transform.Find("Maze2").gameObject;
        Maze3 = haptics.transform.Find("Mazes").gameObject.transform.Find("Maze3").gameObject;
        Maze4 = haptics.transform.Find("Mazes").gameObject.transform.Find("Maze4").gameObject;
        Maze5 = haptics.transform.Find("Mazes").gameObject.transform.Find("Maze5").gameObject;
        Maze6 = haptics.transform.Find("Mazes").gameObject.transform.Find("Maze6").gameObject;
        Maze7 = haptics.transform.Find("Mazes").gameObject.transform.Find("Maze7").gameObject;
        Maze8 = haptics.transform.Find("Mazes").gameObject.transform.Find("Maze8").gameObject;
        //Playground = learning.transform.Find("Playground").gameObject;


        if (ExperimentType==expType.Learning)
        {
            haptics.SetActive(false);
            learning.SetActive(true);
        }
        else if (ExperimentType == expType.Haptics)
        {
            haptics.SetActive(true);
            learning.SetActive(false);
            DeactivateAllHapticObstacles();

            GameObject is_active;

            if (HapticType == hapticType.Maze1)
            {
                is_active = Maze1;
            }
            else if (HapticType == hapticType.Maze2)
            {
                is_active = Maze2;
            }
            else if (HapticType == hapticType.Maze3)
            {
                is_active = Maze3;
            }
            else if (HapticType == hapticType.Maze4)
            {
                is_active = Maze4;
            }
            else if (HapticType == hapticType.Maze5)
            {
                is_active = Maze5;
            }
            else if (HapticType == hapticType.Maze6)
            {
                is_active = Maze6;
            }
            else if (HapticType == hapticType.Maze7)
            {
                is_active = Maze7;
            }
            else if (HapticType == hapticType.Maze8)
            {
                is_active = Maze8;
            }
            else
                is_active = Maze1;

            is_active.SetActive(true);

            // Turn off color change if practising
            //ColorCollisionChildren col = is_active.GetComponent<ColorCollisionChildren>();
            //if (Practice)
            //{
            //    col.KeepColor = false;
            //}
            //else
            //{
            //    col.KeepColor = true;
            //}   
        }
    }

    void DeactivateAllHapticObstacles()
    {
        Maze1.SetActive(false);
        Maze2.SetActive(false);
        Maze3.SetActive(false);
        Maze4.SetActive(false);
        Maze5.SetActive(false);
        Maze6.SetActive(false);
        Maze7.SetActive(false);
        Maze8.SetActive(false);
    }
}
