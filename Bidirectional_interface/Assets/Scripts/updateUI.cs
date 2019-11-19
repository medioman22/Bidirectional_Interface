using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using UnityEngine;

public class updateUI : MonoBehaviour
{
    public Text information;
    public Image horizontal_arrow;
    public Image vertical_arrow;
    public int i = 0;
    private GameObject swarm;
    private float displayedValue;
    private int experimentState;
    private string vertDirection = "up";
    private string horizDirection = "";
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

    // Start is called before the first frame update
    void Start()
    {
        information = gameObject.GetComponentInChildren<Text>();
        horizontal_arrow = GameObject.Find("Horizontal arrow").GetComponent<Image>();
        vertical_arrow = GameObject.Find("Vertical arrow").GetComponent<Image>();
        swarm = GameObject.Find("Swarm");
        arrowDirection.Add("up", new Vector3(0f, 90f, 0f));
        arrowDirection.Add("down", new Vector3(0f, 90f, 180.0f));

        arrowDirection.Add("left", new Vector3(-90.000001f, 180.000001f, 0.0f));
        arrowDirection.Add("back", new Vector3(-90.00001f, 270.0001f, 0.0f));
        arrowDirection.Add("right", new Vector3(-90f, 0f, 0.0f));
        arrowDirection.Add("front", new Vector3(-90.00001f, 90.0f, 0f));
    }

    // Update is called once per frame
    void Update()
    {
        UpdateHandTarget updHandTarget = swarm.GetComponent<UpdateHandTarget>();
        experimentState = swarm.GetComponent<UpdateHandTarget>().experimentState;

        if (updHandTarget.heightError <= 0) vertDirection = "up";
        else vertDirection = "down";

        ;
        Vector3 oldArrowDirect;
        horizDirection = "left";

        switch (experimentState)
        {
            case REACHING_HEIGHT:
                displayedValue = updHandTarget.heightError;
                break;

            case GO_TO_FIRST_WAYPOINT:
                //displayedValue = updHandTarget.distanceToWaypoint;
                //displayedValue = 2.0f;
                Vector3 distToWaypoint = updHandTarget.distanceToWaypoint;
                float angle = Mathf.Rad2Deg * Mathf.Atan(distToWaypoint.x / distToWaypoint.y);
                if (Mathf.Abs(angle) == 90 || Mathf.Abs(angle) == 180 || Mathf.Abs(angle) == 270) angle += 0.0001f;
                arrowDirect = new Vector3(-90.0f, angle, 0.0f);
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
        //arrow.rectTransform.Rotate(new Vector3(0, 0, 1));
        vertical_arrow.rectTransform.rotation = Quaternion.Euler(arrowDirection[vertDirection]);
        horizontal_arrow.rectTransform.rotation = Quaternion.Euler(arrowDirect);// * Quaternion.Euler(arrowDirection["front"]);
        information.text = displayedValue.ToString();
        i++;
    }
}
