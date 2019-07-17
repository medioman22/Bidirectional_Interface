using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SubjectNameUI : MonoBehaviour
{
    public GameObject subjectNamePanel;
    public InputField subjectNameField; 
    public Button validateButton;
    public Text invalidNameText;

    public HandClutchPositionControl drone;
    public DataLogger logger;

    // Start is called before the first frame update
    void Start()
    {
        validateButton.onClick.AddListener(OnValidateButtonPressed);
    }

    void OnValidateButtonPressed()
    {
        string name = subjectNameField.text;

        if (CheckIfValidName(name))
        {
            invalidNameText.gameObject.SetActive(false);
            SimulationData.subjectName = name;
            logger.subjectName = name;

            StartCoroutine(WaitAndActivateDrone(SimulationData.startUpControlDelay));
            subjectNamePanel.SetActive(false);
            // // Reload Scene
            // Scene scene = SceneManager.GetActiveScene(); 
            // SceneManager.LoadScene(scene.name);
        }
        else
        {
            invalidNameText.gameObject.SetActive(true);
        }
    }

    bool CheckIfValidName(string name)
    {
        if (string.IsNullOrWhiteSpace(name))
            return false;

        if (name.Contains(" ") || name.Contains(".") || name.Contains("/")
         || name.Contains("-") || name.Contains("%") || name.Contains("+"))
            return false;

        return true;
    }

    IEnumerator WaitAndActivateDrone(float time)
    {
        yield return new WaitForSeconds(time);

        drone.enabled = true;
    }
}
