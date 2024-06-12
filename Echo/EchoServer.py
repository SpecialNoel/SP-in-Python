# EchoServer.py

import socket

# host is the IP address of this echo server
# '127.0.0.1' is the standard loopback interface address (localhost)
host = '127.0.0.1' 
# port is the port number of this echo server
# Non-privileged ports are > 1023
port = 65432

# Use "with ... as ..." statement here to handle possible exceptions
# Also, when using this statement, there is no need to manually close the serverSocket
# socket.AF_INET means that it has a host with an IPv4 address, and a port number which is an integer
# socket.SOCK_STREAM means that the protocol used is TCP (Transmission Control Protocol)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    print('Server socket created')
    # bind() allows the serverSocket to have host and port as its ip address and port number
    serverSocket.bind((host, port))
    # listen() enables the serverSocket to be connected with client sockets
    serverSocket.listen()
    print('Waiting for connection established by client socket')
    # accept() allows the serverSocket to accept the connection initiated by a client socket
    # conn is a new socket object (a sub socket created by the serverSocket), 
    #   which can be used to send and receive data, to or from the connected client socket
    # address is the address bound to the connected client socket
    (conn, address) = serverSocket.accept()
    # If the new socket object created for the connection with the client socket exists, then:
    with conn:
        print(f'Connected with client socket: {address}')
        # Continously receiving and sending data to the client socket, 
        #   until nothing is sent by the client socket
        while True:
            # Block and try to receive up to 1024 bytes of data from the connected client socket
            # This function will remain blocked (cannot proceed to the next line),
            #   until it receives at least 1 byte from the connected client socket
            receivedData = conn.recv(1024)
            # Break from this infinite loop and close this connection
            #   if conn received the empty bytes object (b'') from the connected client socket
            if not receivedData:
                break
            # Otherwise, conn it will send all of what it received currently
            #   to the connected client socket, thus resulting the "echo" effect
            conn.sendall(receivedData)

print('Server socket closed')
