using UnityEngine;
using System.Collections;

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

public class CommunicationMotors : MonoBehaviour
{
    private LaserSensors sensorValues;
    private float[] distances = new float[SimulationData.nbDistanceSensors];
    byte[] data;

    //UDP
    static private string localIP;
    static private int sendingPort;
    IPEndPoint ipEndPoint;
    UdpClient client;

    void Start()
    {
        sensorValues = GetComponent<LaserSensors>();

        data = new byte[SimulationData.nbDistanceSensors * 4];

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
        byte[] curByte = new byte[4];
        for (int j=0; j<SimulationData.nbDistanceSensors; j++)
        {
            curByte = System.BitConverter.GetBytes(distances[j]);
            data[(j*4)] = curByte[0];
            data[(j*4)+1] = curByte[1];
            data[(j*4)+2] = curByte[2];
            data[(j*4)+3] = curByte[3];
        }

        client.Send(data, data.Length, ipEndPoint);
    }

    private void fillArray()
    {
        distances[0] = sensorValues.allDistances.frontObstacle;
        distances[1] = sensorValues.allDistances.backObstacle;
        distances[2] = sensorValues.allDistances.upObstacle;
        distances[3] = sensorValues.allDistances.downObstacle;
        distances[4] = sensorValues.allDistances.leftObstacle;
        distances[5] = sensorValues.allDistances.rightObstacle;
    }
}
