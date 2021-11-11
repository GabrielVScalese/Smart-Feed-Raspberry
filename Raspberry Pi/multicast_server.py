import struct 
import socket
import _thread
import time

host = '239.255.255.250'
port = 1900

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

class MulticastServer:

    def __init__(self):
        self.host = '239.255.255.250'
        self.port = 1900

    def run (self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.bind((self.host, self.port))
        except:
            sock.bind(('', self.port))

        print('Multicast ouvindo na porta ' + str(self.port) + '\n')
        mreq = struct.pack("4sl", socket.inet_aton(self.host), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
        while True:
            (data, address) = sock.recvfrom(12000)
            if data:
                message = data.decode()
                print(message)
                if message.__contains__('M-SEARCH'):
                    sock.sendto(f'{ip};{5000}'.encode(), address)
    