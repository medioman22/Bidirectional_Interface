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
    public Image extract_arrow1;
    public Image extract_arrow2;
    private Vector2 distToWaypoint;
    private float heightError;
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
        extract_arrow1 = GameObject.Find("Extract1").GetComponent<Image>();
        extract_arrow2 = GameObject.Find("Extract2").GetComponent<Image>();
        swarm = GameObject.Find("Swarm");
        arrowDirection.Add("up", new Vector3(0f, 90f, 0f));
        arrowDirection.Add("down", new Vector3(0f, 90f, 180.0f));

        arrowDirection.Add("left", new Vector3(0.0f, 0.0f, 0.0f));
        arrowDirection.Add("back", new Vector3(0.0f, 270.0f, 0.0f));
        arrowDirection.Add("right", new Vector3(0.0f, 0f, 0.0f));
        arrowDirection.Add("front", new Vector3(0.0f, 90.0f, 0f));
    }

    // Update is called once per frame
    void Update()
    {
        UpdateHandTarget updHandTarget = swarm.GetComponent<UpdateHandTarget>();
        experimentState = swarm.GetComponent<UpdateHandTarget>().experimentState;

        distToWaypoint = new Vector2(updHandTarget.distanceToWaypoint.x, updHandTarget.distanceToWaypoint.z);
        heightError = updHandTarget.heightError;

        if (heightError <= 0) vertDirection = "up";
        else vertDirection = "down";

        switch (experimentState)
        {
            case REACHING_HEIGHT:
                displayedValue = heightError;
                break;

            case GO_TO_FIRST_WAYPOINT:
                //displayedValue = updHandTarget.distanceToWaypoint;
                //displayedValue = 2.0f;
                break;

            case EXTENSION:
                displayedValue = updHandTarget.extensionError;
                break;

            case WAYPOINT_NAV:
                //displayedValue = updHandTarget.distanceToWaypoint;
                break;

            case CONTRACTION:
                displayedValue = updHandTarget.contractionError;
                break;
        }


        vertical_arrow.rectTransform.localScale = new Vector3(1.0f, lengthOfHeightArrow(), 1.0f);
        vertical_arrow.rectTransform.rotation = Quaternion.Euler(arrowDirection[vertDirection]);
        contract_arrow.enabled = false;
        angle = 90.0f + Vector2.SignedAngle(distToWaypoint, new Vector2(10.0f, 0.0f));
        horizontal_arrow.rectTransform.rotation = Quaternion.Euler(new Vector3(90.0f, angle, 0.0f));
        horizontal_arrow.rectTransform.localScale = new Vector3 (1.0f, lengthOfDistArrow(),1.0f);

        //information.text = displayedValue.ToString();

        print("Distance to waypoint :" + distToWaypoint);
        print("Rotation :" +angle);
    }

    float lengthOfDistArrow()
    {
        float length = 0.0f;
        float distance = distToWaypoint.magnitude;
        length = distance / SimulationData.max_distance_error *1;
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
}
