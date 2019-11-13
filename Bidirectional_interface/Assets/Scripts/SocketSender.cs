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
    private int nbOfDrones;
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
        nbOfDrones = allDrones.Count;

        //for each drone, there is 3 positions and each position is a float which requires 4 bytes, plus the dronestate
        //data = new byte[(nbOfDrones * 3 + 1) *4];
        //8 different float a envoyer au script python
        data = new byte[7* 4];

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
        //fillPositionsArray();
        //sendDistancesToPython();
        //sendInformationToPython();
        sendInformationToPython2();
    }

    private void fillPositionsArray()
    {
        int i = 0;
        foreach (GameObject drone in allDrones)
        {
            positions[i] = drone.GetComponent<PositionControl>().transform.position;
            i++;
        }

    }

    private void sendDistancesToPython() //send distances
    {
        //distance is a float :  a float is 4 bytes
        byte[] curByte = new byte[4];
        for (int j = 0; j < nbOfDrones; j++)
        {
            for (int i = 0; i < 3; i++)
            {
                curByte = System.BitConverter.GetBytes(positions[j][i]);
                data[(j * 12 + i * 4)] = curByte[0];
                data[(j * 12 + i * 4) + 1] = curByte[1];
                data[(j * 12 + i * 4) + 2] = curByte[2];
                data[(j * 12 + i * 4) + 3] = curByte[3];
            }
        }
        int droneState = this.GetComponentInParent<UpdateHandTarget>().droneState;
        curByte = System.BitConverter.GetBytes(Convert.ToSingle(droneState));
        floatToByte(nbOfDrones, curByte);

        client.Send(data, data.Length, ipEndPoint);
    }

    private void sendInformationToPython()
    {
        byte[] currentByte = new byte[4];
        int j = 0;
        //Difference between real and desired height
        currentByte = System.BitConverter.GetBytes(heightError());
        //print(heightError());
        floatToByte(j, currentByte);
        j++;
        //Max distance between an element and the Center Of Gravity of the swarm
        currentByte = System.BitConverter.GetBytes(maxRadius());
        //print(maxRadius());
        floatToByte(j, currentByte);
        j++;
        //Distance to next waypoint
        j = vector3toByte(distanceToWaypoint(new Vector3(0.0f, 0.0f, 0.0f)), j);
        //print(distanceToWaypoint(new Vector3(0.0f, 0.0f, 0.0f)));

        //Distance from pilote
        j = vector3toByte(distanceToWaypoint(new Vector3(1.0f, 1.0f, 1.0f)), j);

        client.Send(data, data.Length, ipEndPoint);
    }

    private void sendInformationToPython2()
    {
        UpdateHandTarget swarm = GetComponent<UpdateHandTarget>();
        byte[] currentByte = new byte[4];
        int j = 0;
        //Difference between real and desired height
        currentByte = System.BitConverter.GetBytes(swarm.heightError);
        //print(heightError());
        floatToByte(j, currentByte);
        j++;
        //Max distance between an element and the Center Of Gravity of the swarm
        currentByte = System.BitConverter.GetBytes(swarm.extensionError);
        //print(maxRadius());
        floatToByte(j, currentByte);
        j++;

        //Max distance between an element and the Center Of Gravity of the swarm
        currentByte = System.BitConverter.GetBytes(swarm.contractionError);
        //print(maxRadius());
        floatToByte(j, currentByte);
        j++;
        //Distance to next waypoint
        j = vector3toByte(swarm.distanceToWaypoint, j);
        //print(distanceToWaypoint(new Vector3(0.0f, 0.0f, 0.0f)));

        //Max distance between an element and the Center Of Gravity of the swarm
        currentByte = System.BitConverter.GetBytes(Convert.ToSingle(swarm.experimentState));
        //print(maxRadius());
        floatToByte(j, currentByte);

        client.Send(data, data.Length, ipEndPoint);
    }
    private void floatToByte(int j, byte[] currentByte)
    {
        for (int i = 0; i < 4; i++)
        {
            data[(j * 4 + i)] = currentByte[i];
 //           print(j*4+i);
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


    private float heightError()
    {
        float currenHeight = averageHeight();
        float desiredHeight = gameObject.transform.GetComponent<UpdateHandTarget>().desiredHeight;
        return currenHeight - desiredHeight;
    }

    private float averageHeight()
    {
        List<float> height = new List<float>();
        foreach (Vector3 position in positions) height.Add(position.y);
        return height.Average();
    }

    private Vector3 averagePosition()
    {
        Vector3 Positions = new Vector3(0, 0, 0);
        foreach (GameObject drone in allDrones) Positions += drone.transform.position;
        Positions /= allDrones.Count;
        return Positions;
    }

    private float maxRadius()
    {
        float maxDistance = 0.0f;
        Vector3 CoG = averagePosition();
        Vector2 horizCoG = new Vector2(CoG.x, CoG.z);
        foreach (Vector3 position in positions)
        {
            Vector2 horizPos = new Vector2(position.x, position.z);
            float radius = Math.Abs(Vector2.Distance(horizCoG, horizPos));
            if (radius > maxDistance) maxDistance = radius;
        }
        return maxDistance;
    }

    private Vector3 distanceToWaypoint(Vector3 nextWaypoint)
    {
        //direction of the next waypoint relative to the CoG of the swarm
        Vector3 CoG = averagePosition();
        return nextWaypoint - CoG;
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
