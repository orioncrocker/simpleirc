###########################################################
# Author: Orion Crocker
# Filename: cmds.py
# Date: 05/14/20
# 
# Commands
# 	Server and client cmds for simpleirc
###########################################################

from server.room import Room


def client_cmds(cmd, client, server):

  def leave_server():
    client.connected = False

  def ls(arg):
    if not arg:
      client.dm('Please provide argument!\nEx: \ls rooms')
    else:
      for room in server.rooms:
        if arg == room.name:
          message = 'All clients in [' + room.name + ']:\n'
          for user in room.clients:
            message += '<' + user.name + '>\n'
          client.dm(message)

      if arg == 'users':
        message = 'All clients connected:\n'
        for user in server.clients:
          message += '<' + user.name + '>\n'
        client.dm(message)

      elif arg == 'rooms':
        message = 'All rooms available:\n'
        for room in server.rooms:
          message += '[' + room.name + ']\n'
        message += 'Rooms you are currently in:\n'
        num = 1
        for room in client.rooms:
          message += str(num) + ': [' + room.name + ']\n'
          num += 1
        client.dm(message)

  def print_help():
    send_help = '\nCommands available:'
    for i in cmds:
      send_help += '\n\\' + str(i) + '\t:\t' + str(cmds[i])
    client.dm(send_help)

  def change(arg):
    old_name = client.name
    client.name = arg
    message = '<' + old_name + '> has changed name to <' + client.name + '>\n'
    for room in server.rooms:
      if client in room.clients:
        room.broadcast(message)

  def join(args):
    args = args.split(',')
    for room in server.rooms:
      for i in args:
        if room.name == i:
          room.join(client)

  def leave(arg):
    found = False
    for room in client.rooms:
      if arg == room.name:
        room.leave(client)
        found = True
        break

    if not found:
      client.dm('Could not find room [' + arg + ']')

  def create(args):
    args = args.split(',')
    if len(args) < 1:
      client.dm("Must at least provide name for new room!\nEx: \cr room_name, room_greeting")
      return
    name = args[0]
    greeting = ''
    if len(args) >= 2:
      greeting = str(' '.join(args[1:]))
      print(greeting)
      if greeting[0] == ' ':
        greeting = greeting[1:]
    print(greeting)
    new_room = Room(name, greeting)
    server.rooms.append(new_room)
    client.dm('Created new room [' + new_room.name + ']')

  def direct_message(args):
    args = args.split(',')
    if len(args) < 2:
      return

    name = args[0]
    message = str(','.join(args[1:]))
    if message[0] == ' ':
      message = message[1:]
    recipient = False
    for user in server.clients:
      if user.name == name:
        recipient = user

    if not recipient:
      client.dm('No user named <' + name + '>')
      return

    message = '<' + client.name + ' -> ' + name + '> ' + message
    recipient.dm(message)
    client.dm(message)

  def room_message(num, args):
    num -= 1
    if len(client.rooms) < num:
      return

    room = client.rooms[num]
    room.broadcast('<' + client.name + '> ' + args)

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
          'j'     : '\t\join example_room',
          'leave' : 'leave - leave a selected room',
          'l'     : '\t\leave room_name',
          'create': 'create - creates a new chat room other users can join.',
          'cr'    : '\t\create room_name room_message',
          '1-9'   : 'specific server message - send a message to only one server at a time' +
                    spacer + '\\1 this message is for the first server only',
          'dm'    : 'direct message - send a message to another user.' +
                    spacer + '\dm user, message\n'}

  args = cmd.split(' ')
  cmd = args[0][1:]
  args = str(' '.join(args[1:]))

  # check if cmd is integer
  try:
    room_num = int(cmd)
    room_message(room_num, args)
    return
  except ValueError:
    a = 1

  if cmd in cmds:
    if cmd == 'q' or cmd == 'quit':
      leave_server()
    elif cmd == 'ls' or cmd == 'list':
      ls(args)
    elif cmd == 'h' or cmd == 'help':
      print_help()
    elif cmd == 'ch' or cmd == 'change':
      change(args)
    elif cmd == 'j' or cmd == 'join':
      join(args)
    elif cmd == 'l' or cmd == 'leave':
      leave(args)
    elif cmd == 'cr' or cmd == 'create':
      create(args)
    elif cmd == 'dm':
      direct_message(args)

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
      server.shutdown = True

    elif cmd == 'say':
      message = '<server> ' + str(' '.join(args))
      for room in server.rooms:
        room.broadcast(message)
