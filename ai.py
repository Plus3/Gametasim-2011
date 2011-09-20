import utils
import random



def getPoss(point):
	li = []

	x = point[0]
	y = point[1]

	li.append((x-1,y))
	li.append((x+1,y))
	li.append((x,y-1))
	li.append((x,y+1))

	return li

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
	def __init__(self, name, player, pos, level, attack=True, data={}):
		self.name = name
		self.pos = pos
		self.level = level
		self.player = player
		self.data = data
		self.atk = attack
	
	def move(self):
		#print "Moveing..."
		#print self.data
		#print self.player
		nPos = temp(self.pos, self.data['maps'][self.level], self.player)
		if nPos != None:
			#print "Not none!"
			self.pos = list(nPos)

class Enemy(Bot):
	def attack(self):
		self.player.health[0] -= self.data['attack']

class NPC(Bot):
	pass
