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


def timestamp():
    return datetime.today().strftime("%m:%d:%Y-%H:%M:%S")


class Log:

    def __init__(self, port):
        self.filename = None
        self.path = None
        self.boot(port)

    def boot(self, port):
        # check if logs directory exists
        path = os.path.abspath('server/logs')
        if not os.path.exists(path):
            os.makedirs(path)

        hostname = socket.gethostname()
        date = timestamp()
        self.filename = 'simpleirc_' + str(hostname) + ':' + str(port) +\
                        '_' + str(date) + '.log'
        self.path = path + '/' + self.filename
        with open(self.path, 'w') as file:
            file.write(str(date) + '\nHost machine:' + str(hostname) +\
                       str(port) + '\n\n')

    def write(self, text):
        if text:
            with open(self.path, 'a') as file:
                file.write(str(timestamp()) + '\t' + str(text) + '\n')
            print(text)
