using UnityEngine;
using System.Collections;

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

public class UDPCommandManager : MonoBehaviour
{
    public int rigidbodyTargetIndex = 2;
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

    //[HideInInspector]
    private float[] controlCommands = new float[SimulationData.nbParametersMocap];

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
                // the data points (int, 7 floats) each take 4 bytes
                if (System.BitConverter.ToSingle(data, 0) != rigidbodyTargetIndex) { break; }
                controlCommands[i] = System.BitConverter.ToSingle(data, i * 4);
            }
        }
    }

    public Vector3 GetPosition()
    {
        // x and z are inversed in unity compared to optitrack
        return new Vector3(controlCommands[(int)MocapIndices.z], controlCommands[(int)MocapIndices.y], controlCommands[(int)MocapIndices.x]);
    }

    public Quaternion GetQuaternion()
    {
        // x and z are inversed in unity compared to optitrack, thus quaternion must be modified accordingly
        return new Quaternion(controlCommands[(int)MocapIndices.qz], controlCommands[(int)MocapIndices.qy], controlCommands[(int)MocapIndices.qx], -controlCommands[(int)MocapIndices.qw]);
    }
    
}
