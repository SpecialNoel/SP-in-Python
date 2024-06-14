# MultiConnEchoServer.py

# Example commands to run this program: python3 MultiConnEchoServer.py 127.0.0.1 65432

import sys
import socket
import selectors
import types

# Accept the connection
def accept(socket, selector):
    # Accept connection established by a client socket
    conn, address = socket.accept()  # Should be ready to read since the listening socket was registered with selectors.EVENT_READ
    print(f"\nAccepted connection from {address}")
    # conn is a new socket object (a sub socket created by the serverSocket)
    #   which can be used to send and receive data, to or from the connected client socket
    # setblocking(False) to this sub socket will set it to non-blocking state
    # If it blocks, then the entire server is stalled until it returns. 
    # That means other sockets are left waiting even though the server isn’t actively working.
    conn.setblocking(False)

    # Credit for SimpleNamespace explanation: https://shorturl.at/Uo7B7
    # types.SimpleNamespace is similar to an empty class, except that it has several advantages:
    #   1. it allows you to initialize attributes while constructing the object
    #   2. it provides a readable .repr()
    #   3. it overrides the default comparison. Instead of comparing by .id(), it compares attribute values instead
    # data is the object that holds the data info we want to be included along with the socket
    data = types.SimpleNamespace(addr=address, inb=b"", outb=b"")
    # events can either be selectors.EVENT_READ or selectors.EVENT_WRITE since we want to know when the client connection is ready
    #   for readinig and writing
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    # .register() registers this sub socket to be monitored with selector.select()
    # For this sub socket, it would want read events: selectors.EVENT_READ or selectors.EVENT_WRITE
    # data will store what's being sent and received on this sub socket
    selector.register(conn, events, data=data)

# Serve the client socket
# key is a SelectorKey namedtuple returned from selector.select() that 
#   contains the socket object (fileobj) and data object
# mask contains the events that are ready
def serve(key, mask, selector):
    socket = key.fileobj
    # data will not be None upon entering this function
    data = key.data
    # Handle reading event if the socket is ready for reading
    if mask & selectors.EVENT_READ:
        recv_data = socket.recv(1024)  # Should be ready to read from the client socket
        # If there are data received
        if recv_data:
            # Append received data to data.outb to later sent it back to the client socket
            data.outb += recv_data
        else: 
            # If there are no data received, it means that the client side wants to close the connection with this sub socket
            print(f"\nClosing connection to {data.addr}")
            selector.unregister(socket)
            socket.close()
    # Handle writing event if the socket is ready for writing
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"\nEchoing {data.outb!r} to {data.addr}")
            # Any received data stored in data.outb is echoed to the client using sock.send()
            # The .send() method returns the number of bytes sent. 
            # This number can then be used with slice notation on the .outb buffer to discard the bytes sent.
            sent = socket.send(data.outb)  # Should be ready to write to the client socket
            # After sending the stored data to the client socket, remove the sent bytes from the send buffer
            data.outb = data.outb[sent:]

def setup_serverSocket():
    # This ensures that this program will be ran with appropriate commands accompanied
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <host> <port>")
        sys.exit(1)

    # Server IP address and port number will be parsed from inputed commands
    host, port = sys.argv[1], int(sys.argv[2])
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))
    serverSocket.listen()
    print(f"Listening on {(host, port)}")
    # setblocking(False) makes serverSocket no longer block
    # When used with selector.select(), it will wait for events on one or more sockets,
    #   and then read and write data when it's ready
    serverSocket.setblocking(False)
    return serverSocket

def setup_selector(serverSocket):
    # Introduce selector to handle multiple connection simultaneously
    selector = selectors.DefaultSelector()
    # .register() registers serverSocket to be monitored with selector.select()
    # For the listening socket, it would want read events: selectors.EVENT_READ
    # data will store what's being sent and received on serverSocket
    selector.register(serverSocket, selectors.EVENT_READ, data=None)
    return selector

def start_listen_connections(selector):
    try:
        # The server side program should keep running until an user keyboard input interrupt this program
        while True:
            # selector.select(timeout=None) blocks until there are sockets ready for I/O
            # It returns a list of tuples, one for each socket, with each tuple containing a key and a mask
            events = selector.select(timeout=None)
            # key is a SelectorKey namedtuple that contains a fileobj attribute, with key.fileobject being a socket object
            # mask is an event mask of the operations that are ready
            for key, mask in events:
                # If key.data is equal to None, then it is from the listening socket (see selector.register() above)
                # Need to accept the connection by calling .accept()
                if key.data is None:
                    accept(key.fileobj, selector)
                else:
                    # If key.data is not None, then it is a client socket that is already been accepted
                    # Need to serve the client socket by calling .serve()
                    serve(key, mask, selector)
    except KeyboardInterrupt:
        # Encountering user input [ctrl+c], thus breaking from the infinite loop of serving client sockets
        print("Caught keyboard interrupt, exiting")
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