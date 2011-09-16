#IMPORTS
import sys, os, time
import mapper, utils, reqs, player, events
from player import Player

#VARS AS FUNCS
_loadmap = mapper.load
_cls = utils.CLS

#GLOBALS
TICK = 0
USR_INP = ""
CURRENT_MAP = ""
PLAYER = ""
EVENTS = {}
ITEMS = {}

def printInv():
    print "HEALTH:", str(PLAYER.health[0])+"/"+str(PLAYER.health[1])
    print "INVENTORY:", [PLAYER.inv[i].name for i in PLAYER.inv if PLAYER.inv[i] != None]
    raw_input()

def genDebug():
   return {'tick':TICK}

def _tick_loop():
    global EVENTS
    def resPos():
        print "Player position is BAD. (Hackz?)"
        raw_input()
        PLAYER.pos = [2,2]
    if PLAYER.health < 0:
       print "You died! DEBUG:"
    if tuple(PLAYER.pos) in CURRENT_MAP.hMap:
       if CURRENT_MAP.hMap[tuple(PLAYER.pos)][1] == "0":
           resPos()
    else:
        resPos()
    if tuple(PLAYER.pos) in EVENTS.keys():
      EVENTS[tuple(PLAYER.pos)].fire()

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
    elif inp2[0]=="w" or inp.startswith("up"):
        if len(inp2) <= 1: n = 1
        else: n = int(inp2[1]) 
        PLAYER.move(y=int(n)*int(-1))
    elif inp2[0]=="s" or inp.startswith("down"):
        if len(inp2) <= 1: n = 1
        else: n = int(inp2[1])
        PLAYER.move(y=int(n))
    elif inp2[0]=="a" or inp.startswith("left"):
        if len(inp2) <= 1: n = 1
        else: n = int(inp2[1])
        PLAYER.move(x=int(n)*int(-1))
    elif inp2[0]=="d" or inp.startswith("right"):
        if len(inp2) <= 1: n = 1
        else: n = int(inp2[1])
        PLAYER.move(x=int(n))
    elif inp.startswith("set"):
        PLAYER.setPos(eval(inp2[1]))
    elif inp.startswith("inv"):
        printInv()


def loadMap(Map):
    pass

def init():
    global PLAYER
    global CURRENT_MAP
    global EVENTS
    load = _loadmap(reqs.testlevel, None)
    CURRENT_MAP = load[0]
    EVENTSz = load[1]
    PLAYER = Player("Jimmy", [2,2], CURRENT_MAP)
    CURRENT_MAP.player = PLAYER
    for i in EVENTSz:
        i = EVENTSz[i]
        r = i[2]
        r["player"] = PLAYER
        EVENTS[i[0]] = events.Event(i[0], i[1], r, i[3])
   


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

