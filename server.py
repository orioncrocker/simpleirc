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
import select
import _thread

# default values
default_port = 2000
max_clients = 3


def main():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  host = ''
  port = int(sys.argv[1])

  sock.bind((host, port))
  print('Listening on port ' + str(port))
  start_server(sock)
  sock.close()


def start_server(sock):
  sock.listen(max_clients)
  clients = []

  while True:
    # listen for connections from new clients
    if len(clients) <= max_clients:
      try:
        connection, address = sock.accept()
        if connection:
          print('Client ' + str(address[1]) + ' connected to server from ' + str(address[0]))
          clients.append(connection)
      except:
        continue

    for client in clients:
      try:
        data = client.recv(1024)
        if data:
          message = data.decode()
          print(message)
          broadcast(message, clients)
        else:
          clients.remove(client)
      except:
        continue

    print("Total clients: " + str(len(clients)))

    print('Total clients: ' + str(len(clients)))

  connection.close()


def get_message(connection):
  data = connection.recv(1024)
  if data:
    return data.decode()


def broadcast(message, clients):
  for client in clients:
    client.send(message)

main()
