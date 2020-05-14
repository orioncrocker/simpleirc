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
import threading

# global values

def main():
  host = sys.argv[1]
  port = int(sys.argv[2])

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((host, port))

  read = threading.Thread(target=listen, args=[sock])
  read.start()

  while True:
    message = sys.stdin.readline()
    data = message.encode()
    sock.send(data)

  sock.close()


def listen(sock):
  while True:
    data = sock.recv(1024)
    if data:
      message = data.decode()
      print(message)


main()
