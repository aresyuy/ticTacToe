"""
title: tictactoe game revamp1
description: main()
author: @ay

notes:
>this game is going to be solely for bots - no human intervention
>alpha-beta pruning is going to tally the most optimal decision for the bot to make
>implementing heuristics:
    >thought process: alpha-beta pruning will basically provide a number based on the future combinations the bot can take to win given the next move
    >heursitics will allow the bot to consider another factor:
        >what if you can achieve a win not by winning but by not losing - blocking the opponent from winning.
        >hypothesis:
            >this may result in a higher percentage of ties
        >functionally:
            >give more weight to certain board configurations
notes_of_notes:
>it's dawning on me that i want to simulate randomness to capture as many permutations i can
>sometimes i'm running into an error and it may be because the bot doesn't have any more valid moves left
>something that i ran into with the pokemon project is rather than seeing all of the iterations, i got a summary-like return..
>>i want to emulate something like this
..

"""
import random

def generate_random_board(): #how would i accomplish this..
    symbols = ["X", "O", " "] #the three different possible outcomes within the set
    board = [[random.choice(symbols) for _ in range(3)] for _ in range(3)]
    return board

def initialize_board(): #this is redundant
    #return [[" " for _ in range(3)] for _ in range(3)]
    return generate_random_board()

def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)

def make_move(board, row, col, player):
    if board[row][col] == " ":
        board[row][col] = player
        return True
    return False

def check_win(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def check_tie(board):
    return all(board[i][j] != " " for i in range(3) for j in range(3))

def minimax(board, depth, is_maximizing, alpha, beta): 
    if check_win(board, "X"):
        return -10 + depth, None
    elif check_win(board, "O"):
        return 10 - depth, None
    elif check_tie(board):
        return 0, None

    if is_maximizing:
        best_score = float("-inf")
        best_move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score, _ = minimax(board, depth + 1, False, alpha, beta) #integrating alpha and beta
                    board[i][j] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break #pruning happens here
        return best_score, best_move
    else:
        best_score = float("inf")
        best_move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score, _ = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = " "
                    if score < best_score:
                        best_score = score
                        best_move = (i, j)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break #pruning ""
        return best_score, best_move

def ai_move(board, player):
    #_, move = minimax(board, 0, True)
    #return move
    # --
    #init alpha and beta
    alpha = float("-inf") #alpha is going to head towards negative infinity
    beta = float("inf") #beta is going to head towards positive infinity

    #calling minimax to get the best move based on the most optimal decision
    best_score, best_move = minimax(board, 0, True, alpha, beta)

    #if no valid move is found, return a default move
    if best_move is None:
        return 0, 0

    #return the best move
    return best_move

#re-configure this to make it so that it simulates the num_games at once rather than per instance
def simulate_games(num_games): #augmenting this so that i don't have to see the game itself even if the components were created earlier
    #num_games = 1000
    player_x_total_wins = 0 #baseline
    player_o_total_wins = 0 #""
    total_ties = 0 #""

    for _ in range(num_games): #loop
        player_x_wins = 0
        player_o_wins = 0
        ties = 0

        board = initialize_board()
        current_player = "X"
        game_over = False

        while not game_over:
            #print_board(board) #removing this to only see the summary
            row, col = ai_move(board, current_player)
            if row is not None and col is not None:
                if board[row][col] == " ":
                    board[row][col] = current_player
                    if check_win(board, current_player):
                        #print_board(board)
                        #print(f"Player {current_player} wins!")
                        #game_over = True <<accounting for this
                        if current_player == "X":
                            player_x_wins += 1
                        else:
                            player_o_wins += 1
                        game_over = True #<<here
                    elif check_tie(board):
                        #print_board(board)
                        #print("It's a tie!")
                        ties += 1
                        game_over = True
                    else:
                        current_player = "O" if current_player == "X" else "X"
                else:
                    #print("Invalid move.")
                    game_over = True
            else:
                #print("No valid moves left.")
                game_over = True
        
        player_x_total_wins += player_x_wins
        player_o_total_wins += player_o_wins
        total_ties += ties

    return player_x_total_wins, player_o_total_wins, total_ties #<<bringing from up top

#loop everything through here
def main():
    num_games = 1000 #number of games to simulate
    #player_x_total_wins = 0
    #player_o_total_wins = 0
    #total_ties = 0

    #simulate multiple games
    player_x_total_wins, player_o_total_wins, total_ties = simulate_games(num_games)

    #for _ in range(num_games):
        #player_x_wins, player_o_wins, ties = simulate_games(1)
        #player_x_total_wins += player_x_wins
        #player_o_total_wins += player_o_wins
        #total_ties += ties

    #calculate win-percentage for player X
    total_games = num_games - total_ties
    player_x_win_percentage = (player_x_total_wins / total_games) * 100
    
    #calculate win_percentage for player O 
    total_games1 = num_games - total_ties
    player_o_win_percentage = (player_o_total_wins / total_games) * 100

    #display sumary
    print("Summary:")
    print(f"Player X wins: {player_x_total_wins}")
    print(f"Player O wins: {player_o_total_wins}")
    print(f"Ties: {total_ties}")
    print(f"Player X win-percentage - ties: {player_x_win_percentage:.2f}%")
    print(f"Player O win-percentage - ties: {player_o_win_percentage:.2f}%")

if __name__ == "__main__":
    main()

