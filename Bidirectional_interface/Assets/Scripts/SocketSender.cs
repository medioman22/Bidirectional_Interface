using UnityEngine;
using System.Collections.Generic;

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Linq;

public class SocketSender : MonoBehaviour
{
    public List<GameObject> allDrones;

    private LaserSensors sensorValues;
    private float[] distances = new float[SimulationData.nbDistanceSensors];
    private List<Vector3> positions = new List<Vector3>();
    private float device;
    byte[] data;

    //UDP
    static private string localIP;
    static private int sendingPort;
    IPEndPoint ipEndPoint;
    UdpClient client;

    void Start()
    {
        foreach (Transform child in transform)
        {
            if (child.gameObject.tag == "Drone") allDrones.Add(child.gameObject);
        }
        
        //11 different float to send to python script
        data = new byte[11*4];

        localIP = "127.0.0.1"; // local IP
        sendingPort = 8051; //port used to send the distances to python
        ipEndPoint = new IPEndPoint(IPAddress.Parse(localIP), sendingPort);
        client = new UdpClient();
        foreach (GameObject drone in allDrones)
        {
            positions.Add(drone.GetComponent<PositionControl>().transform.position);
        }
    }

    private void Update()
    {
        sendInformationToPython();
    }


    private void sendInformationToPython()
    {
        UpdateHandTarget swarm = GetComponent<UpdateHandTarget>();
        byte[] currentByte = new byte[4];
        int j = 0;

        //Difference between real and desired height
        currentByte = System.BitConverter.GetBytes(swarm.heightError);
        floatToByte(j, currentByte);
        j++;


        //Max distance between an element and the Center Of Gravity of the 


        currentByte = System.BitConverter.GetBytes(swarm.extensionError);
        floatToByte(j, currentByte);
        j++;

        //Distance to next waypoint
        j = vector3toByte(swarm.distanceToWaypoint, j);
        //print(distanceToWaypoint(new Vector3(0.0f, 0.0f, 0.0f)));

        currentByte = System.BitConverter.GetBytes(Convert.ToSingle(swarm.experimentState));
        floatToByte(j, currentByte);
        j++;

        currentByte = System.BitConverter.GetBytes(Convert.ToSingle(SimulationData.max_distance_error));
        floatToByte(j, currentByte);
        j++;

        currentByte = System.BitConverter.GetBytes(Convert.ToSingle(SimulationData.max_height_error));
        floatToByte(j, currentByte);
        j++;

        currentByte = System.BitConverter.GetBytes(Convert.ToSingle(SimulationData.max_contraction_error));
        floatToByte(j, currentByte);
        j++;

        currentByte = System.BitConverter.GetBytes(Convert.ToSingle(swarm.stopAllMotors));
        floatToByte(j, currentByte);
        j++;
        
        if (swarm.feedback.ToString() == "Glove") device = 1.0f;
        else if (swarm.feedback.ToString() == "Bracelets") device = 0.0f;

        currentByte = System.BitConverter.GetBytes(Convert.ToSingle(device));
        floatToByte(j, currentByte);
        j++;

        client.Send(data, data.Length, ipEndPoint);
    }
    private void floatToByte(int j, byte[] currentByte)
    {
        for (int i = 0; i < 4; i++)
        {
            data[(j * 4 + i)] = currentByte[i];
        }
       
    }

    private int vector3toByte(Vector3 distance, int j)
    {
        for (int i = 0; i < 3; i++)
        {
            byte[] currentByte = System.BitConverter.GetBytes(distance[i]);
            floatToByte(j, currentByte);
            j++;
        }
        return j;
    }

}
