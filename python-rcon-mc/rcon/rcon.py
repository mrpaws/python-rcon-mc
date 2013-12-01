#!/usr/bin/env python
''' rcon.py - RCON protocol interface module
 Author:
   paws
 Project Repo:
 Protocol: 
   https://developer.valvesoftware.com/wiki/Source_RCON_Protocol
 TODO: verify math for packets
'''

import struct
import socket


'''
TCP Packet Structure
Field  Type  Value    Python_Representation
Size   32-bit little-endian Signed Integer  'i<'  
ID   32-bit little-endian Signed Integer   '<i'
Type   32-bit little-endian Signed Integer   '<i' 
Body  Null-terminated ASCII String   Varies "string\x00"
Empty String  Null-terminated ASCII String   0x00 '\x00'
'''

'''Module Declarations:'''
NULL='\x00' ## hex for C null terminator
MIN_PACKET_SIZE=10  # 4(id)+4(type)+1(body)+1(empty string)
MAX_PACKET_SIZE=4096 # just the way it is
MAX_BODY_SIZE=4086 # (4096 - 4(id) - 4(type) - 1(empty string) -1(body null-terminator)) = 4086

'''RCON command types:'''
SERVERDATA_RESPONSE_VALUE=0
SERVERDATA_EXECCOMMAND=2
SERVERDATA_AUTH_RESPONSE=2
SERVERDATA_AUTH=3

error=""

class RconException(Exception):
  '''For passing Rcon module errors'''
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

  def connect(self):
    '''Resolve remote host and connect however possible (IPV6 compat)'''
    if self.connection:
      return self.connection
    for con in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM):
      addr_fam, sock_type, proto, canonical_name, server_addr = con
      try:
        self.connection=socket.socket(addr_fam, sock_type, proto)
      except socket.error as ret_val:
        self.connection=None
        self.error_stack.append(ret_val)
        continue
      try:
        self.connection.settimeout(self.timeout)
        self.connection.connect(server_addr)
      except(socket.error) as ret_val:
        self.connection.close()
        self.connection=None
        self.error_stack.append(ret_val)
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
      except(rcon.error) as ret_val:
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
    packet = struct.pack('<i', size) + struct.pack('<i', self.id) + struct.pack('<i', type) +  msg + NULL + NULL
    self.connection.send(packet)

  def receive(self):
    return self.connection.recv(4096)

  def rcon(self, command):
    self.send(3,self.password)
    self.receive()
    self.send(2,command)
    return self.receive()
