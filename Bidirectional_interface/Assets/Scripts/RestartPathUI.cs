using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class RestartPathUI : MonoBehaviour
{
    public GameObject restartPathPanel;
    public Button restartButton;
    public Button quitButton;
    public DataLogger logger;

    // Start is called before the first frame update
    void Start()
    {
        restartButton.onClick.AddListener(OnRestartButtonPressed);
        quitButton.onClick.AddListener(OnQuitButtonPressed);
    }

    void OnRestartButtonPressed()
    {
            restartPathPanel.SetActive(false);
            logger.SaveResults();

            // Reload Scene
            SimulationData.runNumber++;
            Scene scene = SceneManager.GetActiveScene(); 
            SceneManager.LoadScene(scene.name);
    }

    void OnQuitButtonPressed()
    {
        restartPathPanel.SetActive(false);

        // Logs will be save uppon quitting in any case

#if UNITY_EDITOR
        // Application.Quit() does not work in the editor so
        // UnityEditor.EditorApplication.isPlaying need to be set to false to end the game
        UnityEditor.EditorApplication.isPlaying = false;
#else
         Application.Quit();
#endif
    }
}
