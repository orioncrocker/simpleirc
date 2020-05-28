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
  if len(sys.argv) < 3:
    print("Please enter the destination address and port")
    print("Example: python3 client.py 192.168.0.12 2000")
    quit()

  host = sys.argv[1]
  port = int(sys.argv[2])
  chat = client.IRCClient(host=host, port=port)
  chat.start()


if __name__ == '__main__':
  main()
