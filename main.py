#IMPORTS
import sys, os, time, pickle
import mapper, utils, reqs, player, events, ai, combat, sound
from player import Player
from utils import GlobalVar, Game

_Version_ = 0.1
_Author_ = "@B1naryth1ef"

#VARS AS FUNCS
_cls = utils.CLS

#GLOBALS
NEW_GAME = False
TICK = 0
USR_INP = ""
GAME = ""
MAPS = GlobalVar("MAPS", {})
CURRENT_MAP = GlobalVar("CURRENT_MAP", "")
PLAYER = ""
EVENTS = GlobalVar("EVENTS", {})
ITEMS = {}
SOUNDS = GlobalVar("SOUNDS", {})
BOTS = GlobalVar("BOTS", {})
S_FILE = "save.dat"
KO_BOTS = GlobalVar("BOTS", {})
try:
    SAVE_FILE = open(S_FILE, "rw")
except:
    SAVE_FILE = open(S_FILE, "w")

devPlay = lambda sound: SOUNDS.e[sound].play()
devStop = lambda sound: SOUNDS.e[sound].stop()
_tick = lambda: TICK+1
 
def hax(pos):
    """Takes in a player pos and returns True if the player is out of map bounds. Input: [x,y] or (x,y)"""
    if sum(pos) <= 0:
        return True
    elif tuple(pos) in CURRENT_MAP.e.hMap and CURRENT_MAP.e.hMap[tuple(pos)][1] == 0:
        return True
    elif tuple(pos) not in CURRENT_MAP.e.hMap:
        return True

def delBot(name, iid=False):
    """Removes a bot from the playing field and moves it to KO_BOTS"""
    global BOTS
    if name is not False:
        for i in BOTS.e:
            if BOTS.e[i].name == name:
                KO_BOTS.e[i] = BOTS.e[i]
                del BOTS.e[i]
                break
    elif iid is not False:
        for i in BOTS.e:
            if BOTS.e[i].id == iid:
                KO_BOTS.e[i] = BOTS.e[i]
                del BOTS.e[i]
                break

def Exit(clean=True):
    """Exits, writing saves and stoping sounds if input is True, otherwise just exits."""
    global GAME, S_FILE, EVENTS, PLAYER
    if clean == True:
        for i in SOUNDS.e:
            SOUNDS.e[i].stop()
        GAME.writeSave(os.path.join(os.getcwd(), "data", "saves", PLAYER.name+'.dat'))
        r = open('maps.dat', 'w')
        pickle.dump({1:MAPS.e[1], 2:MAPS.e[2], 'bots':BOTS}, r)
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
    global EVENTS, BOTS, CURRENT_MAP, PLAYER, MAP_ID, GAME

    GAME.currentmap = CURRENT_MAP.e.id

    def resPos():
        print "Player position is BAD. (Hackz?)"
        x = raw_input()
        if x == "skip":
            return None
        else:
            PLAYER.pos = [2,2]

    if PLAYER.health[0] < 1:
       print "You died! DEBUG: ", PLAYER.health
       raw_input("[Exit]")
       sys.exit()
    
    if hax(PLAYER.pos) is True: resPos()

    if tuple(PLAYER.pos) in EVENTS.e.keys():
      EVENTS.e[tuple(PLAYER.pos)].fire()

    for i in BOTS.e:
        if BOTS.e[i].level == CURRENT_MAP.e.id and BOTS.e[i].pr == True:
            BOTS.e[i].move()
    
    for i in BOTS.e:
        if BOTS.e[i].level == CURRENT_MAP.e.id:
            if tuple(PLAYER.pos) in ai.getPoss(BOTS.e[i].pos):
                if BOTS.e[i].atk is True:
                    combat.battle(PLAYER, BOTS.e[i], CURRENT_MAP.e, True, {'printInv':utils.printInv, 'delBot':delBot, 'cls':_cls})
                    break
        
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
    elif inp.startswith("play"):
        devPlay(inp2[1])
    elif inp.startswith("stop"):
        devStop(inp2[1])

def initMap(eventz):
    global EVENTS
    for i in eventz:
        r = eventz[i]
        l = r[2]
        l['player'] = ''
        x = events.Event(r[0], r[1], l, r[3])
        EVENTS.e[r[0]] = x  
  
def setChar(Map, pos, char):
    global MAPS  
    r = MAPS.e[Map]
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
    global PLAYER, CURRENT_MAP, EVENTS, MAPS, SOUNDS
    for i in EVENTS.e:
        EVENTS.e[i].data["player"] = PLAYER
        EVENTS.e[i].data["cmap"] = CURRENT_MAP
        EVENTS.e[i].data['setter'] = setMap 
        EVENTS.e[i].data['setChar'] = setChar
        EVENTS.e[i].data['exit'] = Exit
        EVENTS.e[i].data['sounds'] = SOUNDS

