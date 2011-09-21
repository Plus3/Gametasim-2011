import reqs

class Map():
	def __init__(self, ID, Map, clean, hit, player, events, data={}):
		self.id = ID
		self.Map = Map
		self.cMap = clean
		self.hMap = hit
		self.data = data
		self.player = player
		self.events = events

	def render(self):
		#print "Bot pos:", self.data['BOTS'][(3,3)].pos
		for y in self.cMap:
			print ""
			for x in self.cMap[y]:
				if [x,y] == self.player.pos:
					print "X",
				else:
					for m in self.data['BOTS']:
						if self.data['BOTS'][m].level == self.id:
							if self.data['BOTS'][m].pos == [x,y]:
								if self.data['BOTS'][m].pr is True:
									print self.data['BOTS'][m].data['char'],
								else:
									print self.Map[y][x-1],
							else:
								print self.Map[y][x-1],
						else:
							print self.Map[y][x-1],
				
def clean(inp, new={}, _y=0, _x=0):
	print inp
	for i in inp:
		_y += 1
		_x = 0
		app = []
		for n in inp[i]:
			_x += 1
			app.append(_x)
		new[_y] = app
	print new
	return new

def hitMap(Mapz, dic={}, _y=0, _x=0):
	for y in Mapz:
		_x = 0
		_y += 1
		for x in Mapz[y]:
			_x += 1
			if x == "#":
				dic[(_x,_y)] = ["#", 0, 'wall']
			elif x == " ":
				dic[(_x,_y)] = ["#", 1, '']
			else:
				pass
	print dic
	return dic

def renderMap(Map, pos=[1,1]):
	for y in Map:
		print ""
		for x in Map[y]:
			if [x,y] == pos:
				print "X",
			else:
				print reqs.testlevel[y][x-1],

def loader(Map):
	print "CLEAN:"
	print clean(Map)
	raw_input()
	print "HITMAP:"
	print hitMap(Map)
