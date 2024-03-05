#!python
#starting over
"""
title: tictactoe
description: main()
author: @a
notes:
what i want from this is a tic-tac-toe environment where a bot can essentially play the game by itself and explore different ml frameworks

"""

import random

#establish the board
def initialize_board():
	return [[" " for _ in range(3)] for _ in range(3)]

#actually print it out
def print_board(board):
	for row in board:
		print("|".join(row))
		print("-" * 5)

#create an ai that makes random moves
def ai_move(board, player):
	empty_cells = [(i,j) for i in range(3) for j in range(3) if board[i][j] == " "]
	return random.choice(empty_cells) if empty_cells else None

#check for a win
def check_win(board, player):
	for i in range(3):
		if all(board[i][j] == player for j in range(3)) or \
			all(board[i][j] == player for j in range(3)):
				return True
	for all(board[i][i] == player for i in range(3)) or \
		all(board[i][2-i] == player for i in range(3)):
			return True
	return False

#check for a tie
def check_tie(board):
	return all(board[i][j] != " "for i in range(3) for j in range(3))

#the game loop
def main():
	#establish the actual board
	board = initialize_board()
	#starting with bot1
	current_player = "X"
	#the game hasn't finished, so by default it'll run until it is complete
	game_over = False

	while not game_over:
		print_board(board)
		row, col = ai_move(board, current_player)
		if row is not None and col is not None:
			if board[row][col] == " ":
				board[row][col] = current_player
					if check_win(board, current_player):
						print_board(board)
						print(f"Player {current_player} wins!")
						game_over = True
					elif check_tie(board):
						print_board(board)
						print("It's a tie!")
						game_over = True
					else:
						current_player = "O" if current_player == "X" else "X"
				else:
					print("Invalid move."
			else:
				print("No valid moves left.")
				game_over = True

if __name__ == "__main__":
	main()
