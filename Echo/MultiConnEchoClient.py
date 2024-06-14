# MultiConnEchoClient.py

# Example commands to run this program: python3 MultiConnEchoClient.py 127.0.0.1 65432 2
# *Note: The server side program (MultiConnEchoServer.py) has to run first

import sys
import socket
import selectors
import types

# Start establishing connections to the server socket for num_conns number of client sockets
# num_conns is read from the command-line and is the number of connections to create to the server.
def start_connections(host, port, num_conns, selector, messages):
    # Server socket IP address and port number initialized
    server_addr = (host, port)

    # Do the following process for each client socket
    for i in range(0, num_conns):
        # Give this client socket an id for identification
        connid = i + 1
        print(f"\nClient establishes connection {connid} to {server_addr}")

        # socket.AF_INET means that it has a host with an IPv4 address, and a port number which is an integer
        # socket.SOCK_STREAM means that the protocol used is TCP (Transmission Control Protocol)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # setblocking(False) makes this client socket no longer block
        sock.setblocking(False)

        # Connect this client socket with the server socket using .connect_ex()
        # We use .connect_ex() here instead of .connect() because .connect() would immediately raise a BlockingIOError exception 
        #   (since .connect() should be used under a blocking environment). 
        # The .connect_ex() method initially returns an error indicator, errno.EINPROGRESS, 
        #   instead of raising an exception that would interfere with the connection in progress
        sock.connect_ex(server_addr)
        
        # events can either be selectors.EVENT_READ or selectors.EVENT_WRITE since the socket is ready for reading and writing
        events = selectors.EVENT_READ | selectors.EVENT_WRITE

        # More information on types.SimpleNamespace can be found in MultiConnEchoServer.py
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            messages=messages.copy(),
            outb=b'',
        )

        # .register() registers this client socket to be monitored with selector.select()
        # For this client socket, it would want read events: selectors.EVENT_READ or selectors.EVENT_WRITE
        # data will store what's being sent and received on this client socket
        selector.register(sock, events, data=data)

# Perform services on the connection between the client socket and the server socket
# key contains the socket object (fileobj) and data object
# mask contains the events that are ready
# selector is registered with the client socket and events: selectors.EVENT_READ OR selectors.EVENT_WRITE
def serve(key, mask, selector):
    socket = key.fileobj
    data = key.data

    # Handle reading event if the socket is ready for reading
    if mask & selectors.EVENT_READ:
        recv_data = socket.recv(1024)

        # If there are data received
        if recv_data:
            # Client side keeps track of the number of bytes it received from the server so that it can close its side of the connection
            # When the server detects this, it closes its side of the connection too
            data.recv_total += len(recv_data)
            print(f"\nClient receives message: {recv_data!r} from connection {data.connid}")

        # If there are no data received, it means that the server side wants to close the connection with this client socket
        if not recv_data or (data.recv_total == data.msg_total):
            # Remove this client socket from selector.select()
            selector.unregister(socket)

            # After unregistering, close this client socket (thus the connection with the server socket is fully closed)
            socket.close()
            print(f"\nClient closes connection to {data.connid}")

    # Handle writing event if the socket is ready for writing
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
            
        if data.outb:
            # Any received data stored in data.outb is sent to the server socket using sock.send()
            # The .send() method returns the number of bytes sent. 
            # This number can then be used with slice notation on the .outb buffer to discard the bytes sent.
            sent = socket.send(data.outb)  # Should be ready to write to the server socket
            print(f"\nClient sends message: {data.outb!r} to connection {data.connid}")

            # After sending the stored data to the server socket, remove the sent bytes from the send buffer
            data.outb = data.outb[sent:]

def start_serving_connection(selector):
    try:
        # The client side program should keep running until an user keyboard input interrupt this program
        while True:
            # selector.select(timeout=1) blocks until there are sockets ready for I/O
            # It returns a list of tuples, one for each socket, with each tuple containing a key and a mask
            events = selector.select(timeout=1)

            if events:
                # key is a SelectorKey namedtuple that contains a fileobj attribute, with key.fileobject being a socket object
                # mask is an event mask of the operations that are ready
                for key, mask in events:
                    # Need to serve the connection by calling .serve()
                    serve(key, mask, selector)

            # Check for a socket being monitored to continue.
            if not selector.get_map():
                break
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        selector.close()

if __name__ == '__main__':
    # This ensures that this program will be ran with appropriate commands accompanied
    if len(sys.argv) != 4:
        print(f"Wrong command format. Usage: {sys.argv[0]} <host> <port> <num_connections>")
        sys.exit(1)

    # Client IP address and port number will be parsed from inputed commands
    host, port, num_conns = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    # Two binary messages used for testing in client's side program
    messages = [b"Message 1, sent by client. ", 
                b"Message 2, sent by client. "]

    # Introduce selector to handle multiple connection simultaneously
    selector = selectors.DefaultSelector()
    start_connections(host, port, num_conns, selector, messages)
    start_serving_connection(selector)
