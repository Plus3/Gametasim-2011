
itemz = {
	0:{'xp':10},
	1:{'xp':5},
	2:{'xp':5},
	3:{'xp':8}
}

class Item():
	def __init__(self, iid, data={}):
		self.name = ""
		self.id = iid
		self.data = data
		self.used = False
		self.pickedup = False
		self.type = None
		self.useable = False

		#Weapon vars
		self.weapon = False

		#Light vars
		self.light = False
		self.on = False

		#Food
		self.healAmount = 0
		self.healMsg = None
		self.isFood = False

	def init(self):
		def fists(self):
			self.id = 0
			self.name = "Fists"
			self.damage = .5
			self.hist = 1000
			self.weapon = True
			self.xp = 10

		def woodSword(self):
			self.id = 1
			self.name = "Wood Sword"
			self.damage = 1
			self.hits = 30
			self.weapon = True
			self.xp = 5

		def ironSword(self):
			self.id = 2
			self.name = "Iron Sword"
			self.damage = 2
			self.hits = 50
			self.weapon = True
			self.xp = 5
		
		def fireSword(self):
			self.id = 3
			self.name = "Fire Sword"
			self.damage = 5
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

		def light(self):
			self.id = 5
			self.name = "Unknown Light!"
			self.light = True
			self.on = False
		
		def torch(self):
			self.id = 5.1
			self.name = "Torch"
			self.light = True
			self.on = False
			self.useable = True
			
		def food(self):
			self.isFood = True
			if self.id == 6: pass
			elif self.id == 6.1:
				self.name = "Apple"
				self.healAmount = 5
				self.healMsg = "Om nom nom... juicy apple!"
				self.useable = True
			elif self.id == 6.2:
				self.name = "Orange"
				self.healAmount = 10
				self.healMsg = "Mmmmm... Orange."
				self.useable = True
			elif self.id == 6.3: 
				self.name = "Cookie"
				self.healAmount = 25
				self.healMsg = "Tis a cookie!"
				self.useable = True
			else: pass

		types = {
			0:fists,
			1:woodSword,
			2:ironSword,
			3:fireSword,
			4:key, #SMALL
			4.1:key, #BIG
			4.2:key, #BOSS
			5:light,
			5.1:torch,
			6:food,
			6.1:food, #apple
			6.2:food, #orange
			6.3:food #cookie
		}
		types[self.id](self)
		self.pickedup = True
