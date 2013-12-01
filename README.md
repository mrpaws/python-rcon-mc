python-rcon-mc
==============

** This project is not yet released and is worked on time permitting**

Genral Python API for interacting with RCON servers, specifically for use with Minecraft
  by Paws

** This is primarily a learning project**


Features
=====
  - RCON API
  - Minecraft Server (FTB/Vanilla) RCON API
  - IPV6 compatability
  - Multi-packet responses
  - high level functions for ease of use



Summary
=======
Module rcon/rcon.py provides an interface for general interaction with any Source RCON server ( see below )  while module mc/mc_rcon.py provides an interface to minecraft's implementation of RCON.  The packag format is really just a formality, as these particular modules are for use in a larger project.

The code within is written by somewhat of a Python newbie and is more of a fun learning project than anything else. However, due diligence has been taken to ensure functionality and reusability should anyone want to interface with a minecraft server.  See below for testing information. 

Testing
========
A wrapper script - test.py - is provided to demonstrate general usage and test functionality on your system/Python.  Below are individual confirmed test cases.

  2.7.3 - Linux 3.2.0-4-amd64 #1 SMP Debian 3.2.51-1 x86_64 GNU/Linux

**Security**
============
The RCON protocol does not support SSL and therefore the code is best used when connecting to localhost.  That is, it is run on the same machine and does not need to make any network hops.  The password to the rcon server is transmitted in clear text and can be extracted by any intermediary systems. Exceptions may apply such as connecting to systems on a trusted LAN (home network) or encrypted VPN connection on a trusted network.


Whodunit
======
Again, this is a learning project, but constructive criticism or push requests are welcome!  If you wish to reach the owner, contact paws@delimitize.com .
