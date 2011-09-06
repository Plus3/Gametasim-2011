import sys, os, time
import subprocess
import reqs

EVENTS = {}

#Levels: {level1: obj,level2:obj}
#Current Level: exec (object)
#Player: player obj
#Objects: dict of objs: {"name":exec}
def eventCheck(Mp,pos):
    if pos in Mp.em:
        TYPE = Mp.em[pos]['event']
        DATA = Mp.em[pos]['data']
        EVENT = Event(pos, TYPE, DATA)
        EVENT.go()
    else:
        pass

def CLS(numlines=100):
    if os.name == "posix":
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        os.system('CLS')
    else:
        print '\n' * numlines

class Event():
    def __init__(self, location, etype, data):
        self.pos = location
        self.type = etype
        self.data = data
    def go(self, *inp):
        types = {
            "msg":self.msg,
            "exe":self.exe,
            "end":self.end,
            "cmap":self.cMap
        }
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
        time.sleep(5)

    def exe(self, pos, data):
        data()

    def end(self, pos, data):
        sys.exit()
    
    def cMap(self, pos, data):
        global currentmap
        if data[0] in MAPS:
            currentmap = MAPS[data[0]]
            if data[1] is True:
                p1.pos = data[2]
        else:
            pass

class Engine():
    def __init__(self, maps, currentmap, player, objects):
        self.maps = maps
        self.cmap = currentmap
        self.player = player
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
        self.player = player
    
    def pMap(self):
        ya = 0
        xa = 0
        print "DEBUG:"
        print "Player Position [x,y]: ",self.player.pos
        for y in self.m:
            print ""
            for x in self.m[y]:
                if [x,y] == self.player.pos:
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
    
    def move(self, x=0, y=0):
        nPos = [self.pos[0]+x, self.pos[1]+y]
        x = nPos[0]
        y = nPos[1]
        eventCheck(self.clevel,(x,y))
        if (x,y) in self.clevel.hitmap.keys():
            pass
        else:
            if y in self.clevel.m.keys():
                if x in self.clevel.m[y]:
                    self.pos = nPos
    def set(self, pos):
        self.pos = pos

p1 = Player("Joe",[1,1],"1",{})
m1 = Map(reqs.level1_map1, reqs.level1_hitmap1, reqs.level1_objmap1, player=p1)
m2 = Map(reqs.level1_map2, reqs.level1_hitmap2, reqs.level1_objmap1, player=p1)
MAPS = {"m1":m1,"m2":m2}
currentmap = m1
p1.clevel = currentmap

def gLoop():
    global currentmap
    while True:
        CLS()
        currentmap.pMap()
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
gLoop()