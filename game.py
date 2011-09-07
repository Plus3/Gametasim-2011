import sys, os, time
import subprocess
import reqs, ai

EVENTS = {}
ITEMS = {}
BOTS = {}
COMMANDS = {}
botPos = []

def checkGen():
    '''Events to check on each tick'''
    if p1.health != 0:
        pass
    else:
        print "YOU DIED!"
        raw_input()
        sys.exit()

def botTick():
    '''Move bots on each tick...'''
    for i in BOTS:
        if BOTS[i].enabled is True:
            BOTS[i].move()

def invChange(slot, change):
    '''Scoped inventory changeing of player (by slot)'''
    p1.inv[slot] = change

def invHandle(inp, p):
    '''Print inventory, and other info...'''
    print "Health: "+str(p.health)+"/50"
    print "Your Inventory: "
    for i in p.inv:
        if p.inv[i] != None:
            if p.inv[i].type == "weapon":
                print "Slot #"+str(i)+":", p.inv[i].name, "("+str(p.inv[i].data["health"])+"/"+str(p.inv[i].data["maxhealth"])+")"
    raw_input()

def pBetween(pa, pb):
    '''Get the points between two points'''
    pa1 = pa[0]+pa[1]
    pa2 = pb[0]+pb[1]
    if pa1 < pa2:
        p1f = pa
        p2f = pb
    else:
        p1f = pb
        p2f = pa
    xs = range(p1f[0] + 1, p2f[0]) or [p1f[0]]
    ys = range(p1f[1] + 1, p2f[1]) or [p1f[1]]
    return [(x,y) for x in xs for y in ys]

def eventCheck(Mp,pos):
    '''Check if event already exsists, and fire it if so, otherwise create a new event'''
    if pos in EVENTS:
        EVENTS[pos].go()
    elif pos in Mp.em:
        TYPE = Mp.em[pos]['event']
        DATA = Mp.em[pos]['data']
        ONCE = Mp.em[pos]['once']
        EVENT = Event(pos, TYPE, DATA, ONCE)
        EVENT.go()
        EVENTS[pos] = EVENT
    else:
        pass

def CLS(numlines=100):
    '''Clear the screen in an os friendly way'''
    if os.name == "posix":
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        os.system('CLS')
    else:
        print '\n' * numlines

class Item():
    def __init__(self, iid, name, data, tp):
        self.id = iid
        self.name = name
        self.data = data
        self.type = tp
    
class Enemy():
    def __init__(self, name, data):
        self.name = name
        self.enabled = False
        self.health = data["health"]
        self.attack = data["attack"]
        self.attacktick = 1
        self.pos = data["pos"]
    
    def atk(self):
        p1.health -= self.attack
        print "Ouch! "+self.name+" attacked you!"
        raw_input()

    def move(self):
        r = self.pos[0] - p1.pos[0]
        g = self.pos[1] - p1.pos[1]
        if r == 1 and g == 1:
            self.atk()
        else:
            nPos = list(ai.ai(self.pos,p1.pos,p1.clevel.m))[1]
            self.pos = list(nPos)

class Event():
    def __init__(self, location, etype, data, once):
        self.pos = location
        self.type = etype
        self.data = data
        self.once = once
        self.fired = False

    def go(self, *inp):
        if self.once is True:
            if self.fired is True:
                pass
            elif self.fired is False:
                self.fire(inp)
        else: 
            self.fire(inp)  

    def fire(self, inp):
        types = {
            "msg":self.msg,
            "exe":self.exe,
            "end":self.end,
            "cmap":self.cMap,
            "ipickup":self.pickupitem,
            "spawnenemy":self.spawnenemy
        }
        self.fired = True
        if self.type in types:
            if inp:
                Pos = inp[0]
                Data = inp[1]
            else:
                Pos = self.pos
                Data = self.data
            types[self.type](Pos,Data)

    def msg(self, pos, data):
        print data
        raw_input()

    def exe(self, pos, data):
        data()

    def end(self, pos, data):
        sys.exit()
    
    def cMap(self, pos, data):
        global currentmap
        global resetpos
        if data[0] in MAPS:
            currentmap = MAPS[data[0]]
            p1.clevel = MAPS[data[0]]
            if data[1] is True:
                resetpos = True
        else:
            pass
    
    def pickupitem(self, pos, data):
        iTem = ITEMS[data]
        print "You found a "+iTem.name
        for i in p1.inv:
            if p1.inv[i] == None:
                invChange(i,iTem)
                print "Stored in slot #"+str(i)
                _stored = True
                break
        if _stored != True:
            print "No space!"
        raw_input()
    
    def spawnenemy(self, pos, data):
        pass

class Engine():
    def __init__(self, maps, currentmap, player, objects):
        self.maps = maps
        self.cmap = currentmap
        self.objects = objects
    
    def onEvent(self, pos):
        x = self.cmap.em[pos]
        print x

class Map():
    def __init__(self, zMap, hitmap, eventmap, data={}, player=None):
        self.m = zMap #Map format
        self.hitmap = hitmap
        self.em = eventmap
        self.data = data
    
    def pMap(self):
        botPos = []
        for i in BOTS:
            botPos.append(BOTS[i].pos)
        ya = 0
        xa = 0
        print "DEBUG:"
        print "Player Position [x,y]: ", p1.pos
        print "Bot Position [x,y: ", botPos
        for y in self.m:
            print ""
            for x in self.m[y]:
                if [x,y] == p1.pos:
                    print "X",
                elif (x,y) in self.hitmap:
                    print "+",
                elif [x,y] in botPos:
                    print "$",
                else:
                    print "0",

class Player():
    def __init__(self, name, pos, currentlevel, data):
        self.name = name
        self.pos = pos
        self.clevel = currentlevel
        self.data = data
        self.inv = {}
        self.items = {}
        self.itemlist = []
        self.health = 50
        for i in range(1,10):
            self.inv[i] = None

    def move(self, x=0, y=0):
        go = True
        nPos = [self.pos[0]+x, self.pos[1]+y]
        x = nPos[0]
        y = nPos[1]
        eventCheck(self.clevel,(x,y))
        if (x,y) in self.clevel.hitmap.keys():
            go = False
        if (x,y) in BOTS:
            go = True
            nPos[0] -= 1
            BOTS[(x,y)].atk()
        for i in pBetween((x,y),(self.pos[0],self.pos[1])):
            if i in self.clevel.hitmap.keys():
                go = False
        if go is True:
            if y in self.clevel.m.keys():
                if x in self.clevel.m[y]:
                    self.pos = nPos
    def set(self, pos):
        self.pos = pos

p1 = Player("Joe",[1,1],"1",{})
m1 = Map(reqs.level1_map1, reqs.level1_hitmap1, reqs.level1_objmap1)
m2 = Map(reqs.level1_map2, reqs.level1_hitmap2, reqs.level1_objmap1)
b1 = Enemy("Botty",{"health":5,"attack":3,"pos":[9,9]})
b1.enabled = True
BOTS[tuple(b1.pos)] = b1
MAPS = {"m1":m1,"m2":m2}
currentmap = m1
resetpos = False
p1.clevel = currentmap
ITEMS[1] = Item(1, "Wood Sword", {"damage":1, "health":30, "maxhealth":30}, "weapon")


def tick(count=1, pr="map"):
    global currentmap, resetpos, p1
    CLS()
    for i in range(count):
        CLS()
        if pr == "map":
            currentmap.pMap()
        elif pr == "inv":
            for i in p1.invlist:
                print i.name
        if resetpos is True:
            p1.pos = [1,1]
            resetpos = False
            print "HEADER"
        else:
            inp = raw_input("\n=> ")
            if inp == "exit" or inp == "quit":
                sys.exit()
            elif inp == "nextmap":
                print "Next Map []"
                currentmap = m2
            elif inp.startswith("down") or inp.startswith("s"):
                new = inp.split(" ")
                if len(new) <= 1: n = 1
                else: n = int(new[1])
                p1.move(y=n)
            elif inp.startswith("up") or inp.startswith("w"):
                new = inp.split(" ")
                if len(new) <= 1: n = -1
                else: n = int(new[1])*int(-1)
                p1.move(y=n)
            elif inp.startswith('left') or inp.startswith("a"):
                new = inp.split(" ")
                if len(new) <= 1: n = -1
                else: n = int(new[1])*int(-1)
                p1.move(x=n)
            elif inp.startswith('right') or inp.startswith("d"):
                new = inp.split(" ")
                if len(new) <= 1: n = 1
                else: n = int(new[1])
                p1.move(x=n)
            elif inp.startswith('reset'):
                p1.pos = [1,1]
            elif inp.startswith('inv'):
                invHandle(inp, p1)
            else:
                new = inp.split(" ")
                if new[0] in COMMANDS:
                    COMMANDS[new[0]](inp)
        botTick()
        checkGen()

def gLoop():
    while True:
        tick()
gLoop()