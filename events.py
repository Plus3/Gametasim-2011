
class Event():
	def __init__(self, pos, type, data, once):
		self.pos = pos
		self.type = type
		self.data = data
		self.once = once
		self.fired = False