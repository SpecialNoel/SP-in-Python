import socket

if __name__ == '__main__':
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP

    serverSocket.bind('127.0.0.0', 17990) 

    serverSocket.listen()

    while True:
        conn, addr = serverSocket.accept()

        request = ''

        while True:
            data = conn.recv(1024)

            if not data: break

            request += data.decode()

            print(f'From Client: {request}')

            conn.send(b'This is Server\n')
        
        conn.close()

    print('Client has disconnected. Shutting down Server.')