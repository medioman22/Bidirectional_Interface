from __future__ import absolute_import, division, print_function

import serial

DEFAULT_PORT = 'COM6' # 'COM9'  # USB0
DEFAULT_BAUDRATE = 115200


class ClutchBase(object):

    def __init__(self, port=DEFAULT_PORT, baudrate=DEFAULT_BAUDRATE):
        try:
            self.serial = serial.Serial(port, baudrate)
        except serial.serialutil.SerialException:
            print('Port {} not found. Is the clutch connected via USB?'.format(port))
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

    OFF = '0'  # 'a0\n' 'b0\n'
    ON1 = '1'  # 'a1\n'
    ON2 = '2'  # 'b1\n'

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


class FourClutches(ClutchBase):

    OFF = '0'.encode()
    ON1 = 'a'.encode()  
    ON2 = 'b'.encode()
    ON12 = 'c'.encode()
    ON3 = 'd'.encode()
    ON13 = 'e'.encode()
    ON23 = 'f'.encode()
    ON123 = 'g'.encode()
    ON4 = 'h'.encode()
    ON14 = 'i'.encode()
    ON24 = 'j'.encode()
    ON124 = 'k'.encode()
    ON34 = 'l'.encode()
    ON134 = 'm'.encode()
    ON234 = 'n'.encode()
    ON1234 = 'o'.encode()

    def __init__(self, port=DEFAULT_PORT, baudrate=DEFAULT_BAUDRATE):
        super(FourClutches, self).__init__(port=port, baudrate=baudrate)

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
        elif state == 3:
            self.serial.write(self.ON12)
        elif state == 4:
            self.serial.write(self.ON3)
        elif state == 5:
            self.serial.write(self.ON13)
        elif state == 6:
            self.serial.write(self.ON23)
        elif state == 7:
            self.serial.write(self.ON123)
        elif state == 8:
            self.serial.write(self.ON4)
        elif state == 9:
            self.serial.write(self.ON14)
        elif state == 10:
            self.serial.write(self.ON24)
        elif state == 11:
            self.serial.write(self.ON124)
        elif state == 12:
            self.serial.write(self.ON34)
        elif state == 13:
            self.serial.write(self.ON134)
        elif state == 14:
            self.serial.write(self.ON234)
        elif state == 15:
            self.serial.write(self.ON1234)
        else:
            raise RuntimeError('State {} invalid.'.format(state))

class FiveClutches(ClutchBase):

    OFF = '0'.encode()  # 'a0\n' 'b0\n'
    ON1 = '1'.encode()  # 'a1\n'
    ON2 = '2'.encode()  # 'b1\n'
    ON3 = '3'.encode()  # 'c1\n'
    ON4 = '4'.encode()  # 'd1\n'

    ON5 = '23'.encode()

    def __init__(self, port=DEFAULT_PORT, baudrate=DEFAULT_BAUDRATE):
        super(FiveClutches, self).__init__(port=port, baudrate=baudrate)

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
        elif state == 3:
            self.serial.write(self.ON3)
        elif state == 4:
            self.serial.write(self.ON4)
        elif state == 5:            
            self.serial.write(self.ON5)
        else:
            raise RuntimeError('State {} invalid.'.format(state))
