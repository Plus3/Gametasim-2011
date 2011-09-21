import random

def fight(player, attacker, mode, data):
	meDead = False
	youDead = False
	citem = None
	if mode == "attack":
		while meDead is not True and youDead is not True:
			if attacker.health[0] <= 0:
				youDead = True
				print attacker.name,"has died!"
				attacker.pr = False
				raw_input("")
				break
			todo = raw_input("[BATTLE]=>")
			xtodo = todo.split(" ")
			if todo.startswith("use"):
				try:
					xitem = int(xtodo[1])
					if player.inv[xitem] != None:
						if player.inv[xitem].weapon is True:
							print "Using "+player.inv[xitem].name
							citem = xitem
						else:
							print "Unknown item!"
				except:
					print "Unknown item!"
			elif todo.startswith("inv"):
				data['printInv']()
			elif todo.startswith("a") or todo.startswith("attack"):
				if citem is None:
					print "You must select an item with use!"
				else:
					d = player.use(citem)
					if d[0] == 0:
						print "The weapon is broken!"
					elif d[0] == 1:
						#print d[1]
						#print attacker.health
						attacker.health[0] -= d[1]
						print "You attacked",attacker.name,"with",player.inv[citem].name,"for",d[1],"hit!"
						print attacker.name,"health:",str(attacker.health[0])+"/"+str(attacker.health[1])
						#raw_input()
			elif todo.startswith("exit"):
				print attacker.name, "ran away!"
				attacker.pr = False
				break

			y = random.randint(1,50)
			if y == 23:
				print attacker.name, "escaped!"
				attacker.pr = False
				raw_input("[exit]")
				break
	#raw_input("hold")
def battle(player, attacker, Map, attacked=True, data={}):
	if attacked is True:
		print "\n"+attacker.name, "initated an battle!"
	else:
		print "\nAttacking", attacker.name
		fight(player,attacker,"attack",data)


