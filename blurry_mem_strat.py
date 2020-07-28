from random import *
from random import random

def blurry_mem_strat(player,cards,revealed):

	def blurry_pick(aim_card):
		#print('aim_card: ' + str(aim_card.position))
		x = player.memory.index(aim_card) # the higher the cards index in memory, the more recently it was added to memory
		p = (1/ player.memsize)*x  # probability of picking the card we're aiming for before we random it
		#print('Trying to get the main card with blurry pick')
		random_num = random()
		if random_num > p:
			aim_card.status = 'picked'
			return aim_card
		else:
			#print('')
			#print('Searching nearby cards')
			#print('')
			nearby = [] 
			for card in cards:
				if card.status != 'picked':
					if card not in player.picked:
						if abs(card.position[0]-aim_card.position[0]) < 2:
							if abs(card.position[1]-aim_card.position[1]) < 2:
								nearby.append(card)
			#print([i.position for i in nearby])
			 
			chosen = sample(nearby,1)[0]
			chosen.status = 'picked'
			#print('Chosen: ' + str(chosen.position))
			return chosen




	def update_memory():
			if player.memsize == 0:
				player.memory = []
			else:
				player.memory = [card for card in revealed[-player.memsize:] if card.status == 'unpicked']

	def lucky_dip(cards):
		#print('Doing a lucky_dip')
		chosen = sample([card for card in cards if card not in player.memory and card not in player.picked],1)
		return chosen

	# check_mem looks for pairs in memory (before any cards have been picked)
	def check_mem():
		#print('check_mem')
		for card1 in player.memory[::-1]: # Looking for the pair of cards most recently added to memory
			for card2 in player.memory[::-1]:
				if card1.code == card2.code and card1.position != card2.position:
					return [blurry_pick(card1)]
		#print('check_mem returned nothing')	
		return []		
	
	# compare_mem looks for a single card in memory (after one has already been picked)
	def compare_mem():
		#print('compare_mem')
		for card in player.memory:
			if card.code == player.picked[0].code and card.position != player.picked[0].position:
				#return [card]
				return [blurry_pick(card)]
		#print('compare_mem returned nothing')
		return []

	update_memory()

	player.picked += check_mem()
	if len(player.picked)>0:
		player.picked += compare_mem()
	if len(player.picked) == 2:
		return(player.picked)
	player.picked += lucky_dip(cards)
	if len(player.picked) == 2:
		return(player.picked)
	player.picked += compare_mem()
	if len(player.picked) == 2:
		return(player.picked)
	player.picked += lucky_dip(cards)
	return(player.picked)