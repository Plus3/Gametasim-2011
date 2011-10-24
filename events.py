import sys, os, reqs
import sound, random, items

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
			'xpdoor':self.XPDOOR,
			'chest':self.CHEST,
			'play':self.PLAY,
			'mysterybox':self.MYSTERY,
		}
	def MSG(self): raw_input(self.data['msg'])
	
	def END(self):
		raw_input(self.data['msg'])
		self.data['exit']()
	
	def PICKUP(self): self.data['player'].pickupItem(self.data['item'])
	
	def CHANGEMAP(self): self.data['setter'](self.data['map'], pos=self.data['pos'])

	def DOOR(self):
		p = self.data['player']
		im = None
		go = False
		for i in p.inv:
			if p.inv[i] == None: pass
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
			p.pos = p.lastPos
			raw_input(self.data['msg'])

	def CHEST(self): 
		def chestScreen(self):
			x = 0
			for i in self.data['contains']:
				x += 1
				r = items.Item(i)
				r.init()
				print "[%s] %s" % (x, r.name)
			choice = raw_input("Selection => ")
			if int(choice) > x:
				raw_input("Invalid selection!")
				self.data['player'].goBack()
			else: 
				self.data['player'].pickupItem(r.id, True)
		chestScreen(self)
	
	def PLAY(self):
		if self.data['sound'] in self.data['sounds'].value():
			self.data['sounds'][self.data['sound']].play()

	def MYSTERY(self):
		if random.randint(1,10) != 5:
			random.shuffle(self.data['items'])
			raw_input("You found a %s" % (items.Item(self.data['items'][1]).init().name))
			self.data['player'].pickupItem(self.data['items'][1], False)
		else:
			x = random.randint(1,10)
			self.data['player'].looseHealth(x)
			print "Ouch! The mystery box takes %s health from you!" % (x)
		self.data['player'].goBack()
		self.data['setChar'](self.data['map'], self.pos, " ")

	def go(self):
		self.fired = True
		if self.kind in self.types: self.types[self.kind]()
			
	def fire(self):
		if self.once is True and self.fired is False: self.go()
		elif self.once is False: self.go()
		else: pass
	