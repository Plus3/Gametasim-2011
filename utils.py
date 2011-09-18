import os

class Game():
    def __init__(self, name, player, maps, currentmap):
        self.name = name
        self.player = player
        self.maps = maps
        self.currentmap = currentmap
        self.savedata = {}
        self.configdata = {}
    
    def regSave(self):
        self.name = self.savedata['name']
        self.player.health = eval(self.savedata['health'])
        if self.savedata['inv'] != 'None':
            self.player.inv = self.savedata['inv']
    
    def writeSave(self, File):
        f = open(File, "w")
        for i in self.savedata.keys():
            line = ":"+i+"="+str(self.savedata[i])+"\n"
            f.write(line)
        f.close()

class GlobalVar():
    def __init__(self, Type, e):
        self.t = Type
        self.e  = e

def CLS(numlines=100):
    '''Clear the screen in an os friendly way'''
    if os.name == "posix":
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        os.system('CLS')
    else:
        print '\n' * numlines

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
