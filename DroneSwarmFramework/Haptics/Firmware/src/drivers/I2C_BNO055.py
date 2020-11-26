# -*- coding: utf-8 -*-
# Author: Cyrill Lippuner
# Date: October 2018
"""
Driver file for the BNO055 accelerometer / gyroscope / magnetometer. Communicates
with the device via I2C and implements the basic functions for integrating into
the SoftWEAR package.
"""
import time                                                     # Imported for delay reasons
import drivers._BNO055 as BNO055_DRIVER                         # Import official driver
import threading                                                # Threading class for the threads

from MuxModule import Mux                                       # SoftWEAR MUX module.

# Create a MUX shadow instance as there is only one Mux
MuxShadow = Mux()

# Unique identifier of the sensor
IDENTIFIER = BNO055_DRIVER.BNO055_ID

# Addresses
ADDRESS_1 = BNO055_DRIVER.BNO055_ADDRESS_A
ADDRESS_2 = BNO055_DRIVER.BNO055_ADDRESS_B
BUSNUM = 2

# Mode Map
MODE_MAP = {
    'ACCONLY':      BNO055_DRIVER.OPERATION_MODE_ACCONLY,
    'MAGONLY':      BNO055_DRIVER.OPERATION_MODE_MAGONLY,
    'GYRONLY':      BNO055_DRIVER.OPERATION_MODE_GYRONLY,
    'ACCMAG':       BNO055_DRIVER.OPERATION_MODE_ACCMAG,
    'ACCGYRO':      BNO055_DRIVER.OPERATION_MODE_ACCGYRO,
    'MAGGYRO':      BNO055_DRIVER.OPERATION_MODE_MAGGYRO,
    'AMG':          BNO055_DRIVER.OPERATION_MODE_AMG,
    'IMU':          BNO055_DRIVER.OPERATION_MODE_IMUPLUS,
    'COMPASS':      BNO055_DRIVER.OPERATION_MODE_COMPASS,
    'M4G':          BNO055_DRIVER.OPERATION_MODE_M4G,
    'NDOF_FMC_OFF': BNO055_DRIVER.OPERATION_MODE_NDOF_FMC_OFF,
    #'NDOF':         BNO055_DRIVER.OPERATION_MODE_NDOF
}
################################################################
# WARNING: NDOF                                                #
# NDOF mode cannot be selected during runtime. Please change driver to initialize to NDOF mode at the beginning if needed and do not change it afterwards. More documentation in the official driver _BNO055.py
################################################################



