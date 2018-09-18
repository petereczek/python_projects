#Defining card components to generate deck from

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight': 8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

#importing random function for shuffling the deck

import random 

#Creating the Card class

class Card:
	
	def __init__(self,suit,rank,value):
		self.suit = suit
		self.rank = rank
		self.value = value

	def __str__():
		
		return rank+'of'+suit

#Creating Deck Class

class Deck:
	
	def __init__(self):
		self.deck = []
		for suit in suits:
			for rank in ranks:
				self.deck.append([rank, suit])
	def shuffle(self):
		random.shuffle(self.deck)

	def __str__(self):
		print('\n',self.deck,'\n')

	def deal(self):
		p = self.deck.pop(0)
	#	print('\n'+'p is '+str(p)+'\n')
	#	print('\n',self.deck,'\n')
	#	print('\n deckdeal worked\n')
		return p


#Creating Hand class


class Hand:
	
	def __init__(self):
		self.cards = []		
		self.numvalues = []
		self.cardvals = []
		self.value = 0
		self.aces = 0		

	def add_card(self,card):
		self.cards.append(card)
		self.cardvals = [item[0] for item in self.cards]
		self.numvalues = [values[i] for i in self.cardvals]
		self.value = sum(self.numvalues)

	def adjust_for_ace(self):
		for card in self.cardvals:
			if card == 'Ace' and self.value > 21:
				self.value -= 10
#		print('\nAdjust for ace worked.\n\n')	
		
	def __str__(self):
		print('\nSum:\n')
		print(self.cardvals,self.numvalues,self.value)		
		

#Creating a Chips class to track player's winnings, bets, balance


class Chips:
	def __init__(self,total,bethowmuch):	
		self.total = total
		self.bethowmuch = bethowmuch

	def win_bet(self):
		self.total += self.bethowmuch

	def lose_bet(self):
		self.total -= self.bethowmuch


def take_bet(playerchips):
	while True:
		try:	
			playerchips.bethowmuch = int(input("\nHow many chips would you like to bet on?\n\n"))
			break
		
		except:
			print("\nInput a natural number of chips to input:\n\n")
			continue

def hit(player,newdeck):
	player.add_card(newdeck.deal())
#print(player.cards)
	player.adjust_for_ace()
#print('hit worked')

def hit_or_stand(player,newdeck):
	while True:

		try:
			if input("\nHit ('h') or Stand ('s')?\n\n") == 'h':
				hit(player,newdeck)
#print('hitorstand worked')
				return 1 
			else: 
				return 0
				break
		except:
			print("Invalid input. Enter Hit('h') or Stand('s'):\n")
			continue

def initial_hit(player,dealer,newdeck):
	print("Dealing initial cards: \n")
	hit(player,newdeck)
	hit(player,newdeck)
	hit(dealer,newdeck)
	hit(dealer,newdeck)

def show_some(player,dealer):
	print("\nThe player's cards: \n")#+', '.join(player.cards))
	print(player.cards,'\n')
	print("\nThe dealer's cards: \n")#+ 'X' + ', '.join(dealer.cards[1:]))
	print('XXXXXXXXXXXXXX',dealer.cards[1:],'\n')

def show_all(player, dealer):

	print("\nThe player's cards: \n")#+', '.join(player.cards))
	print(player.cards,'\n')
	print("\nThe dealer's cards: \n")#+', '.join(dealer.cards))
	print(dealer.cards,'\n')

def player_busts():

	print("\nPlayer busted! Dealer wins!\n")
	PlayerChips.lose_bet()

def player_wins():

	print("\nPlayer wins! Dealer loses!\n")
	PlayerChips.win_bet()

def dealer_busts():

	print("\nDealer busts! Player wins!\n")
	PlayerChips.win_bet()

def dealer_wins():

	print("\nDealer wins! Player loses!\n")
	PlayerChips.lose_bet()

def push():

	print("\nIt's a tie! \n")
	


PlayerChips = Chips(int(input("\nWelcome to Blackjack! How many chips would you like to buy?\n\n")),0)

while True:
	breaker = 0 
	game = 1
	Player = Hand()
	Dealer = Hand()
	NewDeck = Deck()
	NewDeck.shuffle()
	take_bet(PlayerChips)
	initial_hit(Player,Dealer,NewDeck)		
	show_some(Player,Dealer)
	while game == 1:
#		Player.__str__()
		game = hit_or_stand(Player,NewDeck)
		show_some(Player, Dealer)
		if Player.value > 21:
			
			player_busts()
			show_all(Player, Dealer)
			breaker = 1
			break
			

	if breaker == 1:
		pass
	else:
		while Dealer.value < 17:
	
			hit(Dealer,NewDeck)
			if Dealer.value >21:
				
				dealer_busts()
				show_all(Player, Dealer)
				breaker = 1
				break
	
	if breaker == 1:
		pass

	else:
		if 21 - Player.value < 21 - Dealer.value :
			
			player_wins()
			show_all(Player,Dealer)
			
		elif abs(Player.value - 21)> abs(Dealer.value -21):
			dealer_wins()
			show_all(Player, Dealer)

		else:
			
			push()
			show_all(Player, Dealer)
	print('\nPlayer total chips equal: ', PlayerChips.total)
	if input("\nPlay again? ('yes/no')\n") == 'yes' :
		continue
	else:
		break
