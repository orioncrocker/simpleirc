################################################################################################
# Author: Orion Crocker
# Filename: cmds.py
# Date: 05/14/20
# 
# Commands
# 	Server and client cmds for simpleirc
################################################################################################

from server.room import Room

def client_cmds(cmd, client, server):

  def quit():
    client.connected = False

  def ls(arg):
    if not arg:
      client.dm('Please provide argument!\nEx: \ls rooms')
    else:
      for room in server.rooms:
        if arg in room.name:
          message = 'All clients in ' + room.name + ':'
          for user in room.clients:
            message += '\n' + user.name
          client.dm(message)

      if arg == 'users':
        message = 'All clients connected:'
        for user in server.clients:
          message += '\n' + user.name
        client.dm(message)

      elif arg == 'rooms':
        message = 'All rooms available:'
        for room in server.rooms:
          message += '\n' + room.name
        client.dm(message)

  def print_help():
    send_help = '\nCommands available:'
    for i in cmds:
      send_help += '\n\\' + str(i) + '\t:\t' + str(cmds[i])
    client.dm(send_help)

  def change(args):
    old_name = client.name
    client.name = '<'+args+'>'
    message = old_name + ' has changed name to ' + client.name
    for room in server.rooms:
      if client in room.clients:
        room.broadcast(message)

  def join(arg):
    print(arg)

  def leave(arg):
    print(arg)

  def create(args):
    args = args.split(',')
    print(args)
    if len(args) < 1:
      client.dm("Must at least provide name for new room!\nEx: \cr 'room_name' 'room_greeting'")
    else:
      name = args[0]
      greeting = ''
      if len(args) > 2:
        greeting = str(' '.join(args[1:]))
      new_room = Room(name, greeting)
      server.rooms.append(new_room)
      client.dm('Created new room ' + name)
    

  spacer = '\n\t\t\t'
  cmds = {'quit'  : 'quit - disconnect from the server',
          'q'     : '',
          'list'  : 'list - lists objects in server',
          'ls'    : '\t\ls users'+
                    spacer + '\list rooms',
          'help'  : 'help - displays the list you are currently reading',
          'h'     : '',
          'change': 'change name - change username from default to something else',
          'ch'    : '\t\ch my_name',
          'join'  : 'join - join a selected room',
          'j'     : '\t\join example_room'+
                    spacer + '\j different_room',
          'leave' : 'leave - leave a selected room',
          'l'     : '\t\leave room_name' +
                    spacer + '\l room_name',
          'create': 'create - creates a new chat room other users can join.',
          'cr'    : '\t\create room_name room_message' +
                    spacer + '\cr room_name room_message'}

  args = cmd.split(' ')
  cmd = args[0][1:]
  args = str(' '.join(args[1:]))

  if cmd in cmds:
    if cmd == 'q' or cmd == 'quit':
      return quit()
    elif cmd == 'ls' or cmd == 'list':
      ls(args)
    elif cmd == 'h' or cmd == 'help':
      print_help()
    elif cmd == 'ch' or cmd == 'change':
      change(args)
    elif cmd == 'cr' or cmd == 'create':
      create(args)
  else:
    client.dm("Command not recognized. Try \h for guidance.")


def server_cmds(cmd, server):
  cmds = ['stop',
          'say',
          'kick',
          'ban',
          'move']

  args = cmd.split(' ')
  cmd = args[0]
  args = args[1:]

  if cmd in cmds:
    if cmd == 'stop':
      for room in server.rooms:
        room.broadcast('The server is shutting down!')
        for client in room.clients:
          client.connected = False
      server.shutdown = True

    elif cmd == 'say':
      message = '<server> ' + str(' '.join(args))
      for room in server.rooms:
        room.broadcast(message)
