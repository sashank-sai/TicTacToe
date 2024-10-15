import tkinter as tk
from tkinter import messagebox


player, opponent = 'x', 'o'

def isMovesLeft(board):
    for row in board:
        if '_' in row:
            return True
    return False

def evaluate(board):

    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != '_':
            if board[row][0] == player:
                return 10
            elif board[row][0] == opponent:
                return -10

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '_':
            if board[0][col] == player:
                return 10
            elif board[0][col] == opponent:
                return -10

    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '_':
        if board[0][0] == player:
            return 10
        elif board[0][0] == opponent:
            return -10

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '_':
        if board[0][2] == player:
            return 10
        elif board[0][2] == opponent:
            return -10

    
    return 0


def minimax(board, depth, isMax):
    score = evaluate(board)

    if score == 10:
        return score


    if score == -10:
        return score

    if not isMovesLeft(board):
        return 0

    if isMax:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = player
                    best = max(best, minimax(board, depth + 1, False))
                    board[i][j] = '_'
        return best


    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = opponent
                    best = min(best, minimax(board, depth + 1, True))
                    board[i][j] = '_'
        return best

def findBestMove(board):
    bestVal = -1000
    bestMove = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = player
                moveVal = minimax(board, 0, False)
                board[i][j] = '_'

                if moveVal > bestVal:
                    bestMove = (i, j)
                    bestVal = moveVal

    return bestMove

def player_move(i, j):
    if board[i][j] == '_' and not game_over:
        board[i][j] = opponent
        buttons[i][j].config(text=opponent, state=tk.DISABLED)
        check_game_state()

        if not game_over:
            bestMove = findBestMove(board)
            if bestMove != (-1, -1):
                board[bestMove[0]][bestMove[1]] = player
                buttons[bestMove[0]][bestMove[1]].config(text=player, state=tk.DISABLED)
                check_game_state()


def check_game_state():
    global game_over
    score = evaluate(board)

    if score == 10:
        messagebox.showinfo("Game Over", "AI wins!")
        game_over = True
    elif score == -10:
        messagebox.showinfo("Game Over", "You win!")
        game_over = True
    elif not isMovesLeft(board):
        messagebox.showinfo("Game Over", "It's a tie!")
        game_over = True


def reset_game():
    global board, game_over
    game_over = False
    board = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text='', state=tk.NORMAL)

root = tk.Tk()
root.title("Tic-Tac-Toe")

game_over = False
board = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]


buttons = [[None for _ in range(3)] for _ in range(3)]

for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text='', font=('Arial', 40), width=5, height=2,
                                  command=lambda i=i, j=j: player_move(i, j))
        buttons[i][j].grid(row=i, column=j)

reset_button = tk.Button(root, text='Reset', font=('Arial', 20), command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3)

root.mainloop()
