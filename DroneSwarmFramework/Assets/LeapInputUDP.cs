using UnityEngine;
using System.Collections;

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

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
                // Bytes empfangen.
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                byte[] data = client.Receive(ref anyIP);

                // Bytes mit der UTF8-Kodierung in das Textformat kodieren.
                string msg = Encoding.UTF8.GetString(data);

                // Den abgerufenen Text anzeigen.
                print(">> " + msg);

                // latest UDPpacket
                lastReceivedUDPPacket = msg;

                spread = Decode(msg);
            }
            catch (Exception err)
            {
                print(err.ToString());
            }
        }
    }

    private float Decode(String msg)
    {


        return 0.0f;
    }
}