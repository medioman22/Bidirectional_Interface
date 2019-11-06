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
    private LaserSensors sensorValues;
    private float[] distances = new float[SimulationData.nbDistanceSensors];
    private Vector3[] positions;
    private List<GameObject> allDrones;
    byte[] data;

    //UDP
    static private string localIP;
    static private int sendingPort;
    IPEndPoint ipEndPoint;
    UdpClient client;

    void Start()
    {
        foreach (Transform drone in transform)
        {
            if (drone.gameObject.tag == "Drone") allDrones.Add(drone.gameObject);
        }
        positions = new Vector3[allDrones.Count];
        data = new byte[allDrones.Count *3 *4];

        localIP = "127.0.0.1"; // local IP
        sendingPort = 8051; //port used to send the distances to python
        ipEndPoint = new IPEndPoint(IPAddress.Parse(localIP), sendingPort);
        client = new UdpClient();
    }

    private void Update()
    {
        fillArray();
        sendDistancesToPython();
    }

    private void sendDistancesToPython() //send distances
    {
        //distance is a float :  a float is 4 bytes
        byte[] curByte = new byte[4];
        for (int j = 0; j < allDrones.Count; j++)
        {
            for (int i = 0; i < 3; i++)
            {
                curByte = System.BitConverter.GetBytes(positions[j][i]);
                data[(j * 4)] = curByte[0];
                data[(j * 4) + 1] = curByte[1];
                data[(j * 4) + 2] = curByte[2];
                data[(j * 4) + 3] = curByte[3];
            }
        }

        client.Send(data, data.Length, ipEndPoint);
    }

    private void fillArray()
    {
        int i = 0;
        foreach (GameObject drone in allDrones)
        {
            positions[i] = drone.GetComponent<PositionControl>().transform.position;
            i += 1;
        }

    }


    private void OnApplicationQuit()
    {
        for (int i = 0; i < SimulationData.nbDistanceSensors; i++)
        {
            distances[i] = float.PositiveInfinity;
        }

        sendDistancesToPython();
        System.Threading.Thread.Sleep(100);
        sendDistancesToPython();
    }
}
