import os, pickle, events

class Game():
    def __init__(self, name, player, maps, currentmap, bots, kobots, data={}):
        self.name = name
        self.player = player
        self.maps = maps
        self.bots = bots
        self.kobots = kobots
        self.events = data['events']
        self.currentmap = currentmap
        self.savedata = {}
        self.configdata = {}
        self.data = data
        
    def regSave(self, dat):
        """Load a save file (actually a dictionary)"""
        self.name = dat['name']
        self.player.health = dat['health']
        self.player.inv = dat['inv']
        self.player.xp = dat['xp']
        self.currentmap = dat['map']
        self.player.pos = dat['pos']
        self.data['setMap'](int(dat['map']), False)
        self.data['money'] = dat['money']
        
        #0: pos, 1:kind, 2:data, 3:once, 4:fired
        
        for i in dat['events']:
            self.events[i[0]] = events.Event(i[0], i[1], i[2], i[3])
            self.events[i[0]].fired = i[4]

        for i in dat['bots']:
            if i in self.bots.value():
                self.kobots[i] = self.bots[i]
                del self.bots[i]

    def writeSave(self, File):
        ev = []
        for r in self.events.value():
            i = self.events[r]
            ev.append([i.pos, i.kind, i.data, i.once, i.fired])
        d = {
            'name':self.name,
            'health':self.player.health,
            'pos':self.player.pos,
            'inv':self.player.inv,
            'lvlid':self.player.lvlid,
            'bots':self.kobots.value(),
            'xp':self.player.xp,
            'map':self.currentmap,
            'money':self.player.money,
            'events':ev
        }
        f = open(File, "w")
        pickle.dump(d, f)
        f.close()

class GlobalVar():
    def __init__(self, Type, e):
        self.t = Type
        self.e = e
    def value(self): return self.e
    def __str__(self): return repr(self.e)
    def __getitem__(self, index=None): 
        if index == None: return self.e
        else: return self.e[index]
    def __setitem__(self, key, value): self.e[key] = value
    def __getitem__(self, key): return self.e[key]
    def set(self, value): self.e = value

def CLS(numlines=100):
    '''Clear the screen in an os friendly way'''
    if os.name == "posix": os.system('clear')
    elif os.name in ("nt", "dos", "ce"): os.system('CLS')
    else: print '\n' * numlines

def pB(pa, pb):
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

def printInv(PLAYER, x=0):
    print "INVENTORY:"
    for i in PLAYER.inv:
        if PLAYER.inv[i] != None: print "Slot %s: %s" % (i, PLAYER.inv[i].name)
    print "HEALTH:", str(PLAYER.health[0])+"/"+str(PLAYER.health[1])
    print "MONEY: %s/%s" % (PLAYER.money[0], PLAYER.money[1])
    print "XP: %s" % (PLAYER.xp)
    raw_input()

def canInt(number):
    try:
        blah = int(number)
        return True
    except:
        return False
    