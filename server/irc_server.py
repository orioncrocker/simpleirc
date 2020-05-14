################################################################################################
# Author: Orion Crocker
# Filename: irc_server.py
# Date: 05/13/20
# 
# Server for simpleirc
# 	Listens for clients and client messages
################################################################################################

import socket
import threading
from server.room import Room
from server.room import Client

class IRCServer():

  def __init__(self, port=2000, max_clients=10):
    self.host = ''
    self.port = port
    self.max_clients = max_clients
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    self.clients = []
    self.rooms = []


  def listen(self, client, current_room):
    connected = True
    current_room.join(client)

    while connected:
      data = client.connection.recv(1024)
      if data:
        message = data.decode()

        if message[0] == '\\':
          if message == '\\q':
            connected = False
            client.dm("Disconnecting you from the server")
          
        else:
          message = "<" + client.name + "> " + message[:-1]
          print(message)
          current_room.broadcast(message)

    current_room.leave(client)
    self.clients.remove(client)
    client.connection.close()


  def start(self):
    self.sock.bind((self.host, self.port))
    self.sock.listen(self.max_clients)
    lobby = Room('the lobby', 'Use command \h for help!')
    self.rooms.append(lobby)

    print("Now listening for clients on port " + str(self.port))

    while True:
      connection, address = self.sock.accept()
      new_client = Client(address[0], connection, address[0])
      self.clients.append(new_client)

      client_thread = threading.Thread(target=self.listen, args=(new_client, lobby))
      client_thread.start()
      print("Clients connected: " + str(len(self.clients)))
