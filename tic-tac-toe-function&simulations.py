import numpy as np
#record the players' moves
playermove = []

#create board of 3x3 array containing zeros
def create_board():
    board = np.zeros((3,3), dtype = int)
    playermove = [0]
    return board

#place 1 for player 1, 2 for player 2 on the array
def place(board, player, position):
    if board[position] == 0:
        board[position] = player
        return board

#function to show possible moves for the player currently
def possibilities(board):
    possibilities = np.where(board == 0)
    listOfCoordinates= list(zip(possibilities[0], possibilities[1]))
    possiblecoord = []
    for cord in listOfCoordinates:
        possiblecoord.append(cord)
    return possiblecoord

#Teacher's solution
def possibilities_best(board):
    return list(zip(*np.where(board == 0)))

#randomly simulate choices
import random
random.seed(1)
def random_place(board, player):
    move = random.choice(possibilities(board))
    place(board, player, move)
    return board

#check if player n has win for the rows (e.g:111 or 222)
def row_win(board, player):
    for i in board:
        if np.all(i == player):
            return True
    return False

#check if player n has win for the columns
def col_win(board, player):
    board_t = np.transpose(board)
    for i in board_t:
        if np.all(i == player):
            return True
    return False

#check if player has win for the diagonals
def diag_win(board, player):
    i = 0
    win1 = False
    win2 = False
    while i < len(board):
        j = 0
        while j < len(board[i]):
            if j == i:
                if board[i][j] == player:
                    win1 += True
            j += 1
        i += 1
    k = 0
    while k < len(board):
        l = 0
        while l < len(board[k]):
            if l == len(board[k]) - k -1:
                if board[k][l] == player:
                    win2 += True
            l += 1       
        k += 1
    #print(win1)
    #print(win2)
    if win1 == 3 or win2 == 3:
        return True
    else:
        return False

#teacher's solution
def diag_win_best(board, player):
    if np.all(np.diag(board)==player) or np.all(np.diag(np.fliplr(board))==player):
        # np.diag returns the diagonal of the array
        # np.fliplr rearranges columns in reverse order
        return True
    else:
        return False

#teacher's solution
def col_win_best(board, player):
    if np.any(np.all(board==player, axis=0)): # this checks if any column contains all positions equal to player
        return True
    else:
        return False

#teacher's solution
def row_win_best(board, player):
    if np.any(np.all(board==player, axis=1)): # this checks if any row contains all positions equal to player.
        return True
    else:
        return False

#see if any player has won row-ly or column-ly or diagonal-ly
def evaluate(board):
    winner = 0
    for player in [1, 2]:
        if row_win(board, player) or col_win(board, player) or diag_win(board, player):
            winner = player
        # add your code here!
    if np.all(board != 0) and winner == 0:
        winner = -1
    return winner    
    
#simulate game
board = create_board()

#seed the random function if required
random.seed(1)

#1st player move, then 2nd player move
i = 1
while i < 10:
    if(i%2 == 0):
        random_place(board,2)
        print(board)
    else:
        random_place(board,1)
        print(board)
    i += 1

#print the winner, 0 or -1 if no winner    
evaluate(board)
