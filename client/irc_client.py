################################################################################
# Author: Orion Crocker
# Filename: irc_client.py
# Date: 05/18/20
# 
# Client
# Client side script for simpleirc
################################################################################

import sys
import socket
import threading

connected = False

class IRCClient():

  def __init__(self, host='localhost', port=2000):
    self.host=host
    self.port=port
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connected=False
    

  def listen(self):
    while self.connected:
      try:
        data = self.sock.recv(1024)
        if data:
          message = data.decode()
          if '\disconnect_from_server' in message:
            self.connected = False
          else:
            print(message)

      except socket.timeout:
        continue


  def start(self):
    try:
      self.sock.settimeout(1)
      self.sock.connect((self.host, self.port))
      self.connected = True

      read = threading.Thread(target=self.listen)
      read.start()

      while self.connected:
        message = sys.stdin.readline()[:-1]
        data = message.encode()
        self.sock.send(data)
        if message == '\q' or message == '\quit':
          self.connected = False

      read.join()
      self.sock.close()
      print("Disconnected from server " + str(self.host) + ":" + str(self.port))

    except ConnectionRefusedError:
      print("Could not connect to specified host IP and port, no response.")



if __name__ == '__main__':
  main()
