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
    client.dm('\disconnect_from_server')
    client.connected = False

  def ls(arg):
    print(arg)

  def print_help():
    send_help = 'Commands available:\n'
    for i in cmds:
      send_help += '\\' + str(i) + '\t:\t' + str(cmds[i]) + '\n'
    client.dm(send_help)

  def change(args):
    old_name = client.name
    client.name = '<'+str(' '.join(args))+'>'
    message = old_name + ' has changed name to ' + client.name
    for room in server.rooms:
      if client in room.clients:
        room.broadcast(message)

  def join(arg):
    print(arg)

  def leave(arg):
    print(arg)

  def create(arg):
    print(arg)

  def rooms():
    print("Rooms available to join:")
    for room in self.rooms:
      print(str(room.name))

  def users(arg):
    print(arg)

  spacer = '\n\t\t\t'
  cmds = {'quit'  : 'quit - disconnect from the server',
          'q'     : '',
          'list'  : 'list - lists objects in server',
          'ls'    : '\t\ls users'+
                    spacer + '\list rooms',
          'help'  : 'help - displays the list you are currently reading',
          'h'     : '',
          'ch'    : 'change name - change username from default to something else',
          'change': '\t\ch my_name',
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
  args = args[1:]

  if cmd in cmds:
    if cmd == 'q' or cmd == 'quit':
      return quit()
    elif cmd == 'ls' or cmd == 'list':
      ls(args)
    elif cmd == 'h' or cmd == 'help':
      print_help()
    elif cmd == 'ch' or cmd == 'change':
      change(args)
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
          client.dm('\disconnect_from_server')
          client.connected = False
      return True

    elif cmd == 'say':
      message = '<server> ' + str(' '.join(args))
      for room in server.rooms:
        room.broadcast(message)

  return False
