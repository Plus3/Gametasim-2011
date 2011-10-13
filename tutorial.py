import utils, time

_cls = utils.CLS

def start():
	_cls()
	print "Hi there! Welcome to Gametasim!"
	print "Key:"
	print "# : Wall"
	print ". : Bunny (evil or friendly)"
	print "O : Ogre"
	print "@ : Portal [door]"
	print "X : You!"
	raw_input('')

def animate(ani):
	_cls()
	for x in ani:
		for y in x:
			print y
		time.sleep(.5)
		_cls() 