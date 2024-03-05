def initialize_board():
    return [[" " for _ in range(3)] for _ in range(3)]

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

def minimax(board, depth, is_maximizing):
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
                    score, _ = minimax(board, depth + 1, False)
                    board[i][j] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_score, best_move
    else:
        best_score = float("inf")
        best_move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score, _ = minimax(board, depth + 1, True)
                    board[i][j] = " "
                    if score < best_score:
                        best_score = score
                        best_move = (i, j)
        return best_score, best_move

def ai_move(board, player):
    _, move = minimax(board, 0, True)
    return move

def main():
    board = initialize_board()
    current_player = "X"
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
                print("Invalid move.")
        else:
            print("No valid moves left.")
            game_over = True

if __name__ == "__main__":
    main()

