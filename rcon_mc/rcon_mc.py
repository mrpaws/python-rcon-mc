#!/usr/bin/env python
"""
               ****** WIP ******
   You probably want rcon.py for elementary usage
   This is a work in progress to implement some
   minecraft rcon commands as a class, to even
   further simplify using this package

   rcon_mc.py - Minecraft RCON helper interface
 Author:
   mrpaws
 Project Repo:
   https://github.com/mrpaws/python-rcon-mc
"""

from rcon import client as rcon


class RconMCException(Exception):
    """class for throwing errors related to rcon_mc"""
    pass


class client(rcon):
    """class to execute commands on the server"""
    """
  def __init__(self, host, port, password ):
    self.host=host
    self.port=port
    self.password=password
    self.error_stack=[]
    assert type(self.host) is StringType,
        "{m}{h}".format(m="hostname is not a string:", h=self.host)
    assert type(self.port) is IntType,
        "{m}{p}".format(m="port is not a number:", p=self.port)
    assert type(self.host) is StringType, "password is not a string"
  """
