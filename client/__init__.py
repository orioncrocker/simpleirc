################################################################################
# Author: Orion Crocker
# Filename: __init__.py
# Date: 05/18/20
# 
# client init
#   self explanatory
################################################################################

import sys
from client.irc_client import IRCClient

assert sys.version_info[0] == 3, "Requires python3"
