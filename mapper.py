import reqs

class Map():
	def __init__(self, ID, Map, hit, player, events, data={}):
		self.id = ID
		self.Map = Map
		self.hMap = hit
		self.data = data
		self.player = player
		self.events = events

	def render(self):
		_y = 0
		for y in self.Map:
			_y += 1
			_x = 0
			print ""
			for x in self.Map[_y]:
				_x += 1
				if [_x,_y] == self.player.pos:
					print "X",
				elif self.data['BOTS'] != {}:
					for m in self.data['BOTS']:
						if self.data['BOTS'][m].level == self.id and self.data['BOTS'][m].pos == [_x,_y] and self.data['BOTS'][m].pr is True:
							print self.data['BOTS'][m].data['char'],
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
