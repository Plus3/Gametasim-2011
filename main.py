#IMPORTS
import sys, os, time, pickle
import mapper, utils, reqs, player, events, ai, combat, sound, tutorial
from player import Player
from utils import GlobalVar, Game
import random

_Version_ = 0.6
_Author_ = "@B1naryth1ef"

#VARS AS FUNCS
_cls = utils.CLS

#GLOBALS
useAudio = True
NEW_GAME = False
TICK = 0
USR_INP = ""
GAME = ""
MAPS = GlobalVar("MAPS", {})
CURRENT_MAP = GlobalVar("CURRENT_MAP", "")
EVENTS = GlobalVar("EVENTS", {})
SOUNDS = GlobalVar("SOUNDS", {})
BOTS = GlobalVar("BOTS", {})
KO_BOTS = GlobalVar("BOTS", {})
ITEMS = {}
PLAYER = ""

if useAudio is True:
    devPlay = lambda sound: SOUNDS.e[sound].play()
    devStop = lambda sound: SOUNDS.e[sound].stop()
else:
    devPlay = lambda x: x
    devStop = lambda x: x
_tick = lambda: TICK+1
getInput = lambda msg: raw_input(msg).lower()

def hax(pos):
    """Takes in a player pos and returns True if the player is out of map bounds. Input: [x,y] or (x,y)"""
    if sum(pos) <= 0: return True
    elif tuple(pos) in CURRENT_MAP.value().hMap and CURRENT_MAP.value().hMap[tuple(pos)][1] == 0: return True
    elif tuple(pos) not in CURRENT_MAP.value().hMap: return True

def delBot(name, iid=False):
    """Removes a bot from the playing field and moves it to KO_BOTS"""
    global BOTS
    if name is not False:
        for i in BOTS.value():
            if BOTS[i].name == name:
                KO_BOTS[i] = BOTS[i]
                BOTS[i].alive = False
                break
    elif iid is not False:
        for i in BOTS.value():
            if BOTS[i].id == iid:
                KO_BOTS[i] = BOTS[i]
                BOTS[i].alive = False
                break

def Exit(clean=True):
    """Exits, writing saves and stoping sounds if input is True, otherwise just exits."""
    global GAME, EVENTS, PLAYER
    if clean == True:
        if useAudio is True:
            for i in SOUNDS.value():
                SOUNDS[i].stop()
        GAME.writeSave(os.path.join(os.getcwd(), "data", "saves", PLAYER.name+'.dat'))
        r = open('maps.dat', 'w')
        pickle.dump({1:MAPS.e[1], 2:MAPS.e[2], 3:MAPS.e[3], 'bots':BOTS}, r)
    sys.exit()

def attackr(inp):
    """Checks if player can attack a bot, and attacks it if they can"""
    global PLAYER, BOTS, CURRENT_MAP
    m = ai.getPoss(PLAYER.pos)
    try:
        for i in BOTS.value():
            if BOTS[i].level == CURRENT_MAP.value().id:
                if tuple(BOTS[i].pos) in m:
                        combat.battle(PLAYER, BOTS[i], CURRENT_MAP.value(), False, {'printInv':utils.printInv, 'delBot':delBot, 'cls':_cls})
    except: pass

def _tickAfter(): pass

def _tickFinal(): pass

def _tickBefore():
    """_tick manager for Before events"""
    global EVENTS, BOTS, CURRENT_MAP, PLAYER, MAP_ID, GAME

    GAME.currentmap = CURRENT_MAP.value().id
    if random.randint(1,300) == 150:
        amount = random.randint(10,30)
        raw_input("You found $%s!" % (amount)) 
        PLAYER.moneyAdd(amount)

    def resPos():
        print "Player position is BAD. (Hackz?)"
        x = raw_input()
        if x == "skip": return None
        else: PLAYER.pos = [2,2]

    if PLAYER.health[0] < 1:
       print "You died! DEBUG: ", PLAYER.health
       raw_input("[Exit]")
       sys.exit()
    
    if hax(PLAYER.pos) is True: resPos()

    if tuple(PLAYER.pos) in EVENTS.value().keys():
      EVENTS.e[tuple(PLAYER.pos)].fire()

    for i in BOTS.value():
        if BOTS[i].level == CURRENT_MAP.value().id and BOTS[i].pr == True and BOTS[i].alive is True:
            BOTS[i].move()
    
    for i in BOTS.value():
        if BOTS[i].level == CURRENT_MAP.value().id:
            if tuple(BOTS[i].pos) in ai.getPoss(PLAYER.pos) or BOTS[i].pos == PLAYER.pos:
                if BOTS[i].atk is True and BOTS[i].alive is True:
                    combat.battle(PLAYER, BOTS[i], CURRENT_MAP.value(), True, {'printInv':utils.printInv, 'delBot':delBot, 'cls':_cls})
                    break #@DEV If more then one bot attacks, should we let it happen? Or ignore one like we are doing now?

