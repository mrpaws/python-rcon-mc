#!/usr/bin/python

import python-rcon-mc


def main():
  server=rcon.Rcon("localhost", 25575, "lol")
  server.connect()
  server.send(3,"lol")
  server.disconnect()

if __name__ == '__main__':
  main()
