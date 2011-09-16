
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
		def woodSword(self):
			self.name = "Wood Sword"
			self.damage = 1
			self.hits = 30
			self.weapon = True

		def ironSword(self):
			self.name = "Iron Sword"
			self.damage = 3
			self.hits = 50
			self.weapon = True
		
		def fireSword(self):
			self.name = "Fire Sword"
			self.damage = 5
			self.hits = 100
			self.weapon = True
		
		def key(self):
			if self.id == 4:
				self.name = "Small Key"
			elif self.id == 4.1:
				self.name = "Big Key"
			elif self.id == 4.2:
				self.name = "Boss Key"

		types = {
			1:woodSword,
			2:ironSword,
			3:fireSword,
			4:key, #SMALL
			4.1:key, #BIG
			4.2:key #BOSS
		}
		types[self.id](self)
		self.pickedup = True