def setMap(ID, rPlayer=True, pos=[2,2]):
    global CURRENT_MAP, MAPS, PLAYER, EVENTS
    print "setting map"
    print CURRENT_MAP.e.id, ID
    # if CURRENT_MAP.e.id != ID:
    if True:
        print "setting map 2"
        CURRENT_MAP.e = MAPS.e[int(ID)]
        PLAYER.level = CURRENT_MAP.e
        PLAYER.lvlid = ID
        EVENTS.e = {}
        initMap(CURRENT_MAP.e.events)
        initEvents()
        if rPlayer is True:
            PLAYER.pos = pos

def retMap(ID):
    return MAPS.e[ID]

def init(dat=None):
    global PLAYER, CURRENT_MAP, EVENTS, GAME, MAPS, BOTS, KO_BOTS, SOUNDS
    if NEW_GAME is True:
        MAPS.e[1] = mapper.Map(1, reqs.testlevel, reqs.testlevel_hit, PLAYER, reqs.testlevel_events, {'BOTS':BOTS.e})
        MAPS.e[2] = mapper.Map(2, reqs.testlevel2, reqs.testlevel2_hit, PLAYER, reqs.testlevel2_events, {'BOTS':BOTS.e})
        CURRENT_MAP.e = MAPS.e[1]
        initMap(CURRENT_MAP.e.events)
        PLAYER = Player(raw_input("Your Name: "), [2,2], CURRENT_MAP, 1, {'retMap':retMap, 'setMap':setMap})
        BOTS.e[(6,4)] = ai.Enemy(1, "Evil Bunny", PLAYER, [6,4], 1, [5,5], True, True, data={'attack':1,'char':".", "maps":MAPS.e, "level":1})
        MAPS.e[1].player = PLAYER
        MAPS.e[2].player = PLAYER
        GAME = Game("Gametasim", PLAYER, MAPS.e, 1, BOTS, KO_BOTS, {'setMap':setMap, 'events':EVENTS})
        SOUNDS.e["pok1"] = sound.Sound("pok1", './data/sounds/pok1.wav')
        initEvents()
    elif NEW_GAME is False:
        r = open('maps.dat', 'rw')
        mapz = pickle.load(r)
        r.close()
        BOTS = mapz['bots']
        MAPS.e[1] = mapz[1]
        MAPS.e[2] = mapz[2]
        CURRENT_MAP.e = MAPS.e[1]   
        PLAYER = Player(dat[1], [2,2], CURRENT_MAP, 1, {'retMap':retMap, 'setMap':setMap})
        MAPS.e[1].player = PLAYER
        MAPS.e[2].player = PLAYER
        GAME = Game("Gametasim", PLAYER, MAPS.e, 1, BOTS, KO_BOTS, {'setMap':setMap, 'events':EVENTS})
        SOUNDS.e["pok1"] = sound.Sound("pok1", './data/sounds/pok1.wav')
        initEvents()
        GAME.regSave(dat[0])

def findSaves(home=os.getcwd()):
    fn = []
    try:
        for i in os.listdir(os.path.join(home, "data", 'saves')):
            if i.endswith('.dat') and not i.startswith("_"):
                fn.append(os.path.join(home, 'data', 'saves', i))
        return fn
    except:
        os.mkdir(os.path.join(home, 'data', 'saves'))
        return findSaves()

def title():
    _cls()
    print "Welcome to GAMETASIM - 2011"
    print "By: Andrei Z"
    print "Status: In Development"
    print "Online @ github.com/b1naryth1ef/Gametasim-2011"
    print ""

def menu():
    global SAVE_FILE, GAME, NEW_GAME
    title()
    saves = findSaves()
    if len(saves) > 0:
        d1 = raw_input("[U]se save OR [C]reate new game? ").lower()
        if d1 == 'u':
            NEW_GAME = False
            print "Avalible Game Saves:"
            x = 0
            m = {}
            for i in saves:
                x += 1
                m[x] = (i, i.split("/")[-1].split(".dat")[0])
                print "[%s] " % (x)+i.split("/")[-1].split(".dat")[0]
            d2 = raw_input("What save? ")
            try: 
                f = open(m[int(d2)][0], "rw")
                return (pickle.load(f), m[int(d2)][1])
            except Exception, e:
                print "Error!", e
                menu()
        elif d1 == "c":
            NEW_GAME = True
            return (None, None)
    else:
        NEW_GAME = True
    
def loop():
    global PLAYER, TICK, CURRENT_MAP, USR_INP
    while True:
       TICK = _tick()
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
    _blank = menu()
    _blank = init(_blank)
    _blank = loop()

    