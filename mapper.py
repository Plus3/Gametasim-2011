import reqs

class Map():
	def __init__(self, Map, clean, hit, pos, data={}):
		self.Map = Map
		self.cMap = clean
		self.hMap = hit
		self.data = data
		self.pos = pos
	def render(self):
		for y in self.cMap:
			print ""
			for x in self.cMap[y]:
				if [x,y] == self.pos:
					print "X",
				else:
					print self.Map[y][x-1],

def clean(inp, new={}, _y=0, _x=0):
	for i in inp:
		_y += 1
		_x = 0
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

def load(Mapy, player):
	cMap = clean(Mapy)
	hMap = hitMap(Mapy)
	return Map(Mapy, cMap, hMap, player)


# hmap = hitMap(reqs.testlevel)
# mapy = clean(reqs.testlevel)
# posys = [[2,3],[3,3],[4,3],[4,4],[5,4]]
