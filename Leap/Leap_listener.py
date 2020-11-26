import math
import numpy as np
from leap import Leap, Mouse
import time

import csv
import socket
import struct
import time
from pyquaternion import Quaternion

MESSAGE_SIZE_PER_HAND = 3

class Control_Listener(Leap.Listener):  #The Listener that we attach to the controller.  This listener is for palm
                                        #tilt movement
    def __init__(self, verbose):
        super(Control_Listener, self).__init__()  #Initialize like a normal listener
        self.verbose = False
        self.data = [None] * MESSAGE_SIZE_PER_HAND  # Empty Message for 2 hands.
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
        self.left_detected = False
        self.right_detected = False

        
        ## Get first frame of when a hand is detected
        #if (self.hands_first_frames[0] is None):
        #    for hand in frame.hands:
        #        if hand.is_right:
        #            self.right_detected = True
        #            if type(self.hands_first_frames[0])!=type(frame):
        #                self.hands_first_frames[0] = frame
        #        elif hand.is_left:
        #            self.left_detected = True
        #            if type(self.hands_first_frames[1])!=type(frame):
        #                self.hands_first_frames[1] = frame
        ## Delete it if no hand is detected
        #else:
        #    for hand in frame.hands:
        #        if hand.is_right:
        #            self.right_detected = False
        #            self.hands_first_frames[0] = None
        #        if hand.is_left:
        #            self.left_detected = False
        #            self.hands_first_frames[1] = None
        

        for hand in frame.hands:
            if hand.is_right:
                self.right_detected = True
                if type(self.hands_first_frames[0])!=type(frame):
                    self.hands_first_frames[0] = frame
                    print "Right hand first frame set"
            elif hand.is_left:
                self.left_detected = True
                if type(self.hands_first_frames[1])!=type(frame):
                    self.hands_first_frames[1] = frame

        if not(self.right_detected):
            self.hands_first_frames[0] = None
        if not(self.left_detected):
            self.hands_first_frames[1] = None

        #print(self.hands_first_frames)
        #print('\n')
        #print("Hand(s) detected : {}".format(nbHands))
        self.create_data(frame)
        print(str(len(self.data)))
        print(self.data)
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
                    '''
                    print("\t Palm velocity : {}".format(hand.palm_velocity))
                    print("\t Vector Normal to the palm : {}".format(hand.palm_normal))
                    print("\t Vector pointing from the center of the palm to the fingers : {}".format(hand.direction))
                    print("\t Palm pitch : {}".format(hand.direction.pitch))
                    print("\t Palm roll : {}".format(hand.direction.roll))
                    print("\t Palm yaw : {}".format(hand.direction.yaw))
                    print("\t Wrist is at position : {} (Not super useful I guess)".format(hand.wrist_position))
                    listFingers = hand.fingers

                    print("\t Detected {} fingers".format(len(listFingers)))
                    for finger in listFingers:
                        print("\t\t Finger Id {}".format(finger.id))
                        for b in range(4):
                            bone = finger.bone(b)
                            print("\t\t Bone in finger {}; Center in position {}; Direction {}".format(finger.id,bone.center,bone.direction))
                    '''
    ###################################################

    def create_data(self, frame):
        if not frame.hands.is_empty:  #Make sure we have some hands to work with
            for hand in frame.hands:
                self.data_temp = []
                first_frame = self.hands_first_frames[0]
                #else:
                #    first_frame = self.hands_first_frames[1]
                #self.one_hand_data(hand,first_frame)
                #self.process_data()

                self.data_temp.append(hand.is_right)
                self.data_temp.append(toVector3(hand.palm_position))
                self.data_temp.append(hand.grab_strength)
                while (len(self.data_temp) < MESSAGE_SIZE_PER_HAND):
                    self.data_temp.append('f')

                #self.data_temp.append(toVector3(hand.rotation_matrix(first_frame).x_basis))


                if hand.is_right:
                    self.data[0:MESSAGE_SIZE_PER_HAND] = self.data_temp    # TODO change the values
                    
                else:
                    self.data[MESSAGE_SIZE_PER_HAND:MESSAGE_SIZE_PER_HAND * 2] = self.data_temp

    ###################################################
    # [Ludovic] Function to treat the data: recognize rotation based on
    # fingertips
    def one_hand_data(self,hand,first_frame):
        self.data_temp.extend(toVector3(hand.palm_position))
        rot_matrix = np.array([toVector3(hand.rotation_matrix(first_frame).x_basis),toVector3(hand.rotation_matrix(first_frame).y_basis),toVector3(hand.rotation_matrix(first_frame).z_basis)])
        q,r = np.linalg.qr(rot_matrix)
        q[:,0] *= np.sign(r[0,0])
        q[:,1] *= np.sign(r[1,1])
        q[:,2] *= np.sign(r[2,2])
        rot_matrix = q   # We make sure the rotation matrix is orthogonal
        # print(Quaternion(matrix=rot_matrix))
                              # print("\n")
        y = np.cross(toVector3(hand.direction), toVector3(hand.palm_normal))
        rot_matrix_bis = np.resize(np.concatenate((y,toVector3(hand.palm_normal),toVector3(hand.direction))),(3,3))
        rot_matrix_bis = np.multiply(np.transpose(rot_matrix_bis),[[-1,1,1],[1,-1,1],[1,1,-1]])
        q,r = np.linalg.qr(rot_matrix_bis)
        q[:,0] *= np.sign(r[0,0])
        q[:,1] *= np.sign(r[1,1])
        q[:,2] *= np.sign(r[2,2])
        rot_matrix_bis = q   # We make sure the rotation matrix is orthogonal

        rot_matrix = rot_matrix_bis

        try:
            quat_order = [3,1,2,0]
            quat_temp = Quaternion(matrix=rot_matrix).elements
            self.data_temp.extend([quat_temp[x] for x in quat_order])
        except:
            print("Matrix is not orthogonal")
            self.data_temp.append(np.array([0,0,0,1]))

        for finger in hand.fingers:
            for b in range(4):
                if not(finger.type == 0) or not(b == 0):
                    #print(finger.bone(b).center)
                    self.data_temp.extend(toVector3(finger.bone(b).center))
                    # Create a rotation matrix from hand to each bone and
                    # associate it a quaternion
                    #rot =
                    #rotation_matrix_from_vectors(toVector3(hand.direction),toVector3(finger.bone(b).direction))
                    rot = RotationMatrixFromBasis(finger.bone(b).basis)
                    q,r = np.linalg.qr(rot)
                    rot_matrix_bis = q   # We make sure the rotation matrix is orthogonal
                    rot = rot_matrix_bis

                    quat_temp = Quaternion(matrix=rot).elements
                    # print(str(quat_temp) + '\t' + str(self.data_temp[3:7]))
                    quat_order = [3,2,1,0]
                    self.data_temp.extend(quat_temp)

    ###################################################

    def process_data(self):
        processed_data = []
        for element in self.data_temp:
            if type(element) == type(np.array([])):
                for data in element:
                    processed_data.append(data)
            else:
                processed_data.append(element)
            ## TODO concatenate data to make the code clearer
            print("Only one data")
            print(element)
            print("\n")
        self.data_temp = processed_data

    ###################################################

    def send_udp_data(self):
        MESSAGE = str(self.data)
        # We need to pack the data to send it
        #strs = "fffffff" # Palm position and quaternion
        #for i in range(19): # All bones position and quaternions
        #    strs += 'fffffff'
        ## strs += 'i'
        #strs = strs + strs
        
        #MESSAGE = struct.pack(strs, *self.data)
        self.sock.sendto(MESSAGE, (self.UDP_IP, self.UDP_PORT))
        print("Data sent")

    ###################################################

    def save_data(self):
        if self.data != []:
            f = open('data.csv', 'a')
            with f:
                writer = csv.writer(f)
                writer.writerow(self.data)
            f.close()

    ###################################################
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
