################################################################################################
# Author: Orion Crocker
# Filename: room.py
# Date: 05/13/20
# 
# Room
# 	Chatroom for simple_irc
################################################################################################

class Client():

  def __init__(self, name, connection, address):
    if not name:
      self.name = '<'+address+'>'
    else:
      self.name = '<'+name+'>'
    self.connection = connection
    self.connected = True
    self.address = address
    self.rooms = []


  def dm(self, message):
    message = message.encode()
    try:
      self.connection.send(message)
    except BrokenPipeError:
      self.connected = False


  def change_name(self, name):
    self.name = '<'+name+'>'


class Room():

  def __init__(self, name, greeting):
    self.name = '['+name+']'
    self.greeting = greeting
    self.clients = []


  def broadcast(self, message):
    message = self.name + ' ' + message
    print(message)
    for client in self.clients:
      client.dm(message)


  def join(self, client):
    self.clients.append(client) 
    client.dm('Welcome to ' + self.name + '\n' + self.greeting + '\n')
    message = client.name + ' has joined the room.'
    self.broadcast(message)


  def leave(self, client):
    self.clients.remove(client)
    client.dm('Left ' + self.name)
    message = client.name + ' left the room.'
    self.broadcast(message)
