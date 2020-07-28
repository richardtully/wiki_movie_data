from random import *

def conc_mem_strat(player,cards,revealed):

	def update_memory():
			#print([card.position for card in revealed[-player.memsize:]])
			if player.memsize == 0:
				player.memory = []
			else:
				player.memory = [card for card in revealed[-player.memsize:] if card.status == 'unpicked']

	def lucky_dip(cards):
		return sample([card for card in cards if card not in player.memory and card not in player.picked],1)

	# check_mem looks for pairs in memory (before any cards have been picked)
	def check_mem():
		for card1 in player.memory:
			for card2 in player.memory:
				if card1.code == card2.code and card1.position != card2.position:
					return [card1,card2]
				
		return []		
	
	# compare_mem looks for a single card in memory (after one has already been picked)
	def compare_mem():
		return [card for card in player.memory if card.code == player.picked[0].code and card.position != player.picked[0].position]



	
	update_memory()

	player.picked += check_mem()
	if len(player.picked) == 2:
		return(player.picked)		

	player.picked += lucky_dip(cards)
	player.picked += compare_mem()
	if len(player.picked) == 2:
		return(player.picked)
	player.picked += lucky_dip(cards)
	return(player.picked)