def itemFire(iid):
    global PLAYER, ITEMS
    if PLAYER.hasSlot(iid) is True and PLAYER.inv[iid].isFood is True: PLAYER.eat(iid)

def _handle(inp):
    """Parse/handle a user input"""
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
    elif inp2[0]=="use":
        if len(inp2) <= 1: raw_input("Must supply inventory slot number!")
        else: itemFire(int(inp2[1]))
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
    """Initiates a map"""
    global EVENTS
    for i in eventz:
        r = eventz[i]
        l = r[2]
        l['player'] = ''
        x = events.Event(r[0], r[1], l, r[3])
        EVENTS.e[r[0]] = x  
  
def setChar(Map, pos, char):
    """Sets a char"""
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
    """Add data stuffz to all our events"""
    global PLAYER, CURRENT_MAP, EVENTS, MAPS, SOUNDS
    for i in EVENTS.e:
        EVENTS[i].data["player"] = PLAYER
        EVENTS[i].data["cmap"] = CURRENT_MAP
        EVENTS[i].data['setter'] = setMap 
        EVENTS[i].data['setChar'] = setChar
        EVENTS[i].data['exit'] = Exit
        EVENTS[i].data['sounds'] = SOUNDS
        EVENTS[i].data['globmaps'] = MAPS

def setMap(ID, rPlayer=True, pos=[2,2]):
    """Set a map"""
    global CURRENT_MAP, MAPS, PLAYER, EVENTS
    print CURRENT_MAP.e.id, ID
    CURRENT_MAP.set(MAPS[int(ID)])
    PLAYER.level = CURRENT_MAP.value()
    PLAYER.lvlid = ID
    EVENTS.set({})
    initMap(CURRENT_MAP.value().events)
    initEvents()
    if rPlayer is True:
        PLAYER.pos = pos

def retMap(ID): return MAPS[ID]
def regMapz():
    global PLAYER, MAPS
    for i in MAPS.value():
        MAPS[i].player = PLAYER

