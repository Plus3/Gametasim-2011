
def getPoss(x,y):
	li = []

	li.append((x-1,y))
	li.append((x+1,y))
	li.append((x,y-1))
	li.append((x,y+2))

	return li
