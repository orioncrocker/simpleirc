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


def main():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # server address
  host = sys.argv[1]
  # port server is listening on
  port = int(sys.argv[2])
  sock.connect((host, port))

  while True:
    data = sock.recv(1024)

    if data:
      message = data.decode()
      print(message)

    if not data:
      message = sys.stdin.readline()
      sock.send(message)
      sys.stdout.flush()

  sock.close()


main()
