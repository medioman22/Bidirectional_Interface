/*	WARNING: COPYRIGHT (C) 2017 XSENS TECHNOLOGIES OR SUBSIDIARIES WORLDWIDE. ALL RIGHTS RESERVED.
	THIS FILE AND THE SOURCE CODE IT CONTAINS (AND/OR THE BINARY CODE FILES FOUND IN THE SAME
	FOLDER THAT CONTAINS THIS FILE) AND ALL RELATED SOFTWARE (COLLECTIVELY, "CODE") ARE SUBJECT
	TO A RESTRICTED LICENSE AGREEMENT ("AGREEMENT") BETWEEN XSENS AS LICENSOR AND THE AUTHORIZED
	LICENSEE UNDER THE AGREEMENT. THE CODE MUST BE USED SOLELY WITH XSENS PRODUCTS INCORPORATED
	INTO LICENSEE PRODUCTS IN ACCORDANCE WITH THE AGREEMENT. ANY USE, MODIFICATION, COPYING OR
	DISTRIBUTION OF THE CODE IS STRICTLY PROHIBITED UNLESS EXPRESSLY AUTHORIZED BY THE AGREEMENT.
	IF YOU ARE NOT AN AUTHORIZED USER OF THE CODE IN ACCORDANCE WITH THE AGREEMENT, YOU MUST STOP
	USING OR VIEWING THE CODE NOW, REMOVE ANY COPIES OF THE CODE FROM YOUR COMPUTER AND NOTIFY
	XSENS IMMEDIATELY BY EMAIL TO INFO@XSENS.COM. ANY COPIES OR DERIVATIVES OF THE CODE (IN WHOLE
	OR IN PART) IN SOURCE CODE FORM THAT ARE PERMITTED BY THE AGREEMENT MUST RETAIN THE ABOVE
	COPYRIGHT NOTICE AND THIS PARAGRAPH IN ITS ENTIRETY, AS REQUIRED BY THE AGREEMENT.
*/

#ifndef XSDEVICEOPTIONFLAG_H
#define XSDEVICEOPTIONFLAG_H

/*! \brief Used to enable or disable some device options
	\sa XsDevice::setOptionFlags
	\note Not all devices support all options.
*/
enum XsDeviceOptionFlag
{
	XDOF_DisableAutoStore				= 0x00000001,
	XDOF_DisableAutoMeasurement			= 0x00000002,
	XDOF_EnableBeidou					= 0x00000004,
	XDOF_DisableGps						= 0x00000008,
	XDOF_EnableMagAidedVru				= 0x00000010,
	XDOF_Unused1						= 0x00000020,
	XDOF_EnableConfigurableBusId		= 0x00000040,
	XDOF_EnableInrunCompassCalibration	= 0x00000080,

	XDOF_None							= 0x00000000,
	XDOF_All							= 0xFFFFFFFF
};

typedef enum  XsDeviceOptionFlag XsDeviceOptionFlag;

#endif
