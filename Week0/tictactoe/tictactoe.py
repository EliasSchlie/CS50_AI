"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for row in board:
        for field in row:
            if field == X:
                count += 1
            elif field == O:
                count -= 1

    if count > 0:
        return O
    return X



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i, row in enumerate(board):
        for j, field in enumerate(row):
            if field == EMPTY:
                actions.add((i,j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0] not in [0,1,2] or action[1] not in [0,1,2]:
        raise ValueError("Invalid action")
    who = player(board)
    new_board = []
    for i, row in enumerate(board):
        new_board.append([])
        for j, field in enumerate(row):
            if (i,j) == action:
                if field != EMPTY:
                    raise ValueError("Invalid action")
                new_board[i].append(who)
            else:
                new_board[i].append(board[i][j])
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    check = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
    for i, row in enumerate(board):
        check.append(row)
        for j, field in enumerate(row):
            check[j][i] = field
            if i - j == 0:
                check[3][i] = field
    check.append([board[0][2], board[1][1], board[2][0]])

    for row in check:
        if row == [X,X,X]:
            return X
        elif row == [O,O,O]:
            return O
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True

    for row in board:
        if EMPTY in row:
            return False
    return True




def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    return next(board)[1]

def next(board):
    if terminal(board):
        return (utility(board), None)
    
    if player(board) == X:
        best = -2
        for action in actions(board):
            res = result(board, action)
            if (uti := next(res)[0]) > best:
                best = uti
                do = action
    else:
        best = 2
        for action in actions(board):
            res = result(board, action)
            if (uti := next(res)[0]) < best:
                best = uti
                do = action

    return (best, do)