import utils

class Player():
	def __init__(self, name, pos, level, data={}):
		self.name = name
		self.pos = pos
		self.level = level
		self.data = data
		self.inv = {}
		self.health = 50

	def move(self, x=0, y=0):
		go = True
		newPos = [self.pos[0]+x, self.pos[1]+y]
		pwa = utils.pB(self.pos, newPos)
		#print self.level.hMap
		for i in self.level.hMap:
			if tuple(newPos) == i:
				if self.level.hMap[i][1] == 0:
					go = False
				else:
					go = True
			else:
				pass
		for b in pwa:
			try:
				if self.level.hMap[b][1] == 0:
					go = False
			except:
				pass
		if go == False:
			pass
		elif go == True:
			self.pos = newPos
