#defining playing  board as a matrix

import numpy as np
board = np.empty([6,8], dtype=str)

#creating clear tictactoe board using ASCII characters

def clear_board():
	for i in range(1,7):
		for j in range(1,9):
			if (i == 2 or i == 4) and j%3 !=0:
				board[i-1][j-1] = '_'
			elif j%3 == 0:
				board[i-1][j-1] = '|'
			else:
				board[i-1][j-1] = ' '

#defining function displaying board

def board_disp():
	print("\n".join(" ".join(str(el) for el in row) for row in board))
	print('\n')

#prompting user to choose box and placing user number in box



while True:
	decide = input("Want to play some tictactoe?\n")
	if decide == 'no':
		continue
	elif decide == 'yes':
		count = 0
		taken = []
		marker =['X','O']
		breaker = 0
		clear_board()
		while True:
			board_disp()
			num = int(input("Player with " + str(marker[count%2]) + " please enter box number\n"))
			if num>9 or num<1:
				print('Choose a number between 1 and 9:\n')
				continue
			elif num in taken:
				print('Box already taken, choose another one\n')
				continue
			else:

				if num%3 == 0:
					b = 7
				elif (num+1)%3 == 0:
					b = 4
				elif (num-1)%3 == 0:
					b = 1
				if num in range(1,4):
					a = 0
				elif num in range(4,7):
					a = 2
				elif num in range(7,10):
					a = 4
				board[a][b] = marker[count%2]
				taken.append(num)	
		
	# Defining game outcome conditions
	
	# Checking for like rows
	
			for a in range(0,5,2):
				if board[a][1] == board[a][4] == board[a][7] != ' ' :
					print("Congratulations! Player with  " + str(board[a][1]) + " wins!\n")
					breaker = 1
	
	#Checking for like columns

			for b in range(1,8,3):
				if board[0][b] == board[2][b] == board[4][b] != ' ' :
					print("Congratulations! Player with " + str(board[0][b]) + " wins!\n")
					breaker = 1
									
	#Checking for like diagonals

			if board[0][1] == board[2][4] == board[4][7] != ' ' or board[0][7] == board[2][4] == board[4][1] != ' ' :
				print("Congratulations! Player with " +  str(board[2][4]) + " wins!\n")
				breaker = 1

	#Breaking out of while if win occurs

			if breaker:
				break
			elif count >= 8:
				print("It's a tie!\n")
				break
			
	#incrementing 
				
			count += 1
			print('\n')

	#displaying board at end of game

		board_disp()
	else:
		print("Invalid input\n ")
		continue
		



