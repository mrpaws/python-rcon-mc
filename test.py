#!/usr/bin/python

''' example usage'''

import rcon_mc.rcon


def main():
  server=rcon_mc.rcon.Rcon("localhost", 25575, "lol")
  response=server.rcon("/help 1")
  print response
  exit

if __name__ == '__main__':
  main()
