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

class IRCServer():

  def __init__(self, port=2000, max_clients=10):
    self.host = ''
    self.port = port
    self.max_clients = max_clients
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.shutdown = False
    self.clients = []
    self.rooms = []


  def commands(self, command, client, room):

    def quit():
      client.dm('\client_requested_quit')
      return False

    def ls(command):
      print(command)

    def print_help():
      send_help = 'Commands available:\n'
      for i in commands:
        send_help += '\t\\' + str(i) + '\t:\t' + str(commands[i]) + '\n'
      client.dm(send_help)

    def join(command):
      print(command)

    def leave(command):
      print(command)

    def create(command):
      print(command)

    def rooms():
      print("Rooms available to join:")
      for room in self.rooms:
        print(str(room.name))

    def users(command):
      print(command)

    commands = {'q' : 'quit - disconnect from the server',
                'ls' : 'list - list based on an argument\n\t\t\t' + 
                      '\ls users\n\t\t\t' + 
                      '\ls rooms',
                'h' : 'help - displays the list you are currently reading',
                'j' : 'join - join a selected room\n\t\t\t' +
                      '\j example_room',
                'l' : 'leave - leave a selected room\n\t\t\t' +
                      '\l example_room',
                'cr' : 'create - creates a new chat room\n\t\t\t' +
                      '\cr room_name room_message',
                'u' : r'users - lists users in room\n\t\t\t\u arg_room',
                'r' : 'rooms - lists rooms you are currently in'}

    command = command[1:]
    args = command.split(' ')[1:]

    if command[0] in commands:
      if command == 'q':
        return quit()
      elif command == 'ls':
        ls(args)
      elif command == 'h':
        print_help()
    else:
      client.dm("Command not recognized. Try \h for guidance.")
    return True


  def listen_to_client(self, client, current_room):
    connected = True
    current_room.join(client)

    while connected:
      data = client.connection.recv(1024)
      if data:
        message = data.decode()

        if message[0] == '\\':
          connected = self.commands(message, client, current_room)
          
        else:
          message = "<" + client.name + "> " + message
          print(message)
          current_room.broadcast(message)

    current_room.leave(client)
    self.clients.remove(client)
    client.connection.close()
    print(str(client.name) + ' disconnected')


  def cmd_center(self):
    commands = ['stop',
                'say',
                'kick',
                'ban',
                'move']

    while not self.shutdown:
      command = sys.stdin.readline()[:-1]
      args = command.split(' ')
      cmd = args[0]

      if cmd in commands:
        if cmd == 'stop':
          for room in self.rooms:
            room.broadcast('Shutting down server!')
          self.shutdown = True

        elif cmd == 'say':
          message = ''
          for arg in args:
            message += arg + ' '
          for room in self.rooms:
            room.broadcast(message)
      
      else:
        continue      
      sys.stdin.flush()


  def start(self):
    self.sock.settimeout(1)
    self.sock.bind((self.host, self.port))
    self.sock.listen(self.max_clients)

    # create server control thread
    command_thread = threading.Thread(target=self.cmd_center)
    command_thread.start()

    # list of client threads
    client_procs = []

    # create default room
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
