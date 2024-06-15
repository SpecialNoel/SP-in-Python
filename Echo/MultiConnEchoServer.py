# MultiConnEchoServer.py

# Example commands to run this program: python3 MultiConnEchoServer.py 127.0.0.1 65432

import sys
import socket
import selectors
import types

# Accept the connection established by a client socket
# socket is serverSocket
# selector is registered with serverSocket and events: selectors.EVENT_READ
def accept(serverSocket, selector):
    # Should be ready to read since the listening socket was registered with selectors.EVENT_READ
    # conn is a new socket object (a sub socket created by the serverSocket)
    #   which can be used to send and receive data, to or from the connected client socket
    # For each client socket accepted, there will be one corresponding conn to be connected with it
    conn, address = serverSocket.accept()
    print(f'\nServer accepts connection from {address}')

    # setblocking(False) to conn will set it to non-blocking state
    # Reason to do so: if conn blocks, then the entire server is stalled until it returns. 
    # This means other sockets are left waiting even though the server isn’t actively working
    conn.setblocking(False)

    # Credit for SimpleNamespace explanation: https://shorturl.at/Uo7B7
    # .SimpleNamespace is similar to an empty class, except that it has several advantages
    # data is the object that holds the data info we want to be included along with the socket
    # Therefore, for every newly connected (accepted) client socket, there will be a corresponding data object
    # each data is initialized with the client socket's address, an empty binary input variable and an empty binary output variable
    data = types.SimpleNamespace(addr=address, inb=b'', outb=b'')

    # events should be selectors.EVENT_READ OR selectors.EVENT_WRITE 
    #   since we want to know when the client connection is ready for readinig and writing
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    
    # .register() registers conn to be monitored with selector.select()
    # conn would want these events: selectors.EVENT_READ OR selectors.EVENT_WRITE
    # data will store what's being sent and received by conn
    selector.register(conn, events, data)

# Perform services on the connection between conn and the client socket
# key contains the socket object (fileobj) and data object
# mask contains the events that are ready
# selector is registered with conn and events: selectors.EVENT_READ OR selectors.EVENT_WRITE
def serve(key, mask, selector):
    # Retrive socket object and data object from key
    socket = key.fileobj
    data = key.data

    # Handle reading event if the socket is ready for reading
    if mask & selectors.EVENT_READ:
        recv_data = socket.recv(1024)
        # If receiving data sent by client socket
        if recv_data:
            # Append received data to data.outb to later sent it back to the client socket (echo)
            data.outb += recv_data
        else: 
            # If there are no data received, it means that the client socket wants to close the connection with conn
            selector.unregister(socket)
            socket.close()
            print(f'\nServer closes connection to {data.addr}')

    # Handle writing event if the socket is ready for writing
    if mask & selectors.EVENT_WRITE:
        # Received data stored in data.outb, if any, is echoed to the client using sock.send()
        if data.outb:
            # The .send() method returns the number of bytes sent. 
            # This number can then be used with slice notation on the .outb buffer to discard the bytes sent.
            sent = socket.send(data.outb)
            print(f'\nServer echos message: {data.outb!r} to {data.addr}')
            
            # After sending the stored data to the client socket, clear the buffer by removing sent bytes
            data.outb = data.outb[sent:]

# Setup the server socket
def setup_serverSocket():
    # This ensures that this program will be ran with appropriate commands accompanied
    if len(sys.argv) != 3:
        print(f'Wrong command format. Usage: {sys.argv[0]} <host> <port>')
        sys.exit(1)

    # Server IP address and port number will be parsed from inputed commands
    host, port = sys.argv[1], int(sys.argv[2])

    # Create the server socket, call it serverSocket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))

    # Make serverSocket start listening to connections (not yet accept any, just open for connection)
    serverSocket.listen()
    print(f'Server listens on {(host, port)}')

    # When setblocking(False) is used with selector.select(), it will wait for events on one or more sockets,
    #   and then read and write data when it's ready
    serverSocket.setblocking(False)
    return serverSocket

# Setup the selector for serverSocket
def setup_selector(serverSocket):
    # Introduce selector to handle multiple connection simultaneously
    selector = selectors.DefaultSelector()

    # .register() registers serverSocket to be monitored with selector.select()
    # serverSocket would want read events: selectors.EVENT_READ
    # data will store what's being sent and received on serverSocket
    selector.register(serverSocket, selectors.EVENT_READ, data=None)
    return selector

# Accepting or Serving connections from client sockets
# selector is registered with serverSocket and events: selectors.EVENT_READ
def start_listen_connections(selector):
    try:
        # Keep running until an user keyboard input interrupt this program
        while True:
            # selector.select(timeout=None) blocks indefinitely until there are sockets ready for reading or writing events
            # It returns a list of tuples, one for each socket, with each tuple containing a key and a mask
            events = selector.select(timeout=None)

            for key, mask in events:
                # If key.data is equal to None, it means that key.fileobj is serverSocket (see setup_selector())
                # We need to accept the connection by calling .accept()
                if key.data is None:
                    accept(key.fileobj, selector)
                else:
                    # If key.data is not None, it means that key.fileobj is a client socket that has already been accepted
                    # We need to serve the client socket by calling .serve()
                    serve(key, mask, selector)
    except KeyboardInterrupt:
        # Encountering user input [ctrl+c], thus breaking from the infinite loop of serving client sockets
        print('Caught user keyboard interrupt, exiting')
    finally:
        # Upon encountering user keyboard interrupt, closes the selector and exits the program
        selector.close()

if __name__ == '__main__':
    # Setup a server socket
    serverSocket = setup_serverSocket()

    # Setup a selector that monitors that server socket
    selector = setup_selector(serverSocket)

    # Start accepting to connections established by client sockets and 
    #   serve them by echoing back messages they sent to the server socket
    start_listen_connections(selector)
