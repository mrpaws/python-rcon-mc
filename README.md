python-rcon-mc
==============

Genral Python API for interacting with RCON servers, specifically for use with Minecraft
** started as a  learning project**

Features
=====
  - Python Minecraft RCON API
  - Reusable client socket module (rcon_mc.lib.msocket)
  - IPV6 compatability 
  - Keep-Alive functionality
  - Minimal reauthentication message to reduce wire spam
  - high level functions for ease of use
  - typical server command class for super ease of use (TBI)



Summary
=======
Module rcon/rcon.py provides an interface for general interaction with any Source RCON server ( see below )  while module mc/mc_rcon.py provides an interface to minecraft's implementation of RCON.  The packag format is really just a formality, as these particular modules are for use in a larger project.

The code within is written by somewhat of a Python newbie and is more of a fun learning project than anything else. However, due diligence has been taken to ensure functionality and reusability should anyone want to interface with a minecraft server.  See below for testing information. 

The primary objectives are to spend time:
 - Coding in python
 - Learning about core python modules
 - Refreshing networking know-how
 

Testing
========
A wrapper script - test.py - is provided to demonstrate general usage and test functionality on your system/Python.  Below are individual confirmed test cases.

  2.7.3 - Linux 3.2.0-4-amd64 #1 SMP Debian 3.2.51-1 x86_64 GNU/Linux
  
RCON Implementation
=========
Source's RCON Protocol documents (see the wiki) were used for general guidance, however RCON "protocols" are not typically implemented verbatim with this protocol.  RCON tends to differ from implementation to implemetnation.  For example, handling multi-packet responses is typically done by following each send with an empty SERVERDATA_RESPONSE packet, because the server is designed to reflect this and - because the server also returns the messages in the order they were received - this could be used to determine the last packet in a sequence of response packets.  Minecraft's implementation simply returns "Unknown request 0".  However, the minecraft implentation does set the 'id' field of the response to -1 upon auth failures and does require the same packet structure and command codes.  Because of these nuances, this particular impmentation of RCON is only really suitable for minecraft, at least for the moment.  However, minimal work should be necessary to match other implementation's requirements.  

**Security**
============
The RCON protocol does not support SSL and therefore the code is best used when connecting to localhost.  That is, it is run on the same machine and does not need to make any network hops.  The password to the rcon server is transmitted in clear text and can be extracted by any intermediary systems. Exceptions may apply such as connecting to systems on a trusted LAN (home network) or encrypted VPN connection on a trusted network.

There are some conceivable workarounds for this problem, the simplest probably involving reverse proxying.  Because the RCON protocol should not mirror the admin password back to the client, an encrypted tunnel from the client end to a reverse proxy engine on the serverside could exist to mask the initial password transmission accompanied with opening and maintaining RCON TCP sessions.  After the initial handshake, the server responds in plain text.  The reverse proxy can detect when receiving SSL encrypted transmissions, and passthrough clear text transmissions.



Whodunit
======
Again, this is a learning project, but constructive criticism or push requests are welcome!  If you wish to reach the owner, contact paws@delimitize.com .
