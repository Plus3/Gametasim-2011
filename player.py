import utils, items

class Player():
	def __init__(self, name, pos, level, lvlid, data={}):
		self.name = name
		self.pos = pos
		self.level = level.e
		self.lvlid = lvlid
		self.xp = 0
		self.data = data
		self.health = [50,50]
		self.lastPos = []
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
				if self.level.hMap[item][1] == 0:
					r = False
			except:
				pass

		return r

	def move(self, x=0, y=0):
		newPos = [self.pos[0]+x, self.pos[1]+y]
		pwa = utils.pB(self.pos, newPos)
		go = self.hitCheck(newPos, pwa)
		if go == False:
			pass
		elif go == True:
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
			raw_input("[OK]")
	
	def looseHealth(self, amount):
		self.health[0] += int(amount)*int(-1)
	
