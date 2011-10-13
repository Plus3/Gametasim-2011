import utils
import random
from math import *

def getPoss(point):
	li = []

	x = point[0]
	y = point[1]

	if x-1 > 0: li.append((x-1,y))
	li.append((x+1,y))
	if y-1 > 0: li.append((x,y-1))
	li.append((x,y+1))
	return li

def axisX(a,b): 
	if a[0] > b[0]: return -1 #me[x] is more then you[x] (MOVE LEFT)
	elif a[0] == b[0]: return None #no l/r
	else: return 1 #you[x] is more then me[x] (MOVE RIGHT)

def axisY(a,b): 
	if a[1] > b[1]: return -1 #MOVE DOWN
	elif a[1] == b[1]: None #no up/down
	else: return 1 #MOVE UP

def checkPos(pos, hitmap):
	if hitmap[tuple(pos)][1] == 1: return True
	elif hitmap[tuple(pos)][1] == 0: return False
	else: return None

def testR(a,b, hitmap):
	nX = axisX(a,b)
	nY = axisY(a,b)
	if nX != None:
		newX = a[0] + nX
	if nY != None:
		newY = a[1] + nY

	if axisX(a,b) != None:
		if checkPos([newX, a[1]], hitmap) is True:
			return [newX, a[1]]
	if axisY(a,b) != None:
		if checkPos([a[0], newY], hitmap) is True: 
			return [a[0], newY]
		else:
			x = ai(a,b,hitmap)
			return x
	else:
		x = ai(a,b,hitmap)
		return x
	
def dist(a,b):
	if sum(a) < sum(b):
		rm = b[0]-a[0]
		rz = b[1]-a[1]
	elif sum(a) > sum(b):
		rm = a[0]-b[0]
		rz = a[1]-b[1]
	else:
		rm = 0
		rz = 0
	r1 = rm^2
	r2 = rz^2
	rx = r1+r2
	return sqrt(abs(rx))

def ai(me,you,Map):
	meP = getPoss(me)
	youP = getPoss(you)
	d = {}
	for a in meP: d[dist(a,you)] = a
	while d != {}:
		try:
			c = min(d.keys())
			if Map.hMap[d[c]][1] == 1:
				if Map.player.pos != list(d[c]): return d[c]
				else: del d[c]
			else: del d[c]
		except: pass
	return None
	
class Bot():
	def __init__(self, iid, name, player, pos, level, health, attack=True, bat=True, data={}):
		self.id = iid
		self.name = name
		self.pos = pos
		self.level = level
		self.player = player
		self.data = data
		self.atk = attack #If false, the bot will not attack players (aka passive)
		self.doMove = True #If false, the bot will not require move computation (nor move) on each tick
		self.bat = bat
		self.health = health
		self.pr = True #If false, the bot will not be printed.
		self.currentMap = data['current']
		self.alive = True #If false, the bot is technically dead and will not act on any events
	
	def move(self):
		if self.pr is True and self.doMove is True and self.alive is True:
			nPos = testR(self.pos, self.player.pos, self.data['maps'][self.level].hMap)
			if nPos != None:
				self.pos = nPos


class Enemy(Bot):
	def attack(self):
		if self.alive is True:
			print "\n", self.data['atkmsg']
			self.player.attacked(self)
			raw_input()

class Passive(Bot):
	def move(self):
		pass
	
	def attack(self):
		pass

class NPC(Bot):
	pass
