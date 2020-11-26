import math
import numpy as np
from leap import Leap, Mouse
import time

import csv
import socket
import struct
import time
from pyquaternion import Quaternion

MESSAGE_SIZE_PER_HAND = 4

class Control_Listener(Leap.Listener):  #The Listener that we attach to the controller.  This listener is for palm
                                        #tilt movement
    def __init__(self, verbose):
        super(Control_Listener, self).__init__()  #Initialize like a normal listener
        self.verbose = False
        self.data = [None] * MESSAGE_SIZE_PER_HAND * 2  # Empty Message for 2 hands.
        self.data_temp = []
        self.UDP_IP = "127.0.0.1"
        self.UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
        self.sock.sendto('t'.encode('utf-8'), (self.UDP_IP, self.UDP_PORT))
        self.hands_first_frames = [None,None]
        prev_frame = None
        print "In init"

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        self.sock.sendto('x', (self.UDP_IP, self.UDP_PORT))
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()  #Grab the latest 3D data
        nbHands = len(frame.hands)
        if nbHands == 0:
            print('No hands detected')
            self.data = ['t']

        else:
            self.create_data(frame)
            self.send_udp_data()
        #self.save_data()

        if self.verbose:
            if not frame.hands.is_empty:  #Make sure we have some hands to work with
                print("Detected {} hand(s)".format(nbHands))
                for hand in frame.hands:
                    if hand.is_right:
                        print("\t Right Hand : Hand Id {} ; Pose determined with confidence {} ; Visible for {:.4} s".format(hand.id,hand.confidence,hand.time_visible))
                    else:
                        print("\t Left Hand : Hand Id {} ; Pose determined with confidence {} ; Visible for {:.4} s".format(hand.id,hand.confidence,hand.time_visible))

                    # hand grasp: 0 = open -> 1 = closed
                    print("\t Scale : {}".format(hand.grab_strength))

                    print("\t Palm position : {}".format(hand.palm_position))

    ###################################################

    def create_data(self, frame):
        if not frame.hands.is_empty:  #Make sure we have some hands to work with
            self.data_temp = []

            hand = frame.hands[0]
            self.data_temp.append(hand.grab_strength)

                # Other values that might be interesting
                #self.data_temp.append(hand.is_right)
                #self.data_temp.append(toVector3(hand.palm_position))
                #self.data_temp.append(toVector3(hand.rotation_matrix(first_frame).x_basis))

                # Padding if ever necessary
                #while (len(self.data_temp) < MESSAGE_SIZE_PER_HAND):
                #    self.data_temp.append('f')

            self.data[0:MESSAGE_SIZE_PER_HAND*2] = self.data_temp
            #print(type(self.data[0]))

    ###################################################
    # Send the message
    def send_udp_data(self):
        MESSAGE = str(self.data)
        MESSAGE = MESSAGE.replace('[', '')
        MESSAGE = MESSAGE.replace(']', '')
        print(len(MESSAGE))
        print(MESSAGE)
        self.sock.sendto(MESSAGE, (self.UDP_IP, self.UDP_PORT))

    ###################################################
    # Save to csv file
    def save_data(self):
        if self.data != []:
            f = open('data.csv', 'a')
            with f:
                writer = csv.writer(f)
                writer.writerow(self.data)
            f.close()

    ###################################################
    # Utility functions (unused)
    def toVector3(leap_vector):
        return(np.array([leap_vector[0],leap_vector[1],leap_vector[2]]))

    def RotationMatrixFromBasis(basis):
        x = toVector3(basis.x_basis)
        y = toVector3(basis.y_basis)
        z = -toVector3(basis.z_basis)
        return(np.vstack([x,y,z]))

    def rotation_matrix_from_vectors(vec1, vec2):
        """ Find the rotation matrix that aligns vec1 to vec2
        :param vec1: A 3d "source" vector
        :param vec2: A 3d "destination" vector
        :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
        """
        a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
        v = np.cross(a, b)
        c = np.dot(a, b)
        s = np.linalg.norm(v)
        kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
        return rotation_matrix
