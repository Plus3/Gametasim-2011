from pprint import *
import sys,os,time
import reqs, titles

mup = lambda P, y: P.move(y=y) 
mdown = lambda P, y: P.move(y=y)
mright = lambda P, y: P.move(x=y)
mleft = lambda P, y: P.move(x=y)
play = True

def hitcheck(level,x,y):
    for i in level:
        if [x,y,1] == i:
            return True
        elif [x,y,0] == i:
            return True
        else:
            pass
    return False

def handle(level,pos,G):
    G.lvl = G.lvl2

def badc():
    print "XXXXXX"
    time.sleep(.2)

def CLS(numlines=100):
    if os.name == "posix":
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        os.system('CLS')
    else:
        print '\n' * numlines

class Game():
    def __init__(self, name, *levels):
        self.name = name
        self.lvl = levels[0] #Current level
        self.lvl1 = levels[0]
        self.lvl2 = levels[1]
        #self.lvln = levelname

class Level():
    def __init__(self, Map, hitmap, objmap, limit, actions):
        self.map = Map
        self.hmap = hitmap
        self.omap = objmap
        self.xlim = limit[0]
        self.ylim = limit[1]
        self.lim = limit
        self.actions = actions

class Player():
    def __init__(self, game, name, pos):
        self.name = name
        self.game = game
        self.x = pos[0]
        self.y = pos[1]
        self.pos = [self.x,self.y]

    def move(self, x=0, y=0):
        new_x = self.x+int(x)
        new_y = self.y+int(y)
        goto = [self.x+int(x),self.y+int(y)]
        Map = self.game.lvl.map
        go = True
        try:
            _blank = Map[new_y]
            if hitcheck(self.game.lvl.hmap,new_x,new_y): KeyError("")
            elif goto in self.game.lvl.omap: 
                handle(self.game.lvl,goto,self.game)
                self.x = 1
                self.y = 1
                self.pos = [1,1]
            elif new_x in _blank:
                self.x = new_x
                self.y = new_y
                self.pos = goto
            else:
                raise KeyError("")
        except KeyError, e:
            print e
            go = False
        return go
            
    def set(self, x, y):
        self.x = x
        self.y = y
        self.pos = [self.x, self.y]

def printLvl(G, player=None):
    if player:
        for y in G.lvl.map:
            print ""
            for x in G.lvl.map[y]:
                if player.pos == [x,y]:
                    print "X",
                elif [x,y,1] in G.lvl.hmap:
                    print "-",
                elif [x,y,0] in G.lvl.hmap:
                    print "|",
                elif [x,y] in G.lvl.omap:
                    print "+",
                else:
                    print "0",                
    if not player:
        for i1 in level.values():
            print ""
            for i2 in i1:
                print "0",

def init():
    CLS()
    titles.main()
    L1 = Level(reqs.level1,reqs.level1_hit,reqs.level1_obj,reqs.level1_limit,reqs.level1_actions)
    L2 = Level(reqs.level2,reqs.level2_hit,reqs.level2_obj,reqs.level2_limit,reqs.level2_actions)
    G = Game("The Game",L1,L2)
    P = Player(G, "Joe", [1,1])
    raw_input("PRESS ENTER TO CONTINUE!  ")
    loop(G,P)

def loop(G,P):
    printLvl(G,P)
    print ""
    while play == True:
        CLS()
        printLvl(G,P)
        print " "
        inp = raw_input("=> ")
        if inp:
            if inp.startswith("quit") or inp.startswith("exit"):
                print "G'BYE!"
                time.sleep(.2)
                sys.exit()
            elif inp.startswith("reset"):
                N = inp.split(" ")
                P.set(1,1)
            elif inp.startswith("left"):
                N = inp.split(" ")
                if len(N) <= 1: n = -1
                else: n = int(N[1])*int(-1)
                mleft(P,n)
            elif inp.startswith("right"):
                N = inp.split(" ")
                if len(N) <= 1: n = 1
                else: n = N[1]
                mright(P,int(n))
            elif inp.startswith("down"):
                N = inp.split(" ")
                if len(N) <= 1: n = 1
                else: n = N[1]
                mdown(P,int(n))
            elif inp.startswith("up"):
                N = inp.split(" ")
                if len(N) <= 1: n = -1
                else: n = int(N[1])*int(-1)
                mup(P,n)
            else:
                badc()
            
if __name__ == "__main__":
    init()