import utils
import random
from math import *

def meistehai(me, you, Map):
	mePos = getPoss(me)
	youPos = getPoss(you)
	final = {}

	for i in mePos:
		final[dist(i, you)] = i
	
	y = min(final.keys())
	return final[y]

def getPoss(point):
	li = []

	x = point[0]
	y = point[1]

	li.append((x-1,y))
	li.append((x+1,y))
	li.append((x,y-1))
	li.append((x,y+1))

	return li

def sub(a,b):
	if sum(a) > sum(b):
		return sum(a)-sum(b)
	elif sum(a) < sum(b):
		return sum(b) - sum(a)

def dist(a,b):
	#print sum(a)
	#print sum(b)
	if sum(a) < sum(b):
		rm = b[0]-a[0]
		rz = b[1]-a[1]
	elif sum(a) > sum(b):
		rm = a[0]-b[0]
		rz = a[1]-b[1]
	else:
		rm = 0
		rz = 0
	#print rm,rz
	r1 = rm^2
	r2 = rz^2
	rx = r1+r2
	#print rx
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

def temp(myPos, Map, Player):
	l = getPoss(myPos)
	random.shuffle(l)
	for i in l:
		if list(i) == Player.pos:
			break
		try:
			if Map.hMap[i][1] == 1:
				return i
		except:
			pass
	
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
			nPos = ai(self.pos, self.player.pos, self.data['maps'][self.level])
			nPos2 = meistehai(self.pos, self.player.pos, None)
			if nPos != None:
				self.pos = list(nPos)

class Enemy(Bot):
	def attack(self):
		if self.alive is True:
			print ""
			print self.data['atkmsg']
			self.player.attacked(self)
			raw_input()

class Passive(Bot):
	def move(self):
		pass
	
	def attack(self):
		pass

class NPC(Bot):
	pass

class Bunny(Bot):
	def move(self):
		if self.pr is True and self.alive is True:
			nPos = temp(self.pos, self.data['maps'][self.level], self.player)
			nPos2 = meistehai(self.pos, self.player, none)
			if nPos != None:
				self.pos = list(nPos2)
	
	def attack(self):
		pass