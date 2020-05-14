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

def main():
  if len(sys.argv) < 3:
    print("Please enter the destination address and port")
    print("Example: python3 client.py 192.168.0.12 2000")
    quit()

  host = sys.argv[1]
  port = int(sys.argv[2])

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((host, port))

  connected = True
  read = threading.Thread(target=listen, args=[sock, connected])
  read.start()

  while connected:
    message = sys.stdin.readline()[:-1]
    data = message.encode()
    sock.send(data)
    if message == '\q':
      connected = False

  read.join()
  sock.close()
  print("Disconnected from server " + str(host) + ":" + str(port))


def listen(sock, connected):
  while connected:
    data = sock.recv(1024)
    if data:
      message = data.decode()
      if '\client_requested_quit' in message:
        connected = False
      else:
        print(message)


if __name__ == '__main__':
  main()
