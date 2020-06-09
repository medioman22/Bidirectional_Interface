from __future__ import absolute_import, division, print_function

import rospy
import serial

DEFAULT_PORT = '/dev/ttyACM0' #USB0
DEFAULT_BAUDRATE = 115200


class ClutchBase(object):

    def __init__(self, port=DEFAULT_PORT, baudrate=DEFAULT_BAUDRATE):
        try:
            self.serial = serial.Serial(port, baudrate)
        except serial.serialutil.SerialException:
            rospy.logerr('Port {} not found. Is the clutch connected via USB?'.format(port))
            exit()


class Clutch(ClutchBase):

    ON = '1'
    OFF = '0'

    def __init__(self, port=DEFAULT_PORT, baudrate=DEFAULT_BAUDRATE):
        super(Clutch, self).__init__(port=port, baudrate=baudrate)

    def set_state(self, engaged):
        """
        engaged: bool
        """
        message = self.ON if engaged else self.OFF
        self.serial.write(message)


class TwoClutches(ClutchBase):

    OFF = '0'	# 'a0\n' 'b0\n'
    ON1 = '1'	#'a1\n'
    ON2 = '2'  #'b1\n'

    def __init__(self, port=DEFAULT_PORT, baudrate=DEFAULT_BAUDRATE):
        super(TwoClutches, self).__init__(port=port, baudrate=baudrate)

    def set_state(self, state):
        """
        state: 0 (OFF), 1 (ON1), and 2 (ON2)
        """
        if state == 0:
            self.serial.write(self.OFF)
        elif state == 1:
            self.serial.write(self.ON1)
        elif state == 2:
            self.serial.write(self.ON2)
        else:
            raise RuntimeError('State {} invalid.'.format(state))