class BNO055:
    """Driver for BNO055."""

    # Name of the device
    _name = 'BNO055'

    # Info of the device
    _info = 'The BNO055 is the first in a new family of Application Specific Sensor Nodes (ASSN) implementing an intelligent 9-axis Absolute Orientation Sensor, which includes sensors and sensor fusion in a single package.'

    # Direction of the driver (in/out)
    _dir = 'in'

    # Dimension of the driver (0-#)
    _dim = 17

    # Dimension map of the driver (0-#)
    _dimMap = ['Acc X', 'Acc Y', 'Acc Z', 'Mag X', 'Mag Y', 'Mag Z', 'Gyr X', 'Gyr Y', 'Gyr Z', 'Euler Head', 'Euler Roll', 'Euler Pitch', 'Quat W', 'Quat X', 'Quat Y', 'Quat Z', 'Temp']

    # Dimension unit of the driver (0-#)
    _dimUnit = ['m/s^2', 'm/s^2', 'm/s^2', 'uT', 'uT', 'uT', '°/s', '°/s', '°/s', '°', '°', '°', '', '', '', '', '°C']

    # Channel
    _channel = None

    # Muxed channel
    _muxedChannel = None

    # The driver object
    _bno = None

    # Flag whether the driver is connected
    _connected = False

    # Settings of the driver
    _settings = {
        'frequencies': [
            '1 Hz',
            '2 Hz',
            '3 Hz',
            '4 Hz',
            '5 Hz',
            '6 Hz',
            '10 Hz',
            '20 Hz',
            '30 Hz',
            '40 Hz',
            '50 Hz',
            '60 Hz',
            '100 Hz'
        ],
        'modes': [
            'ACCONLY',
            'MAGONLY',
            'GYRONLY',
            'ACCMAG',
            'ACCGYRO',
            'MAGGYRO',
            'AMG',
            'IMU',
            'COMPASS',
            'M4G',
            'NDOF_FMC_OFF',
            #'NDOF'
        ],
        'flags': ['TEMPERATURE']
    }

    # Data type of values
    _dataType = 'Range'

    # Data range for values
    _dataRange = []

    # Value to set
    _currentValue = 0

    # Value history
    _values = None

    # Mode
    _mode = None

    # Duty frequency
    _dutyFrequency = None

    # Flags
    _flags = None

    # Frequency for the thread
    _frequency = '10 Hz'

    # Period for the thread
    _period = 0.1

    # Thread active flag
    _threadActive = False

    # Thread for the inner loop
    _thread = None

    # Duration needed for an update cycle
    _cycleDuration = 0


    def __init__(self, channel, muxedChannel = None, ADRSet = False):
        """Device supports an address pin, one can represent this with a 'True' value of ADRSet."""
        self._channel = channel                                 # Set pin
        self._muxedChannel = muxedChannel                       # Set muxed pin

        self._values = []                                       # Set empty values array

        self._mode = self._settings['modes'][0]                 # Set default mode
        #########################################################
        # self._mode = self._settings['modes'][<NDOF_INDEX>]    # USE THIS LINE FOR NDOF
        #########################################################
        self._flags = []                                        # Set default flag list

        # self._bno = BNO055_DRIVER.BNO055(rst='P9_12')         # Use that line for hardware reset pin
                                                                # otherwise software reset is used
        self._bno = BNO055_DRIVER.BNO055(address=ADDRESS_1,busnum=BUSNUM) # Create the driver object
        try:
            self._connected = self._bno.begin()                 # Connect to the device
            #####################################################
            # self._connected = self._bno.begin(MODE_MAP[self._mode]) # USE THIS LINE FOR NDOF
            #####################################################
        except IOError:
            self._connected = False

    def cleanup(self):
        """Clean up driver when no longer needed."""
        self._connected = False                                 # Device disconnected
        self._threadActive = False                              # Unset thread active flag

    def getDeviceConnected(self):
        """Return True if the device is connected, false otherwise."""
        try:
            status, self_test, error = self._bno.get_system_status(False) # Get status
            self._connected = (error == 0)                      # Device is connected and has no error
        except IOError:
            self._connected = False                             # Device disconnected
        return self._connected

    def configureDevice(self):
        """Once the device is connected, it must be configured."""
        try:
            self._bno.set_mode(MODE_MAP[self._mode])            # Set device as to default mode
        except:                                                 # Device disconnected in the meantime
            raise IOError('Error on i2c device while switching mode')
        self._threadActive = True                               # Set thread active flag
        self._thread = threading.Thread(target=self._loop, name=self._name) # Create thread
        self._thread.daemon = True                              # Set thread as daemonic
        self._thread.start()                                    # Start thread

    def _loop(self):
        """Inner loop of the driver."""
        while True:
            beginT = time.time()                                # Save start time of loop cycle

            acc = [None,None,None]
            mag = [None,None,None]
            gyr = [None,None,None]
            eul = [None,None,None]
            qua = [None,None,None,None]
            tem = [None]
            if self._mode in ['ACCONLY', 'ACCMAG', 'ACCGYRO', 'AMG', 'IMU', 'COMPASS', 'M4G', 'NDOF_FMC_OFF', 'NDOF']:
                acc = list(self._bno.read_accelerometer())      # Get acc data
            if self._mode in ['MAGONLY', 'ACCMAG', 'MAGGYRO', 'AMG', 'COMPASS', 'M4G', 'NDOF_FMC_OFF', 'NDOF']:
                mag = list(self._bno.read_magnetometer())       # Get mag data
            if self._mode in ['GYRONLY', 'ACCGYRO', 'MAGGYRO', 'AMG', 'IMU', 'NDOF_FMC_OFF', 'NDOF']:
                gyr = list(self._bno.read_gyroscope())          # Get gyr data
            if self._mode in ['IMU', 'COMPASS', 'M4G', 'NDOF_FMC_OFF', 'NDOF']:
                eul = list(self._bno.read_euler())              # Get eul data
            if self._mode in ['IMU', 'COMPASS', 'M4G', 'NDOF_FMC_OFF', 'NDOF']:
                qua = list(self._bno.read_quaternion())         # Get qua data
            if 'TEMPERATURE' in self._flags:
                tem = [self._bno.read_temp()]                   # Get tem data
            self._currentValue = acc + mag + gyr + eul + qua + tem

            self._values.append([time.time(), self._currentValue]) # Save timestamp and value

            endT = time.time()                                  # Save start time of loop cycle
            deltaT = endT - beginT                              # Calculate time used for loop cycle
            self._cycleDuration = deltaT                        # Save time needed for a cycle
            if (deltaT < self._period):
                time.sleep(self._period - deltaT)               # Sleep until next loop period

            if not self._threadActive:                          # Stop the thread
                return

    def getValues(self, clear=True):
        """Get values for the i2c device."""
        if self._values == None:                                # Return empty array for no values
            return []
        values = self._values[:]                                # Get the values
        if clear:
            self._values = []                                   # Reset values
        return values                                           # Return the values


    def getDevice(self):
        """Return device name."""
        return self._name

    def getName(self):
        """Return device name."""
        if self._muxedChannel == None:
            return '{}@I2C[{}]'.format(self._name, self._channel)
        else:
            return '{}@I2C[{}:{}]'.format(self._name, self._channel, self._muxedChannel)

    def getDir(self):
        """Return device direction."""
        return self._dir

    def getDim(self):
        """Return device dimension."""
        return self._dim

    def getDimMap(self):
        """Return device dimension map."""
        return self._dimMap[:]

    def getChannel(self):
        """Return device channel."""
        return self._channel

    def getMuxedChannel(self):
        """Return device muxed channel."""
        return self._muxedChannel

    def getAbout(self):
        """Return device settings."""
        return {
            'info': self._info,
            'dimMap': self._dimMap[:],
            'dimUnit': self._dimUnit[:],
            'dataType': self._dataType,
            'dataRange': self._dataRange[:]
        }

    def getSettings(self):
        """Return device settings."""
        return self._settings

    def getCycleDuration(self):
        """Return device cycle duration."""
        return self._cycleDuration

    def getMode(self):
        """Return device mode."""
        return self._mode

    def setMode(self, mode):
        """Set device mode."""
        if (mode in self._settings['modes']):
            self._mode = mode
            try:
                self._bno.set_mode(MODE_MAP[self._mode])            # Set device to mode
            except:                                                 # Device disconnected in the meantime
                raise IOError('Error on i2c device while switching mode')
        else:
            raise ValueError('mode {} is not allowed'.format(mode))

    def getFlags(self):
        """Return device mode."""
        return self._flags[:]

    def getFlag(self, flag):
        """Return device mode."""
        return self._flags[flag]

    def setFlag(self, flag, value):
        """Set device flag."""
        if (flag in self._settings['flags']):
            if value:
                self._flags.append(flag)                            # Add the flag
            else:
                self._flags.remove(flag)                            # Remove the flag
        else:
            raise ValueError('flag {} is not allowed'.format(flag))

    def getFrequency(self):
        """Return device frequency."""
        return self._frequency

    def setFrequency(self, frequency):
        """Set device frequency."""
        if (frequency in self._settings['frequencies']):
            self._frequency = frequency
            self._period = 1./int(self._frequency[:-3])
        else:
            raise ValueError('frequency {} is not allowed'.format(frequency))

    def getDutyFrequency(self):
        """Return device duty frequency."""
        return self._dutyFrequency

    def setDutyFrequency(self, dutyFrequency):
        """Set device duty frequency."""
        raise ValueError('duty frequency {} is not allowed'.format(dutyFrequency))
