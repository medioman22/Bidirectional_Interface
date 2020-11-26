using UnityEngine;
using System.Collections;

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Globalization;
using System.IO;

public class LeapInputUDP : MonoBehaviour
{

    // receiving Thread
    Thread receiveThread;

    // udpclient object
    UdpClient client;

    // Port defined in init()
    public int port;

    // infos
    public string lastReceivedUDPPacket = "";
    public float spread = 0.0f;

    // start from shell
    private static void Main()
    {
        LeapInputUDP receiveObj = new LeapInputUDP();
        receiveObj.init();

        string msg = "";
        do
        {
            msg = Console.ReadLine();
        }
        while (!msg.Equals("exit"));
    }
    // start from unity3d
    public void Start()
    {
        init();
    }

    // OnGUI
    void OnGUI()
    {
        Rect rectObj = new Rect(40, 10, 200, 400);
        GUIStyle style = new GUIStyle();
        style.alignment = TextAnchor.UpperLeft;
        GUI.Box(rectObj, "# Leap Input from: " + port + " #\n"
                    + "\nLast Packet: \n" + lastReceivedUDPPacket
                , style);
    }

    // init
    private void init()
    {
        // define port
        port = 5005;

        // status
        print("Test-Sending to this Port: nc -u 127.0.0.1  " + port + "");

        // Lokalen Endpunkt definieren (wo Nachrichten empfangen werden).
        // Einen neuen Thread für den Empfang eingehender Nachrichten erstellen.
        receiveThread = new Thread(
            new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
    }

    // receive thread
    private void ReceiveData()
    {
        client = new UdpClient(port);
        while (true)
        {
            try
            {
                // Receive data
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                byte[] data = client.Receive(ref anyIP);

                string msg = Encoding.UTF8.GetString(data);
                lastReceivedUDPPacket = msg;

                if (msg != "t")
                    spread = float.Parse(msg, CultureInfo.InvariantCulture.NumberFormat);
            }
            catch (Exception err)
            {
                print(err.ToString());
            }
        }
    }

}