


class Item():
	def __init__(self, iid, data={}):
		self.name = ""
		self.id = iid
		self.data = data
		self.used = False
		self.pickedup = False
		self.weapon = False
		self.type = None

	def init(self):
		def fists(self):
			self.name = "Fists"
			self.damage = .5
			self.hist = 1000
			self.weapon = True
			self.xp = 10

		def woodSword(self):
			self.name = "Wood Sword"
			self.damage = 1
			self.hits = 30
			self.weapon = True
			self.xp = 5

		def ironSword(self):
			self.name = "Iron Sword"
			self.damage = 2
			self.hits = 50
			self.weapon = True
			self.xp = 5
		
		def fireSword(self):
			self.name = "Fire Sword"
			self.damage = 3
			self.hits = 100
			self.weapon = True
			self.xp = 8
		
		def key(self):
			if self.id == 4:
				self.name = "Small Key"
			elif self.id == 4.1:
				self.name = "Big Key"
			elif self.id == 4.2:
				self.name = "Boss Key"

		types = {
			0:fists,
			1:woodSword,
			2:ironSword,
			3:fireSword,
			4:key, #SMALL
			4.1:key, #BIG
			4.2:key #BOSS
		}
		types[self.id](self)
		self.pickedup = True
