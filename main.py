#IMPORTS
import sys, os, time, pickle
import mapper, utils, reqs, player, events, menu, ai, combat
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
BOTS = GlobalVar("BOTS", {})
S_FILE = "save.dat"

try:
    SAVE_FILE = open(S_FILE, "rw")
except:
    SAVE_FILE = open(S_FILE, "w")

def delBot(name, iid=False):
    global BOTS
    if name is not False:
        for i in BOTS.e:
            if BOTS.e[i].name == name:
                del BOTS.e[i]
                break
    elif iid is not False:
        for i in BOTS.e:
            if BOTS.e[i].id == iid:
                del BOTS.e[i]
                break

def Exit(clean=True):
    global GAME, S_FILE
    if clean == True:
        GAME.writeSave(S_FILE)
    sys.exit()

def attackr(inp):
    global PLAYER, BOTS, CURRENT_MAP
    m = ai.getPoss(PLAYER.pos)
    try:
        for i in BOTS.e:
            if BOTS.e[i].level == CURRENT_MAP.e.id:
                for z in m:
                    if list(z) == BOTS.e[i].pos:
                        combat.battle(PLAYER, BOTS.e[i], CURRENT_MAP.e, False, {'printInv':utils.printInv, 'delBot':delBot, 'cls':_cls})
    except:
        pass

def _tickAfter():
    global BOTS, CURRENT_MAP, PLAYER
    return None

def _tickFinal(): pass

def _tickBefore():
    global EVENTS, BOTS, CURRENT_MAP, PLAYER

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

    for i in BOTS.e:
        if BOTS.e[i].level == CURRENT_MAP.e.id:
            BOTS.e[i].move()
    
    for i in BOTS.e:
        if BOTS.e[i].level == CURRENT_MAP.e.id:
            if tuple(PLAYER.pos) in ai.getPoss(BOTS.e[i].pos):
                if BOTS.e[i].atk is True:
                    combat.battle(PLAYER, BOTS.e[i], CURRENT_MAP.e, True, {'printInv':utils.printInv, 'delBot':delBot, 'cls':_cls})
                    break

def _tick():
    global TICK
    TICK+=1
        
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
        utils.printInv(PLAYER)
    elif inp.startswith("health"):
        PLAYER.health[0] = int(inp2[1])
    elif inp.startswith("attack"):
        attackr(inp2)

def initMap(eventz):
    global EVENTS
    for i in eventz:
        r = eventz[i]
        l = r[2]
        l['player'] = ''
        x = events.Event(r[0], r[1], l, r[3])
        EVENTS[r[0]] = x  
  
def setChar(Map, pos, char):
    global MAPS  
    r = MAPS[Map]
    line = []
    itr = 0
    for i in r.Map[pos[1]]:
        itr += 1
        if itr == pos[0]:
            line.append(char)
        else:
            line.append(i)
    r.Map[pos[1]] = "".join(line)
      
def initEvents():
    global PLAYER, CURRENT_MAP, EVENTS, MAPS
    for i in EVENTS:
        EVENTS[i].data["player"] = PLAYER
        EVENTS[i].data["cmap"] = CURRENT_MAP
        EVENTS[i].data['setter'] = setMap 
        EVENTS[i].data['setChar'] = setChar
        EVENTS[i].data['exit'] = Exit

def setMap(ID, rPlayer=True, pos=[2,2]):
    global CURRENT_MAP, MAPS, PLAYER, EVENTS
    if CURRENT_MAP.e.id != ID:
        CURRENT_MAP.e = MAPS[int(ID)]
        PLAYER.level = CURRENT_MAP.e
        PLAYER.lvlid = ID
        EVENTS = {}
        initMap(CURRENT_MAP.e.events)
        initEvents()
        if rPlayer is True:
            PLAYER.pos = pos

def retMap(ID):
    return MAPS[ID]

def init():
    global PLAYER, CURRENT_MAP, EVENTS, GAME, MAPS, BOTS
    MAPS[1] = mapper.Map(1, reqs.testlevel, reqs.testlevel_clean, reqs.testlevel_hit, PLAYER, reqs.testlevel_events, {'BOTS':BOTS.e})
    MAPS[2] = mapper.Map(2, reqs.testlevel2, reqs.testlevel2_clean, reqs.testlevel2_hit, PLAYER, reqs.testlevel2_events, {'BOTS':BOTS.e})
    CURRENT_MAP.e = MAPS[1]
    initMap(CURRENT_MAP.e.events)
    PLAYER = Player("Jimmy", [2,2], CURRENT_MAP, 1, {'retMap':retMap, 'setMap':setMap})
    BOTS.e[(6,4)] = ai.Enemy(1, "Evil Bunny", PLAYER, [6,4], 1, [5,5], True, True, data={'attack':1,'char':".", "maps":MAPS, "level":1})
    MAPS[1].player = PLAYER
    MAPS[2].player = PLAYER
    GAME = Game("Gametasim", PLAYER, MAPS, MAPS[1], BOTS, {'setMap':setMap})
    initEvents()
    return None

def title():
    _cls()
    print "Welcome to GAMETASIM - 2011"
    print "By: Andrei Z"
    print "Status: In Development"
    print "Online @ github.com/b1naryth1ef/Gametasim-2011"
    print ""

def menu():
    global SAVE_FILE, GAME
    title()
    try:
        dat = pickle.load(SAVE_FILE)
        print "Save data for player "+dat['name']+" has been found!"
        cho = raw_input("[U]se [N]ew [D]elete\n=> ").lower()
        if cho == "u":
            print "Using data..."
            GAME.regSave(dat)
        elif cho == "n":
            print "Dumping data..."
        elif cho == "d":
            f = open(SAVE_FILE, "w")
            f.close()
        else:
            print "Unknown input!"
            time.sleep(.5)
            menu()
            #FIXME Should loop back to menu?
    except:
        return None

def loop():
    global PLAYER, TICK, CURRENT_MAP, USR_INP
    while True:
       _tick()
       _tickBefore()
       _cls()
       print "DEBUG:"
       print "Position: ",PLAYER.pos,"Last:",PLAYER.lastPos
       print "Tick #: ", TICK
       print "Map ID: ", CURRENT_MAP.e.id
       CURRENT_MAP.e.render()
       _tickAfter()
       USR_INP = raw_input("\n=> ")
       _handle(USR_INP)
       _tickFinal()

if __name__ == "__main__":
    _blank = init()
    _blank = menu()
    _blank = loop()

    