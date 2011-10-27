import errors 
itemInfo = {
	-1: {'name':None, 'damage':0, 'hits':0, 'xp':0, 'needxp':0, 'type':None},
	0:  {'name':'Fists', 'damage':.5, 'hits':1000, 'xp':10, 'needxp':0, 'type':'weapon'},
	1:  {'name':'Wood Sword', 'damage':1, 'hits':30, 'xp':5, 'needxp':0, 'type':'weapon'},
	2:  {'name':'Iron Sword', 'damage':2, 'hits':50, 'xp':10, 'needxp':10, 'type':'weapon'},
	3:  {'name':'Fire Sword', 'damage':5, 'hits':100, 'xp':15, 'needxp':50, 'type':'weapon'},
	4:  {'type':'holder'}, #Unused Holder
	4.1: {'name':'Small Key', 'type':'key'},
	4.2: {'name':'Big Key', 'type':'key'},
	4.3: {'name':'Boss Key', 'type':'key'},
	5: {'type':'holder'},
	5.1: {'name':'Torch', 'type':'light', 'usable':True},
	6: {'type':'holder'},
	6.1: {'name':'Apple', 'healamount':5, 'healmsg':"Om nom nom... juicy apple!", 'usable':True, 'type': 'food'},
	6.2: {'name':'Orange', 'healamount':10, 'healmsg':"Eatz teh orange!", 'usable':True, 'type': 'food'},
	6.3: {'name':'Cookie', 'healamount':25, 'healmsg':"COOOOOOKIIIEEEE MOOOONNNSSSSSTTTEEEERRRR", 'usable':True, 'type': 'food'},
	6.4: {'name':'Chicken', 'healamount':20, 'healmsg':"Mmmmmmm.... chicken", 'usable':True, 'type':'food'}

}

def getInfo(iid, field=None):
	if iid == None: return itemInfo[-1][field]
	if field == None: return itemInfo[iid]
	else: return itemInfo[iid][field]

class Item():
	def __init__(self, iid, data={}):
		self.name = ""
		self.id = iid
		self.type = itemInfo[iid]['type']
		self.data = data
		self.used = False
		self.pickedup = False
		self.type = None
		self.useable = False
		self.enabled = True

		#Weapon vars
		self.xp = 0
		self.needxp = 0

		#Light vars
		self.on = False

		#Food
		self.healAmount = 0
		self.healMsg = None

	def init(self):
		def fists(self):
			self.id = 0
			self.name = itemInfo[self.id]['name']
			self.damage = itemInfo[self.id]['damage']
			self.hits = itemInfo[self.id]['hits']
			self.xp = itemInfo[self.id]['xp']
			self.needxp = itemInfo[self.id]['needxp']
			self.type = itemInfo[self.id]['type']

		def woodSword(self):
			self.id = 1
			self.name = itemInfo[self.id]['name']
			self.damage = itemInfo[self.id]['damage']
			self.hits = itemInfo[self.id]['hits']
			self.xp = itemInfo[self.id]['xp']
			self.needxp = itemInfo[self.id]['needxp']
			self.type = itemInfo[self.id]['type']

		def ironSword(self):
			self.id = 2
			self.name = itemInfo[self.id]['name']
			self.damage = itemInfo[self.id]['damage']
			self.hits = itemInfo[self.id]['hits']
			self.xp = itemInfo[self.id]['xp']
			self.needxp = itemInfo[self.id]['needxp']
			self.type = itemInfo[self.id]['type']
		
		def fireSword(self):
			self.id = 3
			self.name = itemInfo[self.id]['name']
			self.damage = itemInfo[self.id]['damage']
			self.hits = itemInfo[self.id]['hits']
			self.xp = itemInfo[self.id]['xp']
			self.needxp = itemInfo[self.id]['needxp']
			self.type = itemInfo[self.id]['type']
		
		def key(self):
			if self.id == 4: raise errors.ItemError("ID# 4 is not used for anything!") 
			else:
				self.name = itemInfo[self.id]['name']
				self.type = itemInfo[self.id]['type']
			
		def light(self): raise errors.ItemError("ID# 5 is not used for anything!")
		
		def torch(self):
			self.id = 5.1
			self.name = itemInfo[self.id]['name']
			self.type = itemInfo[self.id]['type']
			self.on = False
			self.useable = itemInfo[self.id]['usable']
			
		def food(self):
			if self.id == 6: raise errors.ItemError("ID# 6 is not used for anything!")
			else:
				self.name = itemInfo[self.id]['name']
				self.healAmount = itemInfo[self.id]['healamount']
				self.healMsg = itemInfo[self.id]['healmsg']
				self.useable = itemInfo[self.id]['usable']
				self.type = itemInfo[self.id]['type']

		types = {
			0:fists,
			1:woodSword,
			2:ironSword,
			3:fireSword,
			4:key, #Holder
			4.1:key, #SMALL
			4.2:key, #BIG
			4.3:key, #BOSS
			5:light,
			5.1:torch,
			6:food,
			6.1:food, #apple
			6.2:food, #orange
			6.3:food, #cookie
			6.4:food  #chicken
		}
		types[self.id](self)
		self.pickedup = True
		return self
