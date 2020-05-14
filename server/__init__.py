################################################################################################
# Author: Orion Crocker
# Filename: __init__.py
# Date: 05/13/20
# 
# server init
# 	self explanatory
################################################################################################

import sys
from server.irc_server import IRCServer

assert sys.version_info[0] == 3, "Requires python3"
