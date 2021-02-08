/*	Copyright (c) 2003-2017 Xsens Technologies B.V. or subsidiaries worldwide.
	All rights reserved.

	Redistribution and use in source and binary forms, with or without modification,
	are permitted provided that the following conditions are met:

	1.	Redistributions of source code must retain the above copyright notice,
		this list of conditions and the following disclaimer.

	2.	Redistributions in binary form must reproduce the above copyright notice,
		this list of conditions and the following disclaimer in the documentation
		and/or other materials provided with the distribution.

	3.	Neither the names of the copyright holders nor the names of their contributors
		may be used to endorse or promote products derived from this software without
		specific prior written permission.

	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
	EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
	MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
	THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
	SPECIAL, EXEMPLARY OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
	OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
	HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY OR
	TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
	SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#ifndef CONNECTEDMTWDATA_H
#define CONNECTEDMTWDATA_H

#include <xsensdeviceapi.h> // The Xsens device API header

#include <QMetaType>
#include <QList>

//------------------------------------------------------------------------------
// Class used to store the connection data of a connected MTw.
// It is attached to the list item itself and therefore declared as meta-type.
//------------------------------------------------------------------------------
class ConnectedMTwData
{
public:
    ConnectedMTwData();
    ~ConnectedMTwData();

    QString ID() const;
    int batteryLevel() const;
    int rssi() const;
    int effectiveUpdateRate() const;
    XsEuler orientation() const;
    XsQuaternion quaternion() const;
    XsMatrix3x3 matrix() const;
    QList<int>* frameSkipsList();
    unsigned int sumFrameSkips() const;
	bool containsOrientation() const;

    void setIDint(XsDeviceId newIDint);
    void setID(QString newID);
    void setBatteryLevel(int newBatteryLevel);
    void setRssi(int newRssi);
    void setEffectiveUpdateRate(int newEffectiveUpdateRate);
    void setSumFrameSkips(int newSumFrameSkips);
    void setOrientation(XsEuler newOrientation);
    void setQuaternion(XsQuaternion newQuaternion);
    void setMatrix(XsMatrix3x3 newMatrix);

private:

    XsDeviceId		m_IDint;
    QString			m_ID;
    int				m_batteryLevel;
    int				m_rssi;
    int				m_effectiveUpdateRate;
    XsEuler			m_orientation;
    XsQuaternion	m_quaternion;
    XsMatrix3x3		m_matrix;
    QList<int>		m_frameSkipsList;
    unsigned int	m_sumFrameSkips;
	bool			m_containsOrientation;
};
Q_DECLARE_METATYPE(ConnectedMTwData)


#endif // CONNECTEDMTWDATA_H