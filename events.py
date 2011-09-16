import sys, os

class Event():
	def __init__(self, pos, type, data, once):
		self.pos = pos
		self.type = type
		self.data = data
		self.once = once
		self.fired = False
	
	def go(self):
		if self.type == "msg":
			print self.data['msg']
			raw_input("")
		elif self.type == "end":
			print self.data['msg']
			sys.exit()

	def fire(self):
		if self.once is True and self.fired is False:
			self.go()
		elif self.once is False:
			self.go()
		else:
			pass
	