def genPossibles(point, dia=False):
	x = point[0]
	y = point[1]
	li = []
	li.append((x-1,y))
	li.append((x+1,y))
	li.append((x,y-1))
	li.append((x,y+2))
	if dia is True:
		li.append((x+1,y+1))
		li.append((x+1,y-1))
		li.append((x-1,y+1))
		li.append((x-1,y-1))
	return li

def ai(me,you,Map, hMap):
	x1 = me[0]
	y1 = me[1]

	x2 = you[0]
	y2 = you[1]

	list1 = genPossibles(me)
	list2 = genPossibles(you)
	#print list1
	#print list2

	f = []
	z = []
	fin = []

	for i in list1:
		for y in list2:
			if sum(i)<sum(y):
				a = y[0]-i[0]
				b = y[1]-i[1]
			else:
				a = i[0]-y[0]
				b = i[1]-y[1]
			f.append((a+b,(i[0],i[1])))
			z.append(a+b)
	f = list(set(f))
	#print Map
	for i in f:
		if i[1] not in hMap:
			if i[1][1] in Map.keys():
				if i[1][0] in Map[i[1][1]]:
					fin.append(i)
	return min(fin)

