############################################################
# Author: Orion Crocker
# Filename: log.py
# Date: 05/30/20
# 
# Log
# 	Record of server information and public chat log
#   Client DMs are never recorded
############################################################

import os
import socket
from datetime import datetime


class Log:

    def __init__(self, port):
        self.filename = None
        self.path = None
        self.boot(port)

    def boot(self, port):
        hostname = socket.gethostname()
        date = datetime.today().strftime("%m:%d:%Y_%H:%M:%S")
        self.filename = 'simpleirc_' + str(hostname) + ':' + str(port) +\
                        '_' + str(date) + '.log'
        self.path = os.path.abspath('server/logs/' + self.filename)
        with open(self.path, 'w') as file:
            file.write(str(date) + '\n' + str(hostname) + ':' + str(port) + '\n\n')

    def write(self, text):
        if text:
            date = datetime.today().strftime('%H:%M%S')
            with open(self.path, 'a') as file:
                file.write(str(date) + str(text) + '\n')
            print(text)

    def time(self):
        date = datetime.today().strftime("%m:%d:%Y_%H:%M:%S")
        with open(self.path, 'a') as file:
            file.write(str(date) + '\n')
