import sys, os, reqs

class Event():
	def __init__(self, pos, kind, data, once):
		self.pos = pos
		self.kind = kind
		self.data = data
		self.once = once
		self.fired = False
		self.types = {
			'msg':self.MSG,
			'end':self.END,
			'pickup':self.PICKUP,
			'changemap':self.CHANGEMAP,
			'door':self.DOOR,
			'xpdoor':self.XPDOOR
		}
	def MSG(self):
		raw_input(self.data['msg'])
	
	def END(self):
		raw_input(self.data['msg'])
		self.data['exit']()
	
	def PICKUP(self):
		self.data['player'].pickupItem(self.data['item'])
	
	def CHANGEMAP(self):
		self.data['setter'](self.data['map'], pos=self.data['pos'])

	def DOOR(self):
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
	
	def XPDOOR(self):
		p = self.data['player']
		if int(p.xp) >= int(self.data['req']):
			raw_input(self.data['msg2'])
			self.once = True
			if self.data['changeChar'][0] is True:
				self.data['setChar'](self.data['changeChar'][2], self.pos, self.data['changeChar'][1])
		else:
			p.pos = p.lastpos
			raw_input(self.data['msg'])

	def go(self):
		self.fired = True
		if self.kind in self.types:
			self.types[self.kind]()
			
	def fire(self):
		if self.once is True:
			if self.fired is False:
				self.go()
		elif self.once is False:
			self.go()
		else:
			pass
	