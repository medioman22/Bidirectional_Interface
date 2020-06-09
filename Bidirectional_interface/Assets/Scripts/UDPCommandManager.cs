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
    enum IMUIndices
    {
        roll1 = 0, // imu 1
        pitch1 = 1,
        yaw1 = 2,
        roll2 = 3, // imu 2
        pitch2 = 4,
        yaw2 = 5
    }

    //[HideInInspector]
    private float[] controlCommands = new float[SimulationData.nbParametersMocap];
    private float[] IMUvalues = new float[SimulationData.nbIMUValues];

    //UDP
    static private string localIP = "127.0.0.1"; // local IP

    private int localPortPython = 26000; //localport for receiving control commands
    private int localPortIMUs = 29002; //localport for receiving IMUs 

    Socket socket;
    Socket IMUsocket;
    EndPoint ipEndPoint = new IPEndPoint(IPAddress.Any, 0);

    void Start()
    {
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
        socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
        socket.EnableBroadcast = true;
        socket.Bind(new IPEndPoint(IPAddress.Parse(localIP), localPortPython));

        IMUsocket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
        IMUsocket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
        IMUsocket.EnableBroadcast = true;
        IMUsocket.Bind(new IPEndPoint(IPAddress.Parse(localIP), localPortIMUs));
    }

    private void Update()
    {
        receiveCommandsFromPython();
        receiveCommandsFromIMUs();
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
                if (System.BitConverter.ToSingle(data, (int)MocapIndices.id) != rigidbodyTargetIndex) { break; }
                controlCommands[i] = System.BitConverter.ToSingle(data, i * 4);
            }
        }
    }

    private void receiveCommandsFromIMUs() //receive commands
    {
        // Debug.Log("reading IMUs");
        while (IMUsocket.Available > 0)
        {
            // Debug.Log("in");
            byte[] data = new byte[1024];
            int received = IMUsocket.ReceiveFrom(data, ref ipEndPoint);

            for (int i = 0; i < SimulationData.nbIMUValues; i++)
            {
                // the data points (int, 7 floats) each take 4 bytes
                controlCommands[i] = System.BitConverter.ToSingle(data, i * 4);
                // Debug.Log("new val");
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

    public Vector3 GetIMU1()
    {
        // x and z are inversed in unity compared to optitrack, thus quaternion must be modified accordingly
        return new Vector3(controlCommands[(int)IMUIndices.roll1], controlCommands[(int)IMUIndices.pitch1], controlCommands[(int)IMUIndices.yaw1]);
    }

    public Vector3 GetIMU2()
    {
        // x and z are inversed in unity compared to optitrack, thus quaternion must be modified accordingly
        return new Vector3(controlCommands[(int)IMUIndices.roll2], controlCommands[(int)IMUIndices.pitch2], controlCommands[(int)IMUIndices.yaw2]);
    }
    
}
