import reqs

class Map():
	def __init__(self, ID, Map, hit, player, events, bots, data={}):
		self.id = ID
		self.Map = Map
		self.hMap = hit
		self.data = data
		self.player = player
		self.events = events
		self.bots = bots

	def render(self):
		_y = 0
		for y in self.Map:
			_y += 1
			_x = 0
			print " "
			for x in self.Map[_y]:
				_x += 1
				if [_x,_y] == self.player.pos:
					print "X",
				elif self.data['BOTS'] != {}: 
					for m in self.bots.e:
						if self.bots.e[m].level == self.id and self.bots.e[m].pos == [_x, _y] and self.bots.e[m].pr is True and self.bots.e[m].alive is True:
							print self.bots.e[m].data['char'],
						else:
							print self.Map[_y][_x-1],
				else:
					print self.Map[_y][_x-1],

def hitMap(Mapz, dic={}, _y=0, _x=0):
	for y in Mapz:
		_x = 0
		_y += 1
		for x in Mapz[y]:
			_x += 1
			if x == "#":
				dic[(_x,_y)] = ["#", 0, 'wall']
			elif x == " ":
				dic[(_x,_y)] = [" ", 1, '']
			elif x == "-":
				dic[(_x,_y)] = ['-', 1, 'door']
			elif x == "@":
				dic[(_x,_y)] = ['@', 1, 'portal']
			else:
				pass
	return dic
