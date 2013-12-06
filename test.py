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
    print "Fail"
    return False
  print rcv
  return True
  


def main():
  '''
  server=rcon_mc.rcon.Rcon("localhost", 25575, "lol")
  response=server.rcon("/help 1")
  print response
  '''
  test_msocket()
  
  exit

if __name__ == '__main__':
  main()
