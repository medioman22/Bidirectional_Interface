
import select
import socket
import time

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

UDP_IP = socket.gethostname()
# local ip of the client computer. Do not change this ip.
LOCAL_IP = "127.0.0.1"

# port to which the data is being received.
UDP_PORT_RIGID_BODIES = 5001

# Bind a UDP socket to this port
rigid_bodies_socket = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
rigid_bodies_socket.bind((UDP_IP, UDP_PORT_RIGID_BODIES))

# socket to send to unity
unity_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
unity_port = 26000

while True:
    # read data from the proxy
    rigid_bodies = get_data(rigid_bodies_socket)
    if len(rigid_bodies):
        print("acquired rigid bodies, total number = ", len(rigid_bodies))

        for i in rigid_bodies:
            # send the data to unity
            unity_socket.sendto(i, (LOCAL_IP, unity_port))
    time.sleep(1e-3)
