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

  def name(arg):
    if not arg:
      client.dm('Your name is ' + client.name)
    else:
      for user in server.clients:
        if user.name == arg:
          client.dm('Another user already has that name!')
          return

      if ',' in arg:
        client.dm('Cannot include commas in usernames!')
        return

      old_name = client.name
      client.name = arg
      message = '<' + old_name + '> has changed name to <' + client.name + '>'
      for room in server.rooms:
        if client in room.clients:
          room.broadcast(message)

  def join(args):
    for room in server.rooms:
      if room.name == args:
        if client not in room.clients:
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
    for room in server.rooms:
      if name == room.name:
        client.dm("Room with that name already exists!")
        return

    greeting = ''
    if len(args) >= 2:
      greeting = str(' '.join(args[1:]))
      if greeting[0] == ' ':
        greeting = greeting[1:]
    new_room = Room(name, greeting, server.log)
    server.rooms.append(new_room)
    client.dm('Created new room [' + name + ']')
    server.log.write(client.name + ' created new room [' + name + ']')

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
      client.dm('No user named <' + name + '>!')
      return

    message = '<' + client.name + ' -> ' + name + '> ' + message
    recipient.dm(message)
    client.dm(message)

  def room_message(room_num, args):
    rooms = len(client.rooms)
    if room_num > rooms or room_num < 1:
      return
    room_num -= 1
    client.rooms[room_num].broadcast('<' + client.name + '> ' + args)

  spacer = '\n\t\t\t'
  cmds = {'quit'  : 'quit - disconnect from the server',
          'q'     : '',
          'list'  : 'list - lists objects in server',
          'ls'    : '\t\ls users'+
                    spacer + '\list rooms',
          'help'  : 'help - displays the list you are currently reading',
          'h'     : '',
          'name'  : 'change name - change username from default to something else',
          'n'     : "use \\" + 'name to see what your current username is' +
                    spacer + "\\" + 'n my_name',
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
    elif cmd == 'n' or cmd == 'name':
      name(args)
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
          'say']

  args = cmd.split(' ')
  cmd = args[0]
  args = args[1:]

  if cmd in cmds:
    if cmd == 'stop':
      server.log.write('STOP')
      for room in server.rooms:
        room.broadcast(' The server is shutting down!')
      server.shutdown = True

    elif cmd == 'say':
      message = '<server> ' + str(' '.join(args))
      for room in server.rooms:
        room.broadcast(message)
