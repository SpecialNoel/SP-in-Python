import socket

if __name__ == '__main__':
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP

    clientSocket.connect(('127.0.0.0', 17990))

    clientSocket.send(b'This is client\n')

    response = clientSocket.recv(1024)

    clientSocket.close()

    print(f'From Server: {response.decode()}')

    print('Client disconnects')