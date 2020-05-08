# header goes here

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server address
host = sys.argv[1]
# port server is listening on
port = int(sys.argv[2])

sock.connect((host, port))

message = 'Is this thing on?'
data = message.encode()
sock.send(data)

i = 0
while(1):
    data = sock.recv(1000000)
    i += 1
    if (i < 5):
        print(data)
    if not data:
        break
    print('Recieved ' + str(len(data)) + ' bytes')

sock.close()
