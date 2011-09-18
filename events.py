import sys, os, reqs

class Event():
	def __init__(self, pos, type, data, once):
		self.pos = pos
		self.type = type
		self.data = data
		self.once = once
		self.fired = False
	
	def go(self):
		self.fired = True
		if self.type == "msg":
			print self.data['msg']
			raw_input("")
		elif self.type == "end":
			print self.data['msg']
			sys.exit()
		elif self.type == "pickup":
			#print ":", self.data['player']
			self.data['player'].pickupItem(self.data['item'])
		elif self.type == "changemap":
			from main import setMap
			self.data['setter'](self.data['map'])
			#self.data["cmap"].e = loadMap(self.data['map'], self.data['e'])

	def fire(self):
		if self.once is True:
			if self.fired is False:
				self.go()
		elif self.once is False:
			self.go()
		else:
			pass
	