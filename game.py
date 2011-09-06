import sys, os, time
import subprocess
import reqs

EVENTS = {}
ITEMS = {}

def invChange(slot, change):
    p1.inv[slot] = change

def invHandle(inp, p):
    print "Your Inventory: "
    for i in p.inv:
        if p.inv[i] != None:
            if p.inv[i].type == "weapon":
                print "Slot #"+str(i)+":", p.inv[i].name, "("+str(p.inv[i].data["health"])+"/"+str(p.inv[i].data["maxhealth"])+")"
    raw_input()

def pBetween(pa, pb):
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
        ya = 0
        xa = 0
        print "DEBUG:"
        print "Player Position [x,y]: ", p1.pos
        for y in self.m:
            print ""
            for x in self.m[y]:
                if [x,y] == p1.pos:
                    print "X",
                elif (x,y) in self.hitmap:
                    print "+",
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

    def move(self, x=0, y=0):
        go = True
        nPos = [self.pos[0]+x, self.pos[1]+y]
        x = nPos[0]
        y = nPos[1]
        eventCheck(self.clevel,(x,y))
        if (x,y) in self.clevel.hitmap.keys():
            go = False
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
MAPS = {"m1":m1,"m2":m2}
currentmap = m1
resetpos = False
p1.clevel = currentmap
ITEMS[1] = Item(1, "Wood Sword", {"damage":1, "health":30, "maxhealth":30}, "weapon")
for i in range(1,10):
    p1.inv[i] = None

def tick(count=1, pr="map"):
    global currentmap
    global resetpos
    global p1
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
            elif inp.startswith("down"):
                new = inp.split(" ")
                if len(new) <= 1: n = 1
                else: n = int(new[1])
                p1.move(y=n)
            elif inp.startswith("up"):
                new = inp.split(" ")
                if len(new) <= 1: n = -1
                else: n = int(new[1])*int(-1)
                p1.move(y=n)
            elif inp.startswith('left'):
                new = inp.split(" ")
                if len(new) <= 1: n = -1
                else: n = int(new[1])*int(-1)
                p1.move(x=n)
            elif inp.startswith('right'):
                new = inp.split(" ")
                if len(new) <= 1: n = 1
                else: n = int(new[1])
                p1.move(x=n)
            elif inp.startswith('reset'):
                p1.pos = [1,1]
            elif inp.startswith('inv'):
                invHandle(inp, p1)

def gLoop():
    while True:
        tick()
gLoop()