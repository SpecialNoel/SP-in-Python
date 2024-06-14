# Echo

## How to Run the programs
*Note: To execute programs in this folder, make sure you have Python version 3 or higher installed.

Step 1: Open two new terminals.

Step 2: Start the server side program by typing in the following commands on one of the terminals: 
```
python3  EchoServer.py
```

Step 3: Start the client side program by typing in the following commands on the other terminal:
```
python3  EchoClient.py
```

Step 4: Check the terminals to see the outputs. It should act exactly like what the ```echo``` does, that output shown on the terminal will be the same as user input.

Notice 1: the server side program has to be executed before the client side program because the server socket created in the server side program will first need to call the 
socket methdo ```listen()``` to enable the server socket be connected with other client sockets. Thus, having the client side program executed first will lead to 
```ConnectionRefusedError: [Errno 61] Connection refused```.

Notice 2: there can only be one ```EchoServer.py``` program running concurrently because the server socket created in the program will occupy the same IP address and port number.
Thus, having more than one ```EchoServer.py``` program running in the same time will lead to ```OSError: [Errno 48] Address already in use```.

There can be as many client programs running concurrently, however. To create and connect with more clients, simply open more terminals, 
and repeat the process to start the client program on each of the new terminals.
```
python3  EchoClient.py
```

## Version 1.0.0
Functionalities are not fully done yet. Specifically:
1. Both input in client side program and output in server side program are hard-coded.
2. The server socket will close once it receives an empty byte object (b'') from any of the connected client sockets.
3. The server side program will be terminated immediately after any of the connected client sockets closes.
4. There can be only one client since both the first client and the server socket close and their programs terminate after their works are done.

