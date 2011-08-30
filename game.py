from pprint import *
import sys,os,time
import reqs, titles

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
	def __init__(self, name, level):
		self.name = name
		self.lvl = level

class Level():
	def __init__(self, Map, hitmap, objmap, limit):
		self.map = Map
		self.hmap = hitmap
		self.omap = objmap
		self.xlim = limit[0]
		self.ylim = limit[1]

class Player():
	def __init__(self, game, name, pos):
		self.name = name
		self.game = game
		self.x = pos[0]
		self.y = pos[1]
		self.pos = [self.x,self.y]

	def move(self, x=0, y=0):
		goto = [self.x+x,self.y+y]
		print goto
		if x == -1 and self.x == 1: badc()
		elif y == -1 and self.y == 1: badc()
		elif x == 1 and self.x == self.game.lvl.xlim: badc()
		elif y == 1 and self.y == self.game.lvl.ylim: badc()
		else:
			self.x = self.x + x
			self.y = self.y + y
			self.pos = [self.x,self.y]
	def set(self, x, y):
		self.x = x
		self.y = y
		self.pos = [self.x, self.y]

def printLvl(level, player=None):
	if player:
		for y in level:
			print ""
			for x in level[y]:
				if player.pos == [x,y]:
					print "X",
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
	L1 = Level(reqs.level1,reqs.level1_hit,reqs.level1_obj,reqs.level1_limit)
	G = Game("The Game",L1)
	P = Player(G, "Joe", [1,1])
	raw_input("PRESS ENTER TO CONTINUE!  ")
	loop(L1,G,P)

def loop(L1,G,P):
	printLvl(G.lvl.map,P)
	print ""
	while True:
		CLS()
		printLvl(G.lvl.map,P)
		print " "
		inp = raw_input("=> ")
		if inp:
			if inp == "quit" or inp == "exit":
				print "G'BYE!"
				time.sleep(.2)
				sys.exit()
			elif inp == "reset":
				P.set(1,1)
			elif inp == "left":
				P.move(x=-1)
			elif inp == "right":
				P.move(x=1)
			elif inp == "down":
				P.move(y=1)
			elif inp == "up":
				P.move(y=-1)
			else:
				badc()
if __name__ == "__main__":
	init()