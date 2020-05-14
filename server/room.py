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
    print(message)
    for client in self.clients:
      client.dm(message)


  def join(self, client):
    self.clients.append(client) 
    client.dm('Welcome to ' + self.name + '\n' + self.greeting + '\n')
    message = client.name + ' joined ' + self.name
    self.broadcast(message)


  def leave(self, client):
    self.clients.remove(client)
    client.dm('Left ' + self.name)
    message = client.name + ' left ' + self.name
    self.broadcast(message)
