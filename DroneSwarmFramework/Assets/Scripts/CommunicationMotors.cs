using UnityEngine;
using System.Collections;

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Linq;

public class CommunicationMotors : MonoBehaviour
{
    private LaserSensors sensorFR;
    private LaserSensors sensorBR;
    private LaserSensors sensorBL;
    private LaserSensors sensorFL;

    private float[] distances = new float[SimulationData.nbDistanceSensors];
    byte[] data;

    //UDP
    static private string localIP;
    static private int sendingPort;
    IPEndPoint ipEndPoint;
    UdpClient client;

    // Drones in swarm
    public GameObject droneFR;
    public GameObject droneBR;
    public GameObject droneBL;
    public GameObject droneFL;

    void Start()
    {
        sensorFR = droneFR.GetComponent<LaserSensors>();
        sensorBR = droneBR.GetComponent<LaserSensors>();
        sensorBL = droneBL.GetComponent<LaserSensors>();
        sensorFL = droneFL.GetComponent<LaserSensors>();

        data = new byte[SimulationData.nbDistanceSensors * 4];

        localIP = "127.0.0.1"; // local IP
        sendingPort = 8051; //port used to send the distances to python
        ipEndPoint = new IPEndPoint(IPAddress.Parse(localIP), sendingPort);
        client = new UdpClient();
    }

    private void LateUpdate()
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
            data[j * 4] = curByte[0];
            data[j * 4 + 1] = curByte[1];
            data[j * 4 + 2] = curByte[2];
            data[j * 4 + 3] = curByte[3];
        }

        client.Send(data, data.Length, ipEndPoint);
    }

    private void fillArray()
    {
        // Find minimum for all drones in every direction
        float[] front_distances = {sensorFR.allDistances.frontObstacle, sensorBR.allDistances.frontObstacle,
                                   sensorBL.allDistances.frontObstacle, sensorFL.allDistances.frontObstacle};
        distances[0] = front_distances.Min();

        float[] back_distances = {sensorFR.allDistances.backObstacle, sensorBR.allDistances.backObstacle,
                                  sensorBL.allDistances.backObstacle, sensorFL.allDistances.backObstacle};
        distances[1] = back_distances.Min();

        float[] left_distances = {sensorFR.allDistances.leftObstacle, sensorBR.allDistances.leftObstacle,
                                  sensorBL.allDistances.leftObstacle, sensorFL.allDistances.leftObstacle};
        distances[2] = left_distances.Min();

        float[] right_distances = {sensorFR.allDistances.rightObstacle, sensorBR.allDistances.rightObstacle,
                                   sensorBL.allDistances.rightObstacle, sensorFL.allDistances.rightObstacle};
        distances[3] = right_distances.Min();
    }


    private void OnApplicationQuit()
    {
        for (int i=0; i<SimulationData.nbDistanceSensors; i++)
        {
            distances[i] = float.PositiveInfinity;
        }

        sendDistancesToPython();
        System.Threading.Thread.Sleep(100);
        sendDistancesToPython();
    }
}
