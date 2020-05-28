################################################################################################
# Author: Orion Crocker
# Filename: start_server.py
# Date: 05/13/20
# 
# Server for simpleirc
# 	Bootstraps server
################################################################################################

#!/usr/bin/python3

import sys
import server


def main():
  if len(sys.argv) < 2:
    print("Need to specify port!\nEx: python3 start_server.py 2000")
    quit()

  port = int(sys.argv[1])
  irc = server.IRCServer(port=port)
  irc.start()


if __name__ == '__main__':
  main()
