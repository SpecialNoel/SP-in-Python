# Echo
_Echo is a Client-Server architecture, where client sends string/binary input to server, and server reports back to client what it received._

**Note**: To execute programs in this folder, make sure you have Python version 3.6 or higher installed.

**Notice 1**: server program has to be executed before client program because server socket created in server program will first need to call the socket method ```listen()``` to enable server socket start listening to connections established by client sockets (not yet accept any, just open for connection). Thus, having client programs executed first will lead to  ```ConnectionRefusedError: [Errno 61] Connection refused```.

**Notice 2**: there can only be one server program running concurrently because server socket created in server program will occupy the same IP address and port number. Thus, having more than one server program running in the same time will lead to ```OSError: [Errno 48] Address already in use```.

There can be as many client programs running concurrently, however. To create and connect with more clients, simply open more terminals, 
and repeat the process to start client program on each of the new terminals.

<br/><br/>

## Version 1.1.0
Echo version 1.1.0 contains two files: ```MultiConnEchoServer.py``` and ```MultiConnEchoClient.py```.

## How to Run programs in Version 1.1.0

Step 1: Open two new terminals.

Step 2: Start the server program by typing in the following commands on one of the terminals: 
```
python3 MultiConnEchoServer.py *server_ip_address* *server_port_number*
```
Example command for starting server program:
```
python3 MultiConnEchoServer.py 127.0.0.1 65432
```

Step 3: Start the client program by typing in the following commands on the other terminal:
```
python3 MultiConnEchoClient.py *server_ip_address* *server_port_number* *number_of_clients*
```
Example command for starting client program:
```
python3 MultiConnEchoClient.py 127.0.0.1 65432 2
```

Step 4: Check the terminals to see the outputs. 

Step 5: These connections between client sockets and server socket are then closed.

Step 6: Client program is terminated (finished), while server program remaining opening. While server is still up, you can create more client sockets and connect them with the same server socket by running client program again with the same commands:
```
python3 MultiConnEchoClient.py *server_IP_address* *server_port_number* *number_of_clients*
```

Fixed bugs in Version 1.1.0, compared to Version 1.0.0:
1. Server program stays up after serving more than one client program.
2. One server socket can be connected with and serve multiple client sockets concurrently.

Existing bugs in Echo Version 1.1.0:
1. Inputs (IP addresses and port numbers for both programs) and output (stated in ```MultiConnEchoClient.py```) are not flexible (hard-coded).
2. Both server and client will "freeze" if the output messages stated in ```MultiConnEchoClient.py``` contains b'' (the empty byte object) as one of the message, thus resulting the programs not functioning right.

<br/><br/>

## Version 1.0.0
Echo version 1.0.0 contains two files: ```EchoServer.py``` and ```EchoClient.py```.

## How to Run programs in Version 1.0.0

Step 1: Open two new terminals.

Step 2: Start server program by typing in the following commands on one of the terminals: 
```
python3  EchoServer.py
```

Step 3: Start client program by typing in the following commands on the other terminal:
```
python3  EchoClient.py
```

Step 4: Check the terminals to see the outputs.

Existing bugs in Echo Version 1.0.0:
1. Inputs (IP addresses and port numbers for both programs) and output (b'Hello, world', stated in ```EchoClient.py```) are not flexible (hard-coded).
2. Both server and client will "freeze" if the output message stated in ```EchoClient.py``` is b'' (the empty byte), thus resulting the programs not functioning right.
3. Server program will be terminated immediately after any of the connected client sockets closes.
4. Only one client will be served by server concurrently, since client and server socket will close and their programs will terminate upon having their works done.
