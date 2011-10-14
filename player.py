import utils, items

class Player():
	def __init__(self, name, pos, level, lvlid, data={}):
		self.name = name #The player name
		self.pos = pos #The player postion (should always be list)
		self.level = level.e #The current level [@DEV do we still need this?]
		self.lvlid = lvlid #The current level ID
		self.xp = 0 #XP Amount
		self.money = [0,50] #Money (and max amount)
		self.data = data #Data dump!
		self.health = [50,50] #Health/max health
		self.lastPos = [] #Last position
		self.inv = { 
			1:None,
			2:None,
			3:None,
			4:None,
			5:None,
			6:None,
			7:None,
			8:None,
			9:None,
			10:None
		}
		
	def hitCheck(self, point, inb={}):
		'''@returns FALSE if point is non-passable, TRUE if passable'''
		r = True
		if type(point) is list:
			point = tuple(point)
		for item in self.level.hMap:
			if item == point and self.level.hMap[item][1] == 0:
				r = False
		for item in inb:
			try:
				if self.level.hMap[item][1] == 0: r = False
			except: pass
		return r

	def move(self, x=0, y=0):
		newPos = [self.pos[0]+x, self.pos[1]+y]
		pwa = utils.pB(self.pos, newPos)
		go = self.hitCheck(newPos, pwa)
		if go == True:
			self.lastPos = self.pos
			self.pos = newPos

	def setPos(self, pos):
		if type(pos) is list:
			self.lastPos = self.pos
			self.pos = pos
	
	def pickupItem(self, iid, notify=True, slot=None):
		for i in self.inv:
			if self.inv[i] == None:				
				self.inv[i] = items.Item(iid)
				self.inv[i].init()
				slot = i
				break
			elif self.inv[i].id == iid:
				notify = False
				break

		if notify is True:
			print "You picked up a", self.inv[slot].name, "it's been stored in Slot #"+str(slot)
			x = raw_input("[OK]")
	
	def use(self, slot, weapon=True):
		if self.inv[slot].weapon == weapon:
			if self.inv[slot].hits > 0:
				self.inv[slot].hits -= 1
				damage = (1,self.inv[slot].damage)
			else: damage = (0,0)
		return damage

	def moneyAdd(self, amount):
		new = self.money[0] + amount
		if new > self.money[1]: self.money[0] = self.money[1]
		else: self.money[0] = new

	def looseHealth(self, amount): self.health[0] -= int(amount)
	
	def attacked(self, bot):
		self.health[0] -= bot.data['attack']
		for i in self.inv:
			if self.inv[i] != None:
				if self.inv[i].weapon == True:
					print "You attack back!!"
					bot.health[0] -= self.inv[i].damage
					self.inv[i].hits -= 1
	
	def eat(self, item): 
		if item.isFood is True:
			self.health[0] += item.heal
			raw_input(item.healMsg)
		else:
			print "You cant eat that!"

