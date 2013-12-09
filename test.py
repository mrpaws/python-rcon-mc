#!/usr/bin/python

''' example usage'''

import rcon_mc.rcon
import rcon_mc.lib.msocket

def test_msocket():
  ''' test low level socket functionality'''
  server = rcon_mc.lib.msocket.msocket("www.google.com",80, 1)
  snd = server.send("GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n")
  rcv = server.receive();
  if rcv is False:
    print "Failed msocket.manage test..."
    return False
  print rcv
  return True

def test_msocket_manage():
  '''test msocket manage function'''
  server = rcon_mc.lib.msocket.msocket("www.google.com",80,1)
  answer = server.manage("GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n")
  print answer 
  


def main():
  ''' test module functionality helper'''
  client=rcon_mc.rcon.client("localhost", 25575, "lol")
  response=client.send("/help 1")
  print response
  #test_msocket_manage()
  
  exit

if __name__ == '__main__':
  main()
