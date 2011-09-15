#IMPORTS
import sys, os, time
import mapper, utils, reqs, player
from player import Player

#VARS AS FUNCS
_loadmap = mapper.load
_cls = utils.CLS

#GLOBALS
TICK = 0
USR_INP = ""
CURRENT_MAP = ""
PLAYER = ""
    
def genDebug():
   return {'tick':TICK}

def _tick_loop():
    if PLAYER.health < 0:
       print "You died! DEBUG:"
    elif tuple(PLAYER.pos) not in CURRENT_MAP.hMap:
       print "Player position is BAD. (Hackz?)"
       raw_input()
       PLAYER.pos = [2,2]

def _tick(count=1, c=0):
   global TICK
   while count > c:
      c+=1
      TICK+=1
      _tick_loop()
      
def _handle(inp):
    inp2 = inp.split(" ")
    if inp.startswith("quit") or inp.startswith("exit"):
        sys.exit()
    elif inp.startswith("w ") or inp.startswith("up"):
        if len(inp2) <= 1: n = 1
        else: n = int(inp2[1]) 
        PLAYER.move(y=int(n)*int(-1))
    elif inp.startswith("s ") or inp.startswith("down"):
        if len(inp2) <= 1: n = 1
        else: n = int(inp2[1])
        PLAYER.move(y=int(n))
    elif inp.startswith("a ") or inp.startswith("left"):
        if len(inp2) <= 1: n = 1
        else: n = int(inp2[1])
        PLAYER.move(x=int(n)*int(-1))
    elif inp.startswith("d ") or inp.startswith("right"):
        if len(inp2) <= 1: n = 1
        else: n = int(inp2[1])
        PLAYER.move(x=int(n))
    elif inp.startswith("set"):
        PLAYER.setPos(eval(inp2[1]))


def init():
   global PLAYER
   global CURRENT_MAP
   CURRENT_MAP = _loadmap(reqs.testlevel, None)
   PLAYER = Player("Jimmy", [2,2], CURRENT_MAP)
   CURRENT_MAP.player = PLAYER

init()
while True:
   _tick()
   _cls()
   print "DEBUG:"
   print "Position: ",PLAYER.pos
   print "Tick #: ", TICK
   CURRENT_MAP.render()
   USR_INP = raw_input("\n=> ")
   _handle(USR_INP)

