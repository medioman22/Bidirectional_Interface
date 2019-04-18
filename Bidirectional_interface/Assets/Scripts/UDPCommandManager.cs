using UnityEngine;
using System.Collections;

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

public class UDPCommandManager : MonoBehaviour
{
    enum MocapIndices
    {
        id = 0, // id of Optitrack rigidbody
        x = 1, // position
        y = 2,
        z = 3,
        qx = 4, // quaternion
        qy = 5,
        qz = 6,
        qw = 7
    }

    public enum TrackedTargets
    {
        RightHand = 0,
        LeftHand = 1,
        RightDrone = 2,
        LeftDrone = 3
    }

    public int RightHandrigidbodyID = 1;
    public int LeftHandrigidbodyID = 2;
    public int RightDronerigidbodyID = 3;
    public int LeftDronerigidbodyID = 4;

    // We track 4 rigidbodies (each of which has 8 params: id+pos+quaternion)
    private float[,] optiTrackRigidbodies = new float[4, SimulationData.nbParametersMocap];

    //UDP
    static private string localIP = "127.0.0.1"; // local IP

    private int localPortPython = 26000; //localport for receiving control commands

    Socket socket;
    EndPoint ipEndPoint = new IPEndPoint(IPAddress.Any, 0);

    void Start()
    {
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
        socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
        socket.EnableBroadcast = true;
        socket.Bind(new IPEndPoint(IPAddress.Parse(localIP), localPortPython));
    }

    private void Update()
    {
        receiveCommandsFromPython();
    }

    private void receiveCommandsFromPython() //receive commands
    {
        while (socket.Available > 0)
        {
            byte[] data = new byte[1024];
            int received = socket.ReceiveFrom(data, ref ipEndPoint);

            for (int i = 0; i < SimulationData.nbParametersMocap; i++)
            {
                int id = (int)System.BitConverter.ToSingle(data, (int)MocapIndices.id * 4);
                
                if (id == RightHandrigidbodyID)
                    optiTrackRigidbodies[(int)TrackedTargets.RightHand, i] = System.BitConverter.ToSingle(data, i * 4);
                else if (id == LeftHandrigidbodyID)
                    optiTrackRigidbodies[(int)TrackedTargets.LeftHand, i] = System.BitConverter.ToSingle(data, i * 4);
                else if (id == RightDronerigidbodyID)
                    optiTrackRigidbodies[(int)TrackedTargets.RightDrone, i] = System.BitConverter.ToSingle(data, i * 4);
                else if (id == LeftDronerigidbodyID)
                    optiTrackRigidbodies[(int)TrackedTargets.LeftDrone, i] = System.BitConverter.ToSingle(data, i * 4);
                else
                    break;
            }
        }
    }

    public Vector3 GetPosition(TrackedTargets target)
    {
        int i = (int)target;

        // x and z are inversed in unity compared to optitrack
        return new Vector3(optiTrackRigidbodies[i, (int)MocapIndices.z], optiTrackRigidbodies[i, (int)MocapIndices.y], 
                           optiTrackRigidbodies[i, (int)MocapIndices.x]);
    }

    public Quaternion GetQuaternion(TrackedTargets target)
    {
        int i = (int)target;

        // x and z are inversed in unity compared to optitrack, thus quaternion must be modified accordingly
        return new Quaternion(optiTrackRigidbodies[i, (int)MocapIndices.qz], optiTrackRigidbodies[i, (int)MocapIndices.qy], 
                              optiTrackRigidbodies[i,(int)MocapIndices.qx], -optiTrackRigidbodies[i,(int)MocapIndices.qw]);
    }
    
}
