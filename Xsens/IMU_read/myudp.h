// myudp.h

#ifndef MYUDP_H
#define MYUDP_H

#include <QObject>
#include <QUdpSocket>
#include <connectedmtwdata.h>

class MyUDP : public QObject
{
    Q_OBJECT
public:
    explicit MyUDP(QObject *parent = 0);
    void HelloUDP();
    void SendAllIMUData(ConnectedMTwData* data, int n);
signals:

public slots:
    void readyRead();

private:

    std::string ID;
    QUdpSocket *socket;

};

#endif // MYUDP_H
