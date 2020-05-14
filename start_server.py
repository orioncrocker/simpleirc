################################################################################################
# Author: Orion Crocker
# Filename: start_server.py
# Date: 05/13/20
# 
# Server for simpleirc
# 	Bootstraps server
################################################################################################

import sys
import server


def main():
  port = int(sys.argv[1])
  irc = server.IRCServer(port=port)
  irc.start()


if __name__ == '__main__':
  main()
