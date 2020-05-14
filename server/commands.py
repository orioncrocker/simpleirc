################################################################################################
# Author: Orion Crocker
# Filename: cmds.py
# Date: 05/14/20
# 
# Commands
# 	Server and client cmds for simpleirc
################################################################################################


def client_cmds(cmd, client, server):

  def quit():
    client.dm('\client_requested_quit')
    return False

  def ls(cmd):
    print(cmd)

  def print_help():
    send_help = 'Commands available:\n'
    for i in cmds:
      send_help += '\\' + str(i) + '\t:\t' + str(cmds[i]) + '\n'
    client.dm(send_help)

  def join(cmd):
    print(cmd)

  def leave(cmd):
    print(cmd)

  def create(cmd):
    print(cmd)

  def rooms():
    print("Rooms available to join:")
    for room in self.rooms:
      print(str(room.name))

  def users(cmd):
    print(cmd)

  spacer = '\n\t\t\t'
  cmds = {'quit'  : 'quit - disconnect from the server',
          'q'     : '',
          'list'  : 'list - lists objects in server',
          'ls'    : '\t\ls users'+
                    spacer + '\list rooms',
          'help'  : 'help - displays the list you are currently reading',
          'h'     : '',
          'join'  : 'join - join a selected room',
          'j'     : '\t\join example_room'+
                    spacer + '\j different_room',
          'leave' : 'leave - leave a selected room',
          'l'     : '\t\leave room_name' +
                    spacer + '\l room_name',
          'create': 'create - creates a new chat room other users can join.',
          'cr'    : '\t\create room_name room_message' +
                    spacer + '\cr room_name room_message',
          'users' : 'users - lists users in room',
          'u'     : '\t' + r'\users a_room' +
                    spacer + r'\u some_room',
          'rooms' : r'\rooms - lists rooms you are currently in',
          'r'     : ''}

  args = cmd.split(' ')
  cmd = args[0][1:]
  args = args[1:]
  print(cmd)

  if cmd in cmds:
    if cmd == 'q' or cmd == 'quit':
      return quit()
    elif cmd == 'ls':
      ls(args)
    elif cmd == 'h':
      print_help()
  else:
    client.dm("Command not recognized. Try \h for guidance.")
  return True


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
        room.broadcast('Shutting down the server!')
      return True

    elif cmd == 'say':
      message = '<server> ' + str(' '.join(args))
      for room in server.rooms:
        room.broadcast(message)

  return False
