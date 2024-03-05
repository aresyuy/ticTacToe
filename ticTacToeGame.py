"""
starting point for tic-tac-toe
"""

#setting up the board
#simply a means of creating the board
def initialize_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)

#player input
#need a function to allow players to input their moves and also check if the position is valid
#>can't go off the map
#>the two conditions are one in the same
def player_move(board, player):
    while True:
        try:
            row = int(input(f"Player {player}, enter your row (1-3): ")) - 1
            col = int(input(f"Player {player}, enter your column (1-3): ")) - 1
            if board[row][col] == " ":
                board[row][col] = player
                break
            else:
                print("This position is already taken. Please choose another.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter numbers from 1 to 3.")

#checking for a win or tie
#check if a player has won or if it's a tie
def check_win(board, player):
    """
    win_conditions = [
            [board[0][0], board[0][1], board[0][2]],
            [board[1][0], board[1][1], board[1][2]],
            [board[2][0], board[2][1], board[2][2]],
            [board[0][0], board[1][0], board[2][0]],
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]],
            [board[0][0], board[1][1], board[2][2]],
            [board[2][0], board[1][1], board[0][2]],
    ]
    return [player, player, player] in win_conditions
    """
    #check for rows
    for row in board:
        if all([cell == player for cell in row]):
            return True
    #check for columns
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    #check for diagnols
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
        return True

    return False

def check_tie(board):
    return all(cell != " " for row in board for cell in row)

#switching between players
#need a way to alternate between players because once it's player 1's turn it has to be player 2's turn and then back until the game is complete
def switch_player(player):
    return "X" if player == "0" else "0" 

#main game loop
#combine all the parts into a main game loop that keeps running until the game is complete -- win or tie
def main():
    play_again = 'y'
    while play_again.lower() == 'y':
        board = initialize_board()
        current_player = "X"
        game_over = False

        while not game_over:
            print_board(board)
            player_move(board, current_player)
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins")
                game_over = True
            elif check_tie(board):
                print_board(board)
                print("It's a tie!")
                game_over = True
            else:
                current_player = switch_player(current_player)

        play_again = input("Do you want to play again? (y/n): ")

#implement an evaluation function basing it off the minimax function
def evaluate(board):
    #check for ai win
    if check_win(board, "O"): #assuming ai uses o
        return 1
    #check for human win
    elif check_win(board, "Human"): #assuming player uses x
        return -1
    #no win
    else:
        return 0

#implement the minimax function
def minimax(board, depth, isMaximizingPlayer):
    score = evaluate(board)

    if score == 1:
        return score
    if score == -1:
        return score
    if check_tie(board):
        return 0

    if isMaximizingPlayer:
        bestScore = -float('inf')
        for row in range(3):
            for col in range(3):
                #is the spot available?
                if board[row][col] == " ":
                    board[row][col] = "O" #ai makes its move
                    score = minimax(board, depth + 1, False)
                    board[row][col] = " " #undo the move
                    bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "X" #human's move is simulated here
                    score = minimax(board, depth + 1, True)
                    board[row][col] = " " #undo the move
                    bestScore = min(score, bestScore)
        return bestScore

#find the best move for ai
def find_best_move(board):
    bestScore = -float('inf')
    move = (-1, -1)
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = "O" #assuming ai is "O"
                score = minimax(board, O, False)
                board[row][col] = " " #undo the move
                if score > bestScore:
                    bestScore = score
                    move = (row, col)
    
    return move

current_player = "X" #assume human starts
game_over = False # initialize the game_over variable

while not game_over:
    print_board(board)
    if current_player == "X":
        player_move(board, current_player) #human's turn
    else:
        row, col = find_best_move(board) #ai's turn
        board[row][col] = "O"
        print(f"AI placed an 'O' in position {row}, {col}")

    #check for a win
    if check_win(board, current_player):
        game_over = True
        print_board(board) #display the final board state
        print(f"{current_player} wins the game!")

    #check for a tie
    elif check_time(board):
        game_over = True
        print_board(board) #display the final board state
        print("The game is a tie!")

    #switch players
    current_player = "O" if current_player == "X" else "X"

#after the loop, ask if one wants to play again
replay = input("Game over. Do you want to play again? (yes/no): ").lower()
if replay in ["yes", "y"]:
    #reset the game to its initial state
    board = initialize_board() #makes ure this function is defined to reset the game
    current_player = "X"
    game_over = False
else:
    print("Thank you for playing!")


if __name__ == "__main__":
    main()
