################################################################################################
# Author: Orion Crocker
# Filename: client.py
# Date: 05/08/20
# 
# Client
# 	Test client
################################################################################################

import sys
import client

def main():
  if len(sys.argv) > 2:
    host = sys.argv[1]
    port = int(sys.argv[2])
  else:
    host = 'irc.orionc.dev'
    port = 2020

  name = input('Username: ')

  chat = client.IRCClient(host, port)
  chat.start(name)


if __name__ == '__main__':
  main()
