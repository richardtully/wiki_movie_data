''' I want two different scripts to play each other at pairs. I'm going to have to modify what the strategies 
look like at the moment in order to do this.'''
from random import *
import matplotlib.pyplot as plt
import math
from concentrated_memory_strat import conc_mem_strat
from blurry_mem_strat import blurry_mem_strat

width = 30
height = 30
revealed = []
# Classes:
# 1: Card - these are the cards that will played with
class Card:
    def __init__(self, position, code, status):
        self.position = position
        self.code = code
        self.status = status

# 2: Player - these are the players who will play the game
class Player:
	def __init__(self, score, score_record, memsize, name, revealed, pick_strat):
		self.score = score 
		self.score_record = []
		self.memsize = memsize
		self.memory = []
		self.picked = []
		self.name = name
		self.pick_strat = pick_strat

	def pick(self):
		return self.pick_strat(self,cards,revealed)


def create_cards (width,height):
	number_of_cards = width*height
	v = [i for i in range (number_of_cards)] 
	shuffle(v)

	# The cards on the 'board'. 
	cards=[Card((i%width,math.floor(i/height)), str(v.pop(-1)%(number_of_cards/2)), 'unpicked') for i in range(number_of_cards)]
	return(cards)

def check_picked(player, picked):
	global revealed
	#build_board()
	#print('Length of cards: ' + str(len(cards)))
	#print('Picked positions: ' + str([i.position for i in picked]))
	#print('Picked codes: ' + str([i.code for i in picked]))
	if len(picked) == 2: 
		if picked[0].code == picked[1].code:
			for i in picked:		
				cards.remove(i)
				i.status = 'picked'
			player.score += 1
			player.picked = []
			return 'Success'
	# If the cards in picked are not a pair, then the cards must be added to revealed (and 
	# the next player must begin their turn)
	revealed += picked

	#print('Didnt get a pair this time...')
	current_player.picked = []

player1 = Player(0,[0],0, 'player1', revealed, blurry_mem_strat)
player2 = Player(0,[0],5, 'player2', revealed, blurry_mem_strat)
player3 = Player(0,[0],10, 'player3', revealed, blurry_mem_strat)
player4 = Player(0,[0],5, 'player4', revealed, conc_mem_strat)
player5 = Player(0,[0],10, 'player5', revealed, conc_mem_strat)

players = [player1, player2, player3, player4, player5]
cards = create_cards(width, height)
# def build_board(width, height, cards):
# 	a=1
# 	row = [i for i in range(width)]
# 	board = [row for i in range(height)]
# 	for i in cards:
# 		board[i.position[1]][i.position[0]] = str(i.position)
	

def build_board():
	row = ['    ' for i in range(width)]
	board = [row.copy() for i in range(height)]
	for card in cards:
		board[card.position[1]][card.position[0]] = card.position
	for i in board:
		print(i)
	print('')

build_board()



'''

  .g8"""bgd                                          `7MM"""YMM `7MM                              
.dP'     `M                                            MM    `7   MM                              
dM'       `   ,6"Yb.  `7MMpMMMb.pMMMb.   .gP"Ya        MM   d     MM   ,pW"Wq.  `7M'    ,A    `MF'
MM           8)   MM    MM    MM    MM  ,M'   Yb       MM""MM     MM  6W'   `Wb   VA   ,VAA   ,V  
MM.    `7MMF' ,pm9MM    MM    MM    MM  8M""""""       MM   Y     MM  8M     M8    VA ,V  VA ,V   
`Mb.     MM  8M   MM    MM    MM    MM  YM.    ,       MM         MM  YA.   ,A9     VVV    VVV    
  `"bmmmdPY  `Moo9^Yo..JMML  JMML  JMML. `Mbmmd'     .JMML.     .JMML. `Ybmd9'       W      W 

                                                                                                  
'''


# Turn Starts:
n=0
while cards:
	current_player = players[n%len(players)]
	while cards:
		#print('----- Turn begins for: ' + current_player.name + ' -----')
		x = current_player.pick() # Current player picks
		if check_picked(current_player, x) != 'Success': # Check if he picked a pair. If not, it's the next players turn.
			break
	for i in players:
		i.score_record.append(i.score)
	n += 1


f = lambda x: x.name + ':  ' + str(x.score)
for i in players:
	print(f(i))#print(list(map(f,players)))


x = range(len(player1.score_record))
print(x)
for i in players:
	plt.plot(x,i.score_record, label = str(i.name) + ' '+ str(i.pick_strat.__name__))
plt.xlabel('Turn number \n (every players turns contribute to this number)')
plt.ylabel('Score')
plt.legend()
plt.show()