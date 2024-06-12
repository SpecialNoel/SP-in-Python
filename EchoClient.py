# EchoClient.py

import socket

# host is the IP address of the server we will be connecting to
host = '127.0.0.1' 
# port is the port number of the server we will be connecting to
port = 65432

# Use "with ... as ..." statement here to handle possible exceptions
# Also, when using this statement, there is no need to manually close the clientSocket
# socket.AF_INET means that it has a host with an IPv4 address, and a port number which is an integer
# socket.SOCK_STREAM means that the protocol used is TCP (Transmission Control Protocol)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    print('Client socket created')
    # connect() establishs connection between the clientSocket and server socket
    clientSocket.connect((host, port))
    print('Connected with server socket')
    # sendall() allows the clientSocket to send bytes of data to the connected server socket
    clientSocket.sendall(b'Hello, world')
    # recv(1024) allows the clientSocket to receive up to 1024 bytes of data sent by the connected server socket
    dataReceived = clientSocket.recv(1024)

print('Client socket closed')

# Unlike the script for the server socket, the "with...as..." statement here only executes once,
#   and upon completion clientSocket will be closed
# After clientSocket closes, print out the byte data received from connected server socket
# We still have access to dataReceived since the "with" statement does not create a scope
print(f'Received from server: {dataReceived!r}')
