
import select
import socket
import struct
import time

# function to get the data, before re-streaming it via send_data (proxy)
def get_data(my_socket):
    
    data = []
    
    # read data as long as packets are coming
    data_ready = False
    data_ready = select.select([my_socket],[],[],0)[0]
    
    while data_ready:
        t, _ = my_socket.recvfrom(1024) # buffer size is 1024 bytes
        
        data.append(t)
            
        data_ready = False
        data_ready = select.select([my_socket],[],[],0)[0]
        
    return data  

# function to send the data to client
def send_data(my_socket, data, data_type):
    if data_type == 'rb':
        # Pack the data to a stream of bytes
        message = struct.pack('%sf' % len(data), *data)
        # Send data to all clients
        for client_ip in CLIENT_IP_LIST:
            my_socket.sendto(message, (client_ip, CLIENT_PORT))


# local IP. Do not change that
UDP_IP = "127.0.0.1"
# socket to which data is being received
UDP_PORT_RIGID_BODIES = 9001

# open the receiving socket
rigid_bodies_socket = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
rigid_bodies_socket.bind((UDP_IP, UDP_PORT_RIGID_BODIES))
    
#############################################################################################
######## PUT THE IP TO THE CLIENT HERE. MAY CHANGE AT EACH RESTART OF THE COMPUTER ##########
CLIENT_IP_LIST = ["128.179.140.168", "128.179.195.151"] #####################################
#############################################################################################
#############################################################################################

# here the port you want to communicate to
CLIENT_PORT = 5001 

# No binding because we send with this socket (server)
send_socket = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP

while True:    
    # read data from receiving port
    rigid_bodies = get_data(rigid_bodies_socket)
    if len(rigid_bodies):
        print("acquired rigid bodies, total number = ", len(rigid_bodies))
        # now re-stream the acquired rigid bodies to the clients
        for i in rigid_bodies:
            # one int (index of rigid body) and 7 floats (x,y,z pos + quaternion)
            strs = 'ifffffff'
            # unpack. Useless thus far but usefull if we need to know the form of the data, hence keeping it.
            data_ump = struct.unpack(strs, i)
            # send data to client
            send_data(send_socket, data_ump, 'rb')
    time.sleep(1e-3)
