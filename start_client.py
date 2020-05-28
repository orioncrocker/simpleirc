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
    # deault server config
    host = '152.44.40.87'
    port = 2000

  chat = client.IRCClient(host=host, port=port)
  chat.start()


if __name__ == '__main__':
  main()
