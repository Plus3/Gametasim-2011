import utils, items

class Player():
	def __init__(self, name, pos, level, data={}):
		self.name = name
		self.pos = pos
		self.level = level
		self.data = data
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
		self.health = [50,50]

	def move(self, x=0, y=0):
		go = True
		newPos = [self.pos[0]+x, self.pos[1]+y]
		pwa = utils.pB(self.pos, newPos)
		#print self.level.hMap
		for i in self.level.hMap:
			if tuple(newPos) == i:
				if self.level.hMap[i][1] == 0:
					go = False
				else:
					go = True
			else:
				pass
		for b in pwa:
			try:
				if self.level.hMap[b][1] == 0:
					go = False
			except:
				pass
		if go == False:
			pass
		elif go == True:
			self.pos = newPos

	def setPos(self, pos):
		if pos:
			self.pos = pos
	
	def pickupItem(self, iid, notify=True):
		slot = None
		for i in self.inv:
			if self.inv[i] == None:
				self.inv[i] = items.Item(iid)
				self.inv[i].init()
				slot = i
				break
		if notify is True:
			print "You picked up a", self.inv[slot].name, "it's been stored in Slot #"+str(slot)
			raw_input("[OK]")
		else:
			pass
	
	def looseHealth(self, amount):
		self.health[0] += int(amount)*int(-1)
		