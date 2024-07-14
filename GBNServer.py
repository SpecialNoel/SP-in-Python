# GBNServer.py

import zlib
import struct
from socket import *
from pathlib import Path

# --------------------------------------------------------------------------------------------------

# Get the size (int) of a string file
def get_file_size(filename):
    return Path(filename).stat().st_size

# Read message from a byte file
def read_file_content(filename):
    message = ''
    
    # Read all bytes from the input file
    with open(filename, 'rb') as bf:
        message = bf.read()
        
    return message

# --------------------------------------------------------------------------------------------------

def create_server_socket():
    global serverName, serverPort
    
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((serverName, serverPort))
    
    return serverSocket

def udt_send(data, clientName, clientPort):
    global serverSocket
    
    serverSocket.sendto(data, (clientName, clientPort))
    
    return

def udt_rcv():
    global serverSocket, MAX_REQUEST_SIZE
    
    response, (clientName, clientPort) = serverSocket.recvfrom(MAX_REQUEST_SIZE)
    
    return response, (clientName, clientPort)

# --------------------------------------------------------------------------------------------------

# Generate an unsigned int of 32-bit (or 4 bytes) checksum for the payload
def generate_checksum(payload):
    return zlib.crc32(payload)



if __name__=='__main__':
    MAX_REQUEST_SIZE = 1024
    
    serverName = '127.0.0.1' # localhost
    serverPort = 17990 # random number
    
    serverSocket = create_server_socket()
    
    
