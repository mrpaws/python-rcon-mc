#!/usr/bin/env python
'''
 rcon_mc.py - Minecraft RCON helper interface
 Author:
   mrpaws
 Project Repo:
   https://github.com/mrpaws/python-rcon-mc
'''

from rcon import client as rcon
from types import *

class RconMCException(Exception):
  '''class for throwing errors related to rcon_mc'''
  pass

class client(rcon):
  '''class to execute commands on the server'''

