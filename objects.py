
#@NOTE Keep these outside or pickle likes to throw errors
def door(self): pass
def chest(self): pass
def test(self): 
	raw_input(self.data['test'])
	self.data['test'] = raw_input("Test is a win!")
	
class Object():
	def __init__(self, name, pos, kind, data):
		self.name = name
		self.kind = kind
		self.pos = pos
		self.data = data
		self.fire = None

		if self.kind in self.kinds: self.fire = self.kinds[self.kind]
		
		def fire(self):
			if self.fire: self.fire(self)	

	kinds = {
		'door':door,
		'chest':chest,
		'test':test
	}