import random, sys, time, items

itemCheck = lambda item: items.itemz[item]['xp']

def wordy():
	words = ["murdered", "slaughtered", "killed", "slayed", "polished off", "f**ked over", "bopped", "dumped in the river"]
	random.shuffle(words)
	return words[0]

def hitPoint(hit):
	if int(hit) == 1: return "1 hit point"
	else: return "%s hit points" % (hit)

def hit(player, attacker, hit, r=True):
	if r != False:
		attacker.health[0] -= hit
		print "You attacked %s for %s! %s's health: %s/%s" % (attacker.name, hitPoint(hit), attacker.name, attacker.health[0], attacker.health[1])
	player.health[0] -= attacker.data['attack']
	print "%s attacked you for %s!" % (attacker.name, hitPoint(attacker.data['attack']))
	return None
	
def console():
	return raw_input("[VS] => ").split(" ")

def checkHealth(obj):
	if obj.health[0] <= 0:
		return True
	else:
		return False

def Combat(player, attacker, mode, data):
	meDead = checkHealth(player)
	youDead = checkHealth(attacker)
	item = None
	
	while meDead is not True and youDead is not True:
		todo = console()
		doHit = True
		if todo[0].startswith("use"):
			try:
				_item = int(todo[1])
				if _item == 0:
					print "Using fists!"
					item = 0
				elif player.inv[_item] != None and player.inv[_item].weapon == True:
					print "Using "+player.inv[_item].name
					item = _item
				else:
					print "Unknown Item"
			except Exception, e:
				print "Unknown Item"
		elif todo[0].startswith('inv'):
			hitr = False
			data['printInv'](player)
		elif todo[0].startswith("a"):
			if item is None:
				print "You must select an item to use! If you don't have a sword try 'use 0'"
			else:
				if item == 0:
					hit(player, attacker, .5)
				else:
					use = player.use(item)
					if use[0] == 1 and doHit != False:
						hit(player, attacker, use[1])
					else:
						print "The weapon is broken!"
						hit(player, attacker, 0, False)
						item=none
		elif todo[0].startswith('exit'):
			if mode == "offense":
				print attacker.name, "runs away!"
				data['delBot'](attacker.name)
				break
			elif mode == "defense":
				print "You try to run away...",
				x = random.randint(1,5)
				if x == 5:
					print "You got away from",attacker.name+"!"
					data['delBot'](attacker.name)
					break
				else:
					print "Nice try!"
					hit(player, attacker, 0, False)
		else:
			print "Unknown command!"
		
		meDead = checkHealth(player)
		youDead = checkHealth(attacker)

	if meDead is True:
		print "%s %s you!" %(attacker.name, wordy())
		sys.exit()
	elif youDead is True:
		if mode == "defense":
			xpp1 = 5+itemCheck(item)
			xpp = xpp1*attacker.data['level']
		elif mode == "offense":
			xpp1 = 3+itemCheck(item)
			xpp = xpp1*attacker.data['level']
		player.xp += xpp
		print "You %s %s gaining %s XP!" % (wordy(), attacker.name, xpp)
		x = random.randint(2,10)
		print "You loot %s and find %s gold coins" % (attacker.name, x)
		player.moneyAdd(x)
		data['delBot'](attacker.name)
	raw_input("[Exit]")

def battle(player, attacker, Map, attacked=True, data={}):
	data["cls"]()
	if attacked is True:
		print "\n"+attacker.name, "initated a battle!"
		Combat(player,attacker,"defense",data)
	else:
		print "\nAttacking", attacker.name
		Offense(player,attacker,"offense",data)


