using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;


public class updateUI : MonoBehaviour
{
    public int test = 0;
    public Text information;
    public Image horizontal_arrow;
    public Image vertical_arrow;
    public Image contract_arrow;
    public Image extens_arrow1;
    public Image extens_arrow2;

    private Vector2 distToWaypoint;
    private float heightError;
    private float contraction_error;

    private float lengthContractionArrow;
    private float lengthExtensionArrow;
    private float lengthhorizArrow;
    private float lengthvertArrow;

    private float angle;
    private GameObject swarm;
    private float displayedValue;
    private int experimentState;
    private string vertDirection = "up";
    private IDictionary<string, Vector3> arrowDirection = new Dictionary<string, Vector3>();


    const int LANDED = 0;
    const int TAKING_OFF = 1;
    const int REACHING_HEIGHT = 2;
    const int FLYING = 3;
    const int LANDING = 4;

    const int GO_TO_FIRST_WAYPOINT = 5;
    const int EXTENSION = 6;
    const int WAYPOINT_NAV = 7;
    const int CONTRACTION = 8;
    Vector3 arrowDirect = new Vector3(0, 0, 0);
    public Quaternion testRotation;

    // Start is called before the first frame update
    void Start()
    {
        information = gameObject.GetComponentInChildren<Text>();
        horizontal_arrow = GameObject.Find("Horizontal arrow").GetComponent<Image>();
        vertical_arrow = GameObject.Find("Vertical arrow").GetComponent<Image>();
        contract_arrow = GameObject.Find("Contract").GetComponent<Image>();
        extens_arrow1 = GameObject.Find("Extract1").GetComponent<Image>();
        extens_arrow2 = GameObject.Find("Extract2").GetComponent<Image>();

        extens_arrow1.enabled = true;
        extens_arrow2.enabled = true;
        contract_arrow.enabled = true;

        swarm = GameObject.Find("Swarm");
        arrowDirection.Add("up", new Vector3(0f, 90f, 0f));
        arrowDirection.Add("down", new Vector3(0f, 90f, 180.0f));
    }

    // Update is called once per frame
    void Update()
    {
        UpdateHandTarget updHandTarget = swarm.GetComponent<UpdateHandTarget>();
        experimentState = swarm.GetComponent<UpdateHandTarget>().experimentState;

        distToWaypoint = new Vector2(updHandTarget.distanceToWaypoint.x, updHandTarget.distanceToWaypoint.z);
        heightError = updHandTarget.heightError;
        contraction_error = updHandTarget.extensionError;

        if (heightError <= 0) vertDirection = "up";
        else vertDirection = "down";

        if (updHandTarget.experiment)
        {
            switch (experimentState)
            {
                case GO_TO_FIRST_WAYPOINT:
                case WAYPOINT_NAV:
                    lengthContractionArrow = 0;
                    lengthExtensionArrow = 0;
                    lengthvertArrow = lengthOfHeightArrow();
                    if (Mathf.Abs(lengthvertArrow) > 0) lengthhorizArrow = 0;
                    else lengthhorizArrow = lengthOfDistArrow();
                    break;

                case EXTENSION:
                case CONTRACTION:
                    if (Mathf.Abs(contraction_error) > 0.1 * SimulationData.max_contraction_error)
                    {
                        if (contraction_error < 0)
                        {
                            lengthContractionArrow = lengthOfContractionArrow();
                            lengthExtensionArrow = 0;
                        }
                        else if (contraction_error > 0)
                        {
                            lengthContractionArrow = 0;
                            lengthExtensionArrow = lengthOfContractionArrow();
                        }
                    }
                    else
                    {
                        lengthContractionArrow = 0;
                        lengthExtensionArrow = 0;
                    }

                    lengthhorizArrow = 0;
                    lengthvertArrow = 0;
                    break;

                case LANDING:
                    lengthContractionArrow = 0;
                    lengthExtensionArrow = 0;
                    lengthhorizArrow = 0;
                    lengthvertArrow = 0;
                    information.text = "LAND";
                    break;
            }


            vertical_arrow.rectTransform.localScale = new Vector3(1.0f, lengthvertArrow, 1.0f);
            vertical_arrow.rectTransform.rotation = Quaternion.Euler(arrowDirection[vertDirection]);

            angle = 90.0f + Vector2.SignedAngle(distToWaypoint, new Vector2(10.0f, 0.0f));
            horizontal_arrow.rectTransform.rotation = Quaternion.Euler(new Vector3(90.0f, angle, 0.0f));
            horizontal_arrow.rectTransform.localScale = new Vector3(1.0f, lengthhorizArrow, 1.0f);

            extens_arrow1.rectTransform.localScale = new Vector3(lengthExtensionArrow, lengthExtensionArrow, 1.0f);
            extens_arrow2.rectTransform.localScale = new Vector3(lengthExtensionArrow, lengthExtensionArrow, 1.0f);
            contract_arrow.rectTransform.localScale = new Vector3(lengthContractionArrow, lengthContractionArrow, 1.0f);
        }
        else
        {
            horizontal_arrow.enabled = false;
            vertical_arrow.enabled = false;
            extens_arrow1.enabled = false;
            extens_arrow2.enabled = false;
            contract_arrow.enabled = false;
            float timeRemaining = 60 - Time.time;
            if (timeRemaining <= 0)
            {
                timeRemaining = 0;
            }
            information.text = "Time remaining :" + timeRemaining.ToString("F2") + " s";
        }
    }

    float lengthOfDistArrow()
    {
        float length = 0.0f;
        float distance = distToWaypoint.magnitude;
        length = distance / SimulationData.max_distance_error * 1;
        if (length > 1) length = 1;
        if (distance < 0.1 * SimulationData.max_distance_error) length = 0;
        return length;
    }
    float lengthOfHeightArrow()
    {
        float length = 0.0f;
        length = Mathf.Abs(heightError) / SimulationData.max_height_error * 1;
        if (length > 1) length = 1;
        if (Mathf.Abs(heightError) < 0.1 * SimulationData.max_height_error) length = 0;
        return length;
    }

    float lengthOfContractionArrow()
    {
        float length = 0.0f;
        length = contraction_error / SimulationData.max_contraction_error * 1;
        if (length > 1) length = 1;
        if (Mathf.Abs(contraction_error) < 0.1 * SimulationData.max_contraction_error) length = 0;
        return length;
    }
}
