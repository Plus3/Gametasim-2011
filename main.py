#IMPORTS
import sys, os, time
import mapper, utils, reqs, player, events
from player import Player
from utils import GlobalVar, Game

#VARS AS FUNCS
_cls = utils.CLS

#GLOBALS
TICK = 0
USR_INP = ""
GAME = ""
MAPS = {}
CURRENT_MAP = GlobalVar("CURRENT_MAP", "")
PLAYER = ""
EVENTS = {}
ITEMS = {}
S_FILE = "save.dat"
SAVE_FILE = open(S_FILE, "rw")

def Exit():
    global GAME, S_FILE
    GAME.writeSave(S_FILE)
    sys.exit()

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
    if PLAYER.health[0] < 1:
       print "You died! DEBUG: ", PLAYER.health
       raw_input("[Exit]")
       sys.exit()
    if tuple(PLAYER.pos) in CURRENT_MAP.e.hMap:
       if CURRENT_MAP.e.hMap[tuple(PLAYER.pos)][1] == "0":
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
        Exit()
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
    elif inp.startswith("health"):
        PLAYER.health[0] = int(inp2[1])

def initMap(eventz):
    global EVENTS
    for i in eventz:
        r = eventz[i]
        l = r[2]
        l['player'] = ''
        x = events.Event(r[0], r[1], l, r[3])
        EVENTS[r[0]] = x  
        
def initEvents():
    global PLAYER, CURRENT_MAP, EVENTS, MAPS
    for i in EVENTS:
        EVENTS[i].data["player"] = PLAYER
        EVENTS[i].data["cmap"] = CURRENT_MAP
        EVENTS[i].data['setter'] = setMap 

def setMap(ID, rPlayer=True, pos=[2,2]):
    global CURRENT_MAP, MAPS, PLAYER, EVENTS
    if CURRENT_MAP.e.id != ID:

        CURRENT_MAP.e = MAPS[int(ID)]
        PLAYER.level = CURRENT_MAP.e
        EVENTS = {}
        initMap(CURRENT_MAP.e.events)
        initEvents()
        if rPlayer is True:
            PLAYER.pos = pos

def init():
    global PLAYER, CURRENT_MAP, EVENTS, GAME, MAPS
    MAPS[1] = mapper.Map(1, reqs.testlevel, reqs.testlevel_clean, reqs.testlevel_hit, PLAYER, reqs.testlevel_events)
    MAPS[2] = mapper.Map(2, reqs.testlevel2, reqs.testlevel2_clean, reqs.testlevel2_hit, PLAYER, reqs.testlevel2_events)
    CURRENT_MAP.e = MAPS[1]
    initMap(CURRENT_MAP.e.events)
    PLAYER = Player("Jimmy", [2,2], CURRENT_MAP)
    MAPS[1].player = PLAYER
    MAPS[2].player = PLAYER
    GAME = Game("Gametasim", PLAYER, MAPS, MAPS[1])
    initEvents()

def handleSave(inp):
    global GAME
    split = inp.split("=")
    if len(split) > 2:
        print "Error on len(split): ", len(split)
    key = split[0].strip().strip(":")
    value = split[1].strip()
    write = True
    if key in GAME.savedata:
        if GAME.savedata[key] == value:
            print "DEBUG: Not writing config, value already set"
            write = False
        elif GAME.savedata[key] != value:
            write = True
    if write == True:
        GAME.savedata[key] = value
        print "Wrote key: ", key, "Value: ", value

def handleSetting(inp):
    pass

def menu():
    global SAVE_FILE, GAME

    def Use():
        GAME.regSave()

    def noUse():
        pass

    for line in SAVE_FILE.readlines():
        if line.startswith(":"):
            print "Going to handle"
            handleSave(line)
        elif line.startswith("#") or line.startswith("//"):
            pass
        elif line.startswith("!"):
            handleSetting(line)
        else:
            print "Unknown line in config: ", line
    if GAME.savedata["new"] == '0':
        _cls()
        print "Game save detected for:", GAME.savedata['name'], "!!"
        useF = raw_input("[U]se or [N]ew \n=> ").lower()
        if useF == "u":
            print "Using save data..."
            GAME.regSave()
        elif useF == "n":
            print "Deleteing save data and creating a new file..."
        else:
            print "Huh? Didnt get that!"
            menu()

            

def title():
    _cls()
    print "Welcome to GAMETASIM - 2011"
    print "By: Andrei Z"
    print "Status: In Development"
    print "Online @ github.com/b1naryth1ef/Gametasim-2011"
    print ""
    raw_input()


if __name__ == "__main__":
    init()
    title()
    menu()
    raw_input()
    while True:
       _tick()
       _cls()
       print "DEBUG:"
       print "Position: ",PLAYER.pos
       print "Tick #: ", TICK
       print "Map ID: ", CURRENT_MAP.e.id
       CURRENT_MAP.e.render()
       USR_INP = raw_input("\n=> ")
       _handle(USR_INP)