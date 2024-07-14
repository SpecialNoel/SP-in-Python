# GBNClient.py

import zlib
import struct
from socket import *

# --------------------------------------------------------------------------------------------------

def create_client_socket():    
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    
    return clientSocket

def udt_send(data):
    global clientSocket, serverName, serverPort
    
    clientSocket.sendto(data, (serverName, serverPort))
    
    return

def udt_rcv():
    global clientSocket
    
    response = clientSocket.recvfrom(MAX_REQUEST_SIZE)[0]
    
    return response

# --------------------------------------------------------------------------------------------------

# Generate an unsigned int of 32-bit (or 4 bytes) checksum for the payload
def generate_checksum(payload):
    return zlib.crc32(payload)

def send_syn_packet():
    udt_send()
    
# Deliver data by appending payload to a byte file
def deliver_data(payload, filename):
    with open(filename, 'ab') as bf:
        bf.write(payload)

    return

if __name__=='__main__':
    MAX_REQUEST_SIZE = 1024
    
    serverName = '127.0.0.1' # localhost
    serverPort = 17990 # random number
    
    clientSocket = create_client_socket()
    

    
    clientSocket.close()