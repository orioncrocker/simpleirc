################################################################################################
# Author: Orion Crocker
# Filename: irc_server.py
# Date: 05/13/20
# 
# Server for simpleirc
# 	Listens for clients and client messages
################################################################################################

import sys
import socket
import threading
from server.room import Room
from server.room import Client
from server.commands import *

class IRCServer():

  def __init__(self, port=2000, max_clients=10):
    self.host = ''
    self.port = port
    self.max_clients = max_clients
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.shutdown = False
    self.clients = []
    self.rooms = []
    self.ban_list = []


  def cmd_center(self):
    while not self.shutdown:
      command = sys.stdin.readline()[:-1]
      sys.stdin.flush()
      self.shutdown = server_cmds(command, self)


  def listen_to_client(self, client, current_room):
    current_room.join(client)
    client.connection.settimeout(1)

    while client.connected and not self.shutdown:
      try:
        data = client.connection.recv(1024)
        if data:
          message = data.decode()

          if message[0] == '\\':
            client_cmds(message, client, self)
            
          else:
            message = client.name + ' ' + message
            current_room.broadcast(message)

      except socket.timeout:
        continue

    print(str(client.name) + ' disconnecting.')
    # remove from all rooms lists
    for room in self.rooms:
      if client in room.clients:
        room.leave(client)
    # remove from master client list
    self.clients.remove(client)
    client.connection.close()
    print(str(client.name) + ' disconnected')


  def start(self):
    self.sock.settimeout(1)
    self.sock.bind((self.host, self.port))
    self.sock.listen(self.max_clients)

    # create server control thread
    command_thread = threading.Thread(target=self.cmd_center)
    command_thread.start()

    # list of client threads
    client_procs = []

    # create defaul room
    lobby = Room('the lobby', 'Use command \h for help!')
    self.rooms.append(lobby)

    print("Now listening for clients on port " + str(self.port))
    while not self.shutdown:
      try:
        connection, address = self.sock.accept()
        new_client = Client(address[0], connection, address[0])
        self.clients.append(new_client)

        client_thread = threading.Thread(target=self.listen_to_client, args=(new_client, lobby))
        client_thread.start()
        client_procs.append(client_thread)
        print("Clients connected: " + str(len(self.clients)))

      except socket.timeout:
        continue

    command_thread.join()
    for proc in client_procs:
      proc.join()
