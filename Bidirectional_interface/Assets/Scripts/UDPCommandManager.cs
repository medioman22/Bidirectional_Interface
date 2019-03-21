using UnityEngine;
using System.Collections;

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

public class UDPCommandManager : MonoBehaviour
{
    public const int nbCommands = 3; // x, y, z position of hand

    //Input & output vectors=
    [HideInInspector]
    public float[] controlCommands = new float[nbCommands];

    //UDP
    //private string localIP = "127.0.0.1"; // local IP
    static private string localIP = "127.0.0.1"; // local IP

    private int localPort_python = 26000; //localport for receiving control commands
    private int localPort_Unity_query = 30001; //local port for sending query
    private int localPort_Unity_calib = 30002; //local port for sending calibration data

    private string remoteIPPy = localIP; // IP of the PC containing the Py app
    private int remotePort_Py = 27000; //remoteport of Qt which emits control commands
    private int remotePort_Py_query = 30011; //local port for sending query
    private int remotePort_Py_calib = 30012; //local port for sending calibration data
    private IPEndPoint remoteEndPointPy, remoteEndPointPy_query, remoteEndPointPy_calib;
    private IPEndPoint localEndPoint_python, localEndPoint_calib, localEndPoint_query;
    private UdpClient client_python, client_calib, client_query;

    //byte[] ByteArray_calib = new byte[(Parameters.NUMBER_OF_KEYJOY + Parameters.NUMBER_OF_SENSORS + 3 + 4 + 1 + 6) * 4]; // + position + quaternion + time + info
    /*byte[] ByteArray_calib = new byte[(8 + 3 + 4 + 1 + 6) * 4]; // + position + quaternion + time + info
    byte[] ByteArray_query = new byte[1];*/

    void Start()
    {
        //Setup remote socket
        remoteEndPointPy_query = new IPEndPoint(IPAddress.Parse(remoteIPPy), remotePort_Py_query);
        remoteEndPointPy_calib = new IPEndPoint(IPAddress.Parse(remoteIPPy), remotePort_Py_calib);
        remoteEndPointPy = new IPEndPoint(IPAddress.Parse(remoteIPPy), remotePort_Py);

        //Setup local socket
        localEndPoint_python = new IPEndPoint(IPAddress.Parse(localIP), localPort_python);
        localEndPoint_calib = new IPEndPoint(IPAddress.Parse(localIP), localPort_Unity_calib);
        localEndPoint_query = new IPEndPoint(IPAddress.Parse(localIP), localPort_Unity_query);

        client_python = new UdpClient(localEndPoint_python);
        client_calib = new UdpClient(localEndPoint_calib);
        client_query = new UdpClient(localEndPoint_query);

    }

    private void Update()
    {
        receiveCommandsFromPython();
    }

    public void receiveCommandsFromPython() //receive commands
    {
        if (client_python.Available > 0)
        {
            byte[] data = client_python.Receive(ref remoteEndPointPy);

            //for(int i = 0; i< 12; i++){
            //	Debug.Log("value: " + data[i] + "\n");
            //}

            //Debug.Log("received:" + data + "\n");

            //for (int i = 0; i < Parameters.NUMBER_OF_CONTROLS_COMMAND_FLOAT; i++)
            for (int i = 0; i < nbCommands; i++)
            {
                controlCommands[i] = System.BitConverter.ToSingle(data, i * 4);
            }
        }
    }

    /*public void Send_CalibData(float[] calibdata) //keyjoy
    {
        Buffer.BlockCopy(calibdata, 0, ByteArray_calib, 0, ByteArray_calib.Length);

        try
        {
            client_calib.Send(ByteArray_calib, ByteArray_calib.Length, remoteEndPointPy_calib);
        }
        catch (Exception err)
        {
            print(err.ToString());
        }
    }

    public void Send_query(char[] query) //keyjoy
    {
        Buffer.BlockCopy(query, 0, ByteArray_query, 0, ByteArray_query.Length);

        try
        {
            client_query.Send(ByteArray_query, ByteArray_query.Length, remoteEndPointPy_query);
        }
        catch (Exception err)
        {
            print(err.ToString());
        }
    }*/
}
