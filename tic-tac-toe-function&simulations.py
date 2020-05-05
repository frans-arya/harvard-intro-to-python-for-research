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
    
#function to play the game 1 time
def play_game():
    board = create_board()
    #1st player move, then 2nd player
    i = 1
    while i < 10:
        if(i%2 == 0):
            random_place(board,2)
            #evaluate if after placement player 2 is the winner
            if evaluate(board) == 2:
                return 2
        else:
            random_place(board,1)
            #evaluate if after placement player 1 is the winner
            if evaluate(board) == 1:
                return 1
        i += 1
    return evaluate(board)

#function to play the game 1 time
def play_strategic_game():
    board = create_board()
    #1st player always place middle of the square first
    board[1,1] = 1
    i = 2
    while i < 10:
        if(i%2 == 0):
            random_place(board,2)
            #evaluate if after placement player 2 is the winner
            if evaluate(board) == 2:
                return 2
        else:
            random_place(board,1)
            #evaluate if after placement player 1 is the winner
            if evaluate(board) == 1:
                return 1
        i += 1
    return evaluate(board)

#teacher's solution
def play_game_alternative():
    board, winner = create_board(), 0
    board[1,1] = 1
    while winner == 0:
        for player in [2,1]:
            random_place(board, player)
            winner = evaluate(board)
            if winner != 0:
                break
    return winner

#teacher's solution
def play_strategic_game_alternative():
    board, winner = create_board(), 0
    board[1,1] = 1
    while winner == 0:
        for player in [2,1]:
            random_place(board, player)
            winner = evaluate(board)
            if winner != 0:
                break
    return winner
