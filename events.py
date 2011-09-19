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
			self.data['player'].pickupItem(self.data['item'])
		elif self.type == "changemap":
			self.data['setter'](self.data['map'], pos=self.data['pos'])
		elif self.type == "door":
			p = self.data['player']
			im = None
			go = False
			for i in p.inv:
				if p.inv[i] == None:
					pass
				elif p.inv[i].id == self.data['req']:
					im = i
					go = True

			if go is True:
				raw_input(self.data['msg2'])
				p.inv[im] = None
				self.once = True
				if self.data['changeChar'][0] is True:
					self.data['setChar'](self.data['changeChar'][2], self.pos, self.data['changeChar'][1])
			else:	
				p.pos = p.lastPos
				raw_input(self.data['msg'])
			
			

	def fire(self):
		if self.once is True:
			if self.fired is False:
				self.go()
		elif self.once is False:
			self.go()
		else:
			pass
	