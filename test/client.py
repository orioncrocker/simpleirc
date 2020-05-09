################################################################################################
# Author: Orion Crocker
# Filename: client.py
# Date: 05/08/20
# 
# Client
# 	Test client
################################################################################################

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server address
host = sys.argv[1]
# port server is listening on
port = int(sys.argv[2])

sock.connect((host, port))

message = sys.argv[3]
message = message.encode()
sock.send(message)
print('Sent ' + str(len(message)) + ' bytes\n')

while(1):
    data = sock.recv(10)
    if not data:
      break 

    message = data.decode()
    print("'" + message + "'")
    print('Recieved ' + str(len(data)) + ' bytes')

sock.close()
