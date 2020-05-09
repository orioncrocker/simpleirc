################################################################################################
# Author: Orion Crocker
# Filename: server.py
# Date: 05/08/20
# 
# Server
# 	Test server
################################################################################################

import socket
import sys

port = 2000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ''
sock.bind((host, port))

sock.listen(1)
print('Listening on port ' + str(port))

connection, address = sock.accept()
print('Client ' + str(address[1]) + ' connected to server from ' + str(address[0]))

data = connection.recv(1024)
message = data.decode()
print(message)

connection.send(data)

connection.close()
