import reqs, objects

class Map():
	def __init__(self, ID, Map, hit, player, events, obj, bots, data={}):
		self.id = ID
		self.Map = Map
		self.hMap = hit
		self.data = data
		self.player = player
		self.events = events
		self.bots = bots
		self.obj = obj

		for i in obj:
			obj[i]['obj'] = objects.Object(self.obj[i]['name'], self.obj[i]['pos'], self.obj[i]['kind'], self.obj[i])
			obj[i]['exec'] = obj[i]['obj'].fire

	def render(self):
		mr = {}
		for m in self.bots.value():
			if self.bots[m].level == self.id and self.bots[m].pr is True and self.bots[m].alive is True:
				mr[tuple(self.bots[m].pos)] = self.bots[m].data['char'] 
		_y = 0
		for y in self.Map:
			_y += 1
			_x = 0
			print " "
			for x in self.Map[_y]:
				_x += 1
				if [_x,_y] == self.player.pos: print "X",
				elif (_x,_y) in mr: print mr[(_x,_y)],
				else: print self.Map[_y][_x-1],

def hitMap(Mapz, dic={}, _y=0, _x=0):
	for y in Mapz:
		_x = 0
		_y += 1
		for x in Mapz[y]:
			_x += 1
			if x == "#": dic[(_x,_y)] = ["#", 0, 'wall']
			elif x == " ": dic[(_x,_y)] = [" ", 1, '']
			elif x == "-": dic[(_x,_y)] = ['-', 1, 'door']
			elif x == "@":dic[(_x,_y)] = ['@', 1, 'portal']
	return dic
