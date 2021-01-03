using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SubjectNameUI : MonoBehaviour
{
    public GameObject subjectNamePanel;
    public InputField subjectNameField; 
    public Button validateButton;
    public Toggle useControllerToggle;
    public Text invalidNameText;
    public Text goLabel;

    public InputManager drone;
    public DataLogger logger;

    // Start is called before the first frame update
    void Start()
    {
        validateButton.onClick.AddListener(OnValidateButtonPressed);
    }

    void Update()
    {
        if (subjectNamePanel.activeSelf)
        {
            // Refocus the UI if no element is selected
            if (UnityEngine.EventSystems.EventSystem.current.currentSelectedGameObject == null)
                subjectNameField.Select();
        }
    }

    void OnValidateButtonPressed()
    {
        string name = subjectNameField.text;

        if (CheckIfValidName(name))
        {
            invalidNameText.gameObject.SetActive(false);
            SimulationData.subjectName = name;
            logger.subjectName = name;

            drone.useController = useControllerToggle.isOn;
            SimulationData.useController = useControllerToggle.isOn;
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
