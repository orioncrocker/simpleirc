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
      self.name = address
    else:
      self.name = name
    self.connection = connection
    self.address = address


  def dm(self, message):
    message = message.encode()
    self.connection.send(message)


class Room():

  def __init__(self, name, greeting):
    self.name = name
    self.greeting = greeting
    self.clients = []


  def broadcast(self, message):
    message = message.encode()
    for client in self.clients:
      client.connection.send(message)


  def join(self, client):
    self.clients.append(client) 
    client.dm('Welcome to ' + self.name + '\n' + self.greeting)
    self.broadcast(str(client.name) + ' joined on ' + str(client.address))
    message = client.name + ' joined ' + self.name
    print(message)


  def leave(self, client):
    client.dm('Leaving ' + self.name)
    self.clients.remove(client)
    self.broadcast(str(client.name) + ' left the room.')
    message = client.name + ' left ' + self.name
    print(message)
