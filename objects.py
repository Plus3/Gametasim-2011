
class Object():
	def __init__(self, name, kind, actions, data):
		self.name = name
		self.kind = kind
		self.actions = actions
		self.data = data
	
	def fire(self): pass