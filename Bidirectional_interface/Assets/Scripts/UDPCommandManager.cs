using UnityEngine;
using System.Collections;

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

public class UDPCommandManager : MonoBehaviour
{
    public const int nbCommands = 8; // x, y, z position of hand

    //Input & output vectors=
    //[HideInInspector]
    public float[] controlCommands = new float[nbCommands];

    //UDP
    static private string localIP = "127.0.0.1"; // local IP

    private int localPort_python = 26000; //localport for receiving control commands

    private string remoteIPPy = localIP; // IP of the PC containing the Py app
    private IPEndPoint remoteEndPointPy;
    private IPEndPoint localEndPoint_python;
    private UdpClient client_python;

    Socket socket;

    EndPoint ipEndPoint = new IPEndPoint(IPAddress.Any, 0);

    void Start()
    {
        //Setup remote socket
        remoteEndPointPy = new IPEndPoint(IPAddress.Any, 0);

        //Setup local socket
        //localEndPoint_python = new IPEndPoint(IPAddress.Any, localPort_python);
        //client_python = new UdpClient(localPort_python);

        socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
        socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
        socket.EnableBroadcast = true;
        //socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
        socket.Bind(new IPEndPoint(IPAddress.Parse(localIP), localPort_python));
    }

    private void Update()
    {
        receiveCommandsFromPython();
    }

    public void receiveCommandsFromPython() //receive commands
    {
        if (socket.Available > 0)
        {
            
            byte[] data = new byte[1024];
            int received = socket.ReceiveFrom(data, ref ipEndPoint);

            for (int i = 0; i < nbCommands; i++)
            {
                controlCommands[i] = System.BitConverter.ToSingle(data, i * 4);
            }
        }

        /*if (client_python.Available > 0)
        {
            Debug.Log("here");
            byte[] data = client_python.Receive(ref remoteEndPointPy);

            for(int i = 0; i< 12; i++)
            {
            	Debug.Log("value: " + data[i] + "\n");
            }

            //Debug.Log("received:" + data + "\n");

            for (int i = 0; i < nbCommands; i++)
            {
                controlCommands[i] = System.BitConverter.ToSingle(data, i * 4);
            }
        }*/
    }
}
