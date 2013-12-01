## Development notes/TODO:

1. The minecraft interface needs to be prototyped.  Can probably reduce the amount of code greatly with some trickery
2. Open issue about Minecraft's failure to comply with RCON protocol; for now implement an 'or' check to get by. probably check mcrcon program
3. Rcon.rcon() needs to test for send failures due to noauth, and then reauth rather than bomb out and disconnect
4. Rcon.Rcon() needs disconnects
5. In Rcon.rcon(), raise exceptions as necessary for general password checking 
6. SSL possible at all with any version of minecraft or RCON? 
7. Mark low level commands private?  (not that it matters in Python)
