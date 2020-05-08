# header will go here

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ''
port = int(sys.argv[1])
sock.bind((host, port))

sock.listen(1)
connection, address = sock.accept()
print('Client ' + str(address) + ' connected to server')

data = connection.recv(1000000)

message = data.decode()
print(message)

connection.send(data)

connection.close()
