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
		print self.cMap
		for y in self.cMap:
			print ""
			for x in self.cMap[y]:
				if [x,y] == self.player.pos:
					print "X",
				else:
					print self.Map[y][x-1],

def clean(inp, new={}, _y=0, _x=0):
	for i in inp:
		_y += 1
		_x = -1
		app = []
		for n in inp[i]:
			_x += 1
			app.append(_x)
		new[_y] = app
	return new

def hitMap(Map, dic={}, _y=0, _x=0):
	for y in Map:
		_x = 0
		_y += 1
		for x in Map[y]:
			_x += 1
			if x == "#":
				dic[(_x,_y)] = ["#", 0, 'wall']
			elif x == " ":
				dic[(_x,_y)] = ["#", 1, '']
			else:
				pass
	return dic

def renderMap(Map, pos=[1,1]):
	for y in Map:
		print ""
		for x in Map[y]:
			if [x,y] == pos:
				print "X",
			else:
				print reqs.testlevel[y][x-1],

def load(ID, Mapy, player, Eventz):
	cMap = clean(Mapy)
	hMap = hitMap(Mapy)
	eves = {}
	x = 0
	return Map(ID, Mapy, cMap, hMap, player, Eventz)


# hmap = hitMap(reqs.testlevel)
# mapy = clean(reqs.testlevel)
# posys = [[2,3],[3,3],[4,3],[4,4],[5,4]]
