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
import threading

# global values
default_port = 2000
max_clients = 3
clients = []


def main():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  host = ''
  port = int(sys.argv[1])

  sock.bind((host, port))
  print('Listening on port ' + str(port))
  listen(sock)
  sock.close()


def listen(sock):
  sock.listen(max_clients)

  while True:
    connection, address = sock.accept()
    clients.append(connection)
    print('Client ' + str(address[1]) + ' connected to server from ' + str(address[0]))

    x = threading.Thread(target=client, args=(connection, address))
    x.start()
    print("Clients connected: " + str(len(clients)))

  connection.close()


def client(connection, address):
  message = "Welcome to the server!"
  message = message.encode()
  connection.send(message)

  while True:
    data = connection.recv(1024)
    if data:
      message = data.decode()
      message = "<" + address[0] + "> " + message
      print(message)
      broadcast(message)


def get_message(connection):
  data = connection.recv(1024)
  if data:
    return data.decode()


def broadcast(message):
  message = message.encode()
  for client in clients:
    client.send(message)


main()
