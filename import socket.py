import socket
import struct
import time

class Datagram:
    def __init__(self, data):
        self.version = int(data[4:6].decode())
        self.header = Header(struct.unpack('>IBBIBBBBHH', data[6:24]))


class Header:
    def __init__(self, header):
        self.sample_counter = header[0]  # Amount of measurements token since start
        self.datagram_counter = header[
            1]  # Datagram number (if it is the last datagram of the measurement this number is high)
        self.item_counter = header[2]  # Amount of items (point/segments)
        self.clock = header[3]  # Time since start measurement
        self.char_counter = header[4]  # Amount of people recorded at the same time
        self.number_of_body_segments = header[5]  # number of body segments measured
        self.props = header[6]  # Amount of property sensors
        self.finger_data_segments = header[7]  # Number of finger data segments
        self.payload = header[9]  # Size of the measurement excluding the header


class Body:
    def __init__(self, data):
        self.pelvis = self.get_joint_data_by_id(data, id=1)
        self.head = self.get_joint_data_by_id(data, id=6)

    def get_joint_data_by_id(self, data, id):
        decoded_data = struct.unpack('>IIfff', data[(id - 1) * 20 + 24: id * 20 + 24])
        return BodyPart(decoded_data)


class BodyPart:
    def __init__(self, decoded_data):
        self.parent_id = decoded_data[0]
        self.child_id = decoded_data[1]
        self.x_rot = decoded_data[2]
        self.y_rot = decoded_data[3]
        self.z_rot = decoded_data[4]


UDP_IP = "127.0.0.1"
UDP_PORT = 9763

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

i=0
while True:
    i+=1
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    body = Body(data)
    d = Datagram(data)
    # print(body.head.x_rot, body.head.y_rot, body.head.z_rot)
    if i%10==0:
        print(body.head.x_rot, body.head.y_rot, body.head.z_rot)