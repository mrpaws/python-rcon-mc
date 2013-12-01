#!/usr/bin/env python
'''
 rcon.py - RCON protocol interface module
 Author:
   paws
 Project Repo:
 Protocol: 
   https://developer.valvesoftware.com/wiki/Source_RCON_Protocol
 TODO: verify math for packets
'''

import struct
import socket

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
  '''Parent class for passing RCON module errors'''
  pass

class RconSocketException(RconException):
  '''For passing RCON socket errors'''
  pass

class RconArgumentException(RconException):
  '''For passing RCON argument'''
  pass

class RconProgramException(RconException):
  '''For passing errors in logic RCON  (debug)'''
  pass

class Rcon:
  '''Rcon class object for connection and communication'''
  def __init__(self, host, port, password, *timeout ): 
    self.host=host
    self.port=port
    self.password=password
    self.id=1
    self.connection=False
    if timeout:
      self.timeout=timeout[0] 
    else:
      self.timeout=2
    self.error_stack=[]
  
  def _manage_socket_error(self, ret_val):
    if self.connection:
      self.connection.close()
    self.connection=None
    self.error_stack.append(ret_val)

  def connect(self):
    '''Resolve remote host and connect however possible (IPV6 compat)'''
    if self.connection:
      return self.connection
    for con in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM):
      addr_fam, sock_type, proto, canonical_name, server_addr = con
      try:
        self.connection=socket.socket(addr_fam, sock_type, proto)
      except socket.error as ret_val:
        self._manage_socket_error(ret_val)
        continue
      try:
        self.connection.settimeout(self.timeout)
      except(socket.error) as ret_val:
        self._manage_socket_error(ret_val)
        continue
      try:
        self.connection.connect(server_addr)
      except(socket.error) as ret_val:
        self._manage_socket_error(ret_val)
        continue
      break
    if self.connection is None:
      raise RconException("Unable to connect: " + str(self.error_stack)) 
      self.connection=False 
      return False
    return True

  def disconnect(self):
    '''Disconnect from remote host'''
    if self.connection: 
      self.connection.close()
      self.connection=False
      return self.connection

  def send(self, type, msg):
    '''Package and issue a packet to the socket'''
    if not self.connection:
      try:
        self.connect()
      ## this needs more thorough testing, seeing as there isn
      except(rcon.RconSocketError) as ret_val:
        self.error_stack.append(ret_val)
        raise RconException("Attempt to connect upon send failed." + str(self.error_stack)) 
        return False
    msg_len=len(msg)
    if msg_len > MAX_BODY_SIZE: 
      raise RconException("Request message body too large. MAX=" + str(MAX_BODY_SIZE))
      return False
    size = msg_len + MIN_PACKET_SIZE
    self.id = self.id+1

    '''
     feels like I should be able to do this in one pack call? i.e. '<i<i<i', but works
      packet = struct.pack('<i', size) + struct.pack('<i', self.id) + struct.pack('<i', type) +  msg + NULL + NULL
    '''
    try: 
      packet = struct.pack('<i', size) + struct.pack('<i', self.id) + struct.pack('<i', type) +  msg + NULL + NULL
    except(struct.error) as ret_val:
      raise RconProgramExceptio("Unable to create TCP packet: " + str(error_stack))
      return False
    try: 
      self.connection.send(packet)
    except(socket.error) as ret_val:
      raise RconSocketException("Send failure: " + str(ret_val))
      return False
    return True

  def receive(self):
    '''Read responses from the socket and unpack them'''
    unpack_fmt="<iiixx" ## empty body packet format
    try:
      packet = self.connection.recv(MAX_PACKET_SIZE)
    except(socket.error) as ret_val:
      self._manage_socket_error(ret_val)
      raise RconSocketException("Failed to receive data from socket:" + str(self.error_stack))
      return False
    msg_size = len(packet) - MIN_PACKET_ACTUAL_SIZE 
    if msg_size > 0:
      unpack_fmt = "<iii" + str(msg_size) + "sxx"
    payload = struct.unpack(unpack_fmt, packet)
    return payload

  def rcon(self, command):
    '''Higher level function that manages message id matching'''
    self.send(3,self.password)
    self.receive()
    self.send(2,command)
    return self.receive()
