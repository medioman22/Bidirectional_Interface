using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using UnityEngine;

public class updateUI : MonoBehaviour
{
    public Text information;
    public Image arrow;
    public int i = 0;
    private GameObject swarm;
    // Start is called before the first frame update
    void Start()
    {
        information = gameObject.GetComponentInChildren<Text>();
        arrow = gameObject.GetComponentInChildren<Image>();
        swarm = GameObject.Find("Swarm");
    }

    // Update is called once per frame
    void Update()
    {
        arrow.rectTransform.Rotate(new Vector3(0, 0, 1));
        information.text = swarm.GetComponent<UpdateHandTarget>().heightError.ToString();
        i++;
    }
}
