###########################################################
# Author: Orion Crocker
# Filename: room.py
# Date: 05/13/20
# 
# Room
# 	Chatroom for simple_irc
###########################################################


class Client:

  def __init__(self, name, connection, address):
    if not name:
      self.name = address
    else:
      self.name = name
    self.connection = connection
    self.connected = True
    self.address = address
    self.rooms = []

  def dm(self, message):
    message = message.encode()
    try:
      self.connection.send(message)
    except BrokenPipeError or OSError:
      self.connected = False

  def change_name(self, name):
    self.name = name


class Room:

  def __init__(self, name, greeting, log):
    self.name = name
    if not greeting:
      greeting = 'Welcome to [' + self.name + ']!'
    self.greeting = greeting
    self.clients = []
    self.log = log

  def broadcast(self, message):
    message = '[' + self.name + ']' + message
    for client in self.clients:
      client.dm(message)
    self.log.write(message)

  def join(self, client):
    self.clients.append(client) 
    client.rooms.append(self)
    client.dm('Joined [' + self.name + ']\n' + self.greeting + '\n')
    message = '<' + client.name + '> has joined the room!'
    self.broadcast(message)

  def leave(self, client):
    client.rooms.remove(self)
    self.clients.remove(client)
    client.dm('Left [' + self.name + ']')
    message = '<' + client.name + '> left the room.'
    self.broadcast(message)
