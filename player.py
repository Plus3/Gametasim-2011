class Player():
	def __init__(self, name, pos, level, data):
		self.name = name
		self.pos = pos
		self.level = level
		self.data = data
		self.inv = {}
		self.health = 50

	def move(self, x, y):
		newPos = [self.pos[0]+x, self.pos[1]+x]
		if newPos in self.hMap:
			pass
		else:
			self.pos = newPos
