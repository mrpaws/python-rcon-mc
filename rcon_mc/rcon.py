#!/usr/bin/env python
'''
 rcon.py - RCON protocol interface module
 Author:
   mrpaws
 Project Repo:
   https://github.com/mrpaws/python-rcon-mc
 Protocol: 
   https://developer.valvesoftware.com/wiki/Source_RCON_Protocol
'''
import struct
import lib.msocket as msocket

''' 
   "Not authenticated" response:
	\n\x00\x00\x00\xff\xff\xff\xff\x02\x00\x00\x00\x00\x00
'''


'''Module Declarations:'''
NULL='\x00' ## hex for C null terminator
MIN_PACKET_SIZE=10  # 4(id)+4(type)+1(body)+1(empty string)
MIN_PACKET_ACTUAL_SIZE=14 # 4(size) + 4(id)+4(type)+1(body)+1(empty string)
MAX_PACKET_SIZE=4096 # just the way it is
MAX_BODY_SIZE=4086 # (4096 - 4(id) - 4(type) - 1(empty string) -1(body null-terminator)) = 4086

'''RCON command types:'''
SERVERDATA_RESPONSE_VALUE=0
SERVERDATA_EXECCOMMAND=2
SERVERDATA_AUTH_RESPONSE=2
SERVERDATA_AUTH=3

error=""

class RconException(Exception):
  '''For passing RCON module exceptions'''
  pass

class rcon:
  '''RCON protocol communication'''
  def __init__(self, host, port, password):
    self.host=host
    self.port=port
    self.password=password
    self.error_stack=[]
    self.id=0
    try: 
      self.connection = msocket.msocket(self.host, self.port)
    except(msocket.error) as ret_val:
      _manage_rcon_error(ret_val)
      return False

  def _manage_rcon_error(self, ret_val):
    self.error_stack.append(ret_val)
    error=str(error_stack)
    raise RconException(error_stack)

  def _connect(self):
    try:
     con = self.connection.connect()
    except(msocket.error) as ret_val:
      if con is False:
        _manage_rcon_error(ret_val)
        return false
    return True

  def _craft_packet(self, type, msg):
    '''Crafts RCON packet'''
    if not msg:
      msg=""
    msg_len=len(msg)
    size = msg_len + MIN_PACKET_SIZE
    if msg_len > MAX_BODY_SIZE:
      _manage_rcon_error("{m}\n{s}".format(m="Request message body too large. MAX=",
        s= str(MAX_BODY_SIZE)))
      return False
    try:
      packet = struct.pack('<i', size) + struct.pack('<i', self.id) + struct.pack('<i', type) + msg + NULL + NULL
    except(struct.error) as ret_val:
      _manage_rcon_error("{m}\n{s}".format(m="Unable to pack data into TCP packet: ", s=str(error_stack)))
      return False
    return packet

  def _send(self, type, msg):
    '''handles send logic.. maybe not necessary'''
    if not self.connection:
      try:
        self._connect()
      except(error) as ret_val:
        return False
      return False
    try:
      packet = self._craft_packet(type, msg)
    except(error) as ret_val:
      return False
    try:
      response = self.connection.manage(packet)
    except(msocket.error) as ret_val:
      _manage_rcon_error(ret_val)
      return false
    if not response:
      _manage_rcon_error("Empty response from server")
      return false
    return response

  def send(self, msg):
    '''Sends a command to the RCON server, does not necessasarily
       disconnect. Returns the response.
       !!!DONT FORGET TO INCREMENT ID HERE!!!, OR... revert your decision
       to put it in this function instead of the private metho
    '''
