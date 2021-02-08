// myudp.cpp

#include "myudp.h"
#include <QTime>

MyUDP::MyUDP(QObject *parent) :
    QObject(parent)
{
    // create a QUDP socket
    socket = new QUdpSocket(this);

    // The most common way to use QUdpSocket class is
    // to bind to an address and port using bind()
    // bool QAbstractSocket::bind(const QHostAddress & address,
    //     quint16 port = 0, BindMode mode = DefaultForPlatform)
    socket->bind(QHostAddress::LocalHost, 27000);

    connect(socket, SIGNAL(readyRead()), this, SLOT(readyRead()));
}

void MyUDP::HelloUDP()
{
    QByteArray Data;
    Data.append("Hello from UDP");

    // Sends the datagram datagram
    // to the host address and at port.
    // qint64 QUdpSocket::writeDatagram(const QByteArray & datagram,
    //                      const QHostAddress & host, quint16 port)
    socket->writeDatagram(Data, QHostAddress::LocalHost, 29000);
}

void MyUDP::SendAllIMUData(ConnectedMTwData* DataIMU, int n)
{
    QByteArray Data;

    long long timestamp = QDateTime::currentMSecsSinceEpoch();


    for (int i=0; i<n; i++)
    {
        ID = DataIMU[i].ID().toStdString();
        ID.c_str();

        XsReal roll = DataIMU[i].orientation().roll();
        XsReal pitch = DataIMU[i].orientation().pitch();
        XsReal yaw = DataIMU[i].orientation().yaw();
        XsReal q_x = DataIMU[i].quaternion().x();
        XsReal q_y = DataIMU[i].quaternion().y();
        XsReal q_z = DataIMU[i].quaternion().z();
        XsReal q_w = DataIMU[i].quaternion().w();

        Data.append(reinterpret_cast<const char*>(&(timestamp)), sizeof(timestamp));
        Data.append(reinterpret_cast<const char*>(&(ID)), sizeof(ID));
        Data.append(reinterpret_cast<const char*>(&(roll)), sizeof(roll));
        Data.append(reinterpret_cast<const char*>(&(pitch)), sizeof(pitch));
        Data.append(reinterpret_cast<const char*>(&(yaw)), sizeof(yaw));
        Data.append(reinterpret_cast<const char*>(&(q_x)), sizeof(q_x));
        Data.append(reinterpret_cast<const char*>(&(q_y)), sizeof(q_y));
        Data.append(reinterpret_cast<const char*>(&(q_z)), sizeof(q_z));
        Data.append(reinterpret_cast<const char*>(&(q_w)), sizeof(q_w));
    }

    // Sends the datagram datagram
    // to the host address and at port.
    // qint64 QUdpSocket::writeDatagram(const QByteArray & datagram,
    //                      const QHostAddress & host, quint16 port)
    socket->writeDatagram(Data, QHostAddress::LocalHost, 29001);
}

void MyUDP::readyRead()
{
    // when data comes in
    QByteArray buffer;

    buffer.resize(socket->pendingDatagramSize());

    QHostAddress sender;
    quint16 senderPort;

    // qint64 QUdpSocket::readDatagram(char * data, qint64 maxSize,
    //                 QHostAddress * address = 0, quint16 * port = 0)
    // Receives a datagram no larger than maxSize bytes and stores it in data.
    // The sender's host address and port is stored in *address and *port
    // (unless the pointers are 0).

    socket->readDatagram(buffer.data(), buffer.size(), &sender, &senderPort);

    qDebug() << "Message from: " << sender.toString();
    qDebug() << "Message port: " << senderPort;
    qDebug() << "Message: " << buffer;
}