def init(dat=None):
    global PLAYER, CURRENT_MAP, EVENTS, GAME, MAPS, BOTS, KO_BOTS, SOUNDS, useAudio
    if NEW_GAME is True:
        name = getInput("Your Name: ")
        m = getInput("Play the tutorial? [Y/N]: ")
        if m == "y": tutorial.start()
        MAPS[1] = mapper.Map(1, reqs.testlevel, reqs.testlevel_hit, PLAYER, reqs.testlevel_events, GlobalVar("BOTS1", {}), {'BOTS':BOTS.value()})
        MAPS[2] = mapper.Map(2, reqs.testlevel2, reqs.testlevel2_hit, PLAYER, reqs.testlevel2_events, GlobalVar("BOTS2", {}), {'BOTS':BOTS.value()})
        MAPS[3] = mapper.Map(3, reqs.testlevel3, reqs.testlevel3_hit, PLAYER, reqs.testlevel3_events, GlobalVar("BOTS3", {}), {'BOTS':BOTS.value()})
        CURRENT_MAP.set(MAPS[1])
        initMap(CURRENT_MAP.e.events)
        PLAYER = Player(name, [2,2], CURRENT_MAP, 1, {'retMap':retMap, 'setMap':setMap})
        BOTS[1] = ai.Enemy(1, "Evil Bunny", PLAYER, [6,4], 1, [5,5], True, True, data={'attack':1,'char':".", "maps":MAPS.value(), "level":1, 'current':CURRENT_MAP})
        BOTS[2] = ai.Enemy(2, "Ye Old Ogre", PLAYER, [10,4], 2, [10,10], True, True, data={'attack':3.5,'char':"O", "maps":MAPS.value(), "level":2, 'current':CURRENT_MAP})
        BOTS[3] = ai.Enemy(3, "Evil Bunny", PLAYER, [2,2], 3, [8,8], True, True, data={'attack':1,'char':".", "maps":MAPS.value(), "level":3, 'current':CURRENT_MAP})
        BOTS[4] = ai.Enemy(4, "Evil Bunny", PLAYER, [8,4], 3, [8,8], True, True, data={'attack':1,'char':".", "maps":MAPS.value(), "level":3, 'current':CURRENT_MAP})
        BOTS[5] = ai.Enemy(5, "Evil Bunny", PLAYER, [7,7], 3, [15,15], True, True, data={'attack':1,'char':".", "maps":MAPS.value(), "level":3, 'current':CURRENT_MAP})
        BOTS[2].doMove = False
        MAPS[1].bots[1] = BOTS[1]
        MAPS[2].bots[2] = BOTS[2]
        MAPS[3].bots[3] = BOTS[3]
        MAPS[3].bots[4] = BOTS[4]
        MAPS[3].bots[5] = BOTS[5]
        regMapz()
        GAME = Game("Gametasim", PLAYER, MAPS.value(), 1, BOTS, KO_BOTS, {'setMap':setMap, 'events':EVENTS})
        SOUNDS["pok1"] = sound.Sound("pok1", './data/sounds/pok1.wav', useAudio)
        initEvents()
    elif NEW_GAME is False:
        r = open('maps.dat', 'rw')
        mapz = pickle.load(r)
        r.close()
        BOTS = mapz['bots']
        MAPS.e[1] = mapz[1]
        MAPS.e[2] = mapz[2]
        MAPS.e[3] = mapz[3]
        CURRENT_MAP.set(MAPS[1])
        PLAYER = Player(dat[1], [2,2], CURRENT_MAP, 1, {'retMap':retMap, 'setMap':setMap})
        MAPS[1].player = PLAYER
        MAPS[2].player = PLAYER
        GAME = Game("Gametasim", PLAYER, MAPS, 1, BOTS, KO_BOTS, {'setMap':setMap, 'events':EVENTS})
        SOUNDS["pok1"] = sound.Sound("pok1", './data/sounds/pok1.wav', useAudio)
        initEvents()
        GAME.regSave(dat[0])

def findSaves(home=os.getcwd()):
    """Find save files, and return a list of them"""
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
    print "Version %s" % (_Version_)
    print "Online @ github.com/b1naryth1ef/Gametasim-2011"
    print ""

def menu():
    """Main menu"""
    global GAME, NEW_GAME
    title()
    saves = findSaves()
    if len(saves) > 0:
        d1 = getInput("[U]se save, [C]reate new game or [D]elete save\n => ")
        if d1 == 'u' or d1 == 'd':
            NEW_GAME = False
            print "Game saves: "
            x = 0
            m = {}
            for i in saves:
                x += 1
                m[x] = (i, i.split("/")[-1].split(".dat")[0])
                print "[%s] " % (x)+i.split("/")[-1].split(".dat")[0]
            d2 = raw_input("Which save? ")
            if d1 == "u":
                try:
                    f = open(m[int(d2)][0], "rw")
                    return (pickle.load(f), m[int(d2)][1])
                except Exception, e:
                    print "Error!", e
                    menu()
            elif d1 == "d":
                try:
                    print "Deleting save..."
                    os.remove(m[int(d2)][0])
                    menu()
                except Exception, e:
                    print 'Error!',e
                    menu()
        elif d1 == "c": NEW_GAME = True
        elif d1 == "exit": sys.exit()
        else:
            raw_input("Huh?") 
            menu()
    else: NEW_GAME = True
    
def loop():
    """ITZ ALL IN HERE!"""
    global PLAYER, TICK, CURRENT_MAP, USR_INP, BOTS
    while True:
        TICK = _tick()
        _tickBefore()
        _cls()
        print "DEBUG:"
        print "Position: ",PLAYER.pos,"Last:",PLAYER.lastPos
        print "Tick #: ", TICK
        print "Map ID: ", CURRENT_MAP.value().id
        CURRENT_MAP.value().render()
        _tickAfter()
        USR_INP = raw_input('\n=> ')
        _handle(USR_INP)
        _tickFinal()

if __name__ == "__main__":
   # try:
    _blank = menu()
    _blank = init(_blank)
    _blank = loop()
    #except KeyboardInterrupt, e: sys.exit()
    #except Exception, e: print "General Error:",e

    
