"""
Tic Tac Toe Player
"""
import random
import math
from itertools import chain
import copy
from collections import Counter

X = "X"
O = "O"
EMPTY = None
max_depth = 10000


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
    def count_filled_cells(player):
        return sum(1 for cell in chain(*board) if cell == player)
    x_count = count_filled_cells(player=X)
    o_count = count_filled_cells(player=O)
    
    if x_count > o_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_list = set()
    for row_idx, row in enumerate(board):
        for cell_idx, cell in enumerate(row):
            if cell == EMPTY:
                actions_list.add((row_idx, cell_idx))

    return actions_list


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    cell_to_change = board_copy[action[0]][action[1]]

    if cell_to_change != EMPTY:
        raise Exception('Cannot fill this cell')

    board_copy[action[0]][action[1]] = player(board)

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for player in [X, O]:
        for i in range(3):
            if all(board[i][j] == player for j in range(3)):
                return player
            if all(board[j][i] == player for j in range(3)):
                return player

        if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
            return player

    return None  


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    has_empty_cells = len(actions(board))
    if winner(board) or not has_empty_cells:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def min_value(board, best_action, additional):
    if terminal(board) or additional['depth'] >= max_depth:
        return (utility(board), best_action)
    v = float('inf')
    additional['depth'] += 1
    
    for action in actions(board):
        if best_action is None:
            best_action = action
        new_v = min(v, max_value(result(board, action), best_action, additional)[0])
        if new_v < v:
            best_action = action
            v = new_v
    return (v, best_action)

def max_value(board, best_action, additional):
    if terminal(board) or additional['depth'] >= max_depth:
        return (utility(board), best_action)
    v = float('-inf')
    additional['depth'] += 1
    
    for action in actions(board):
        if best_action is None:
            best_action = action
        new_v = max(v, min_value(result(board, action), best_action, additional)[0])
        if new_v > v:
            best_action = action
            v = new_v
    return (v, best_action)

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    current_player = player(board)

    if all(cells == [EMPTY, EMPTY, EMPTY] for cells in board):
        allowed_actions = actions(board)
        return list(allowed_actions)[random.randint(0, len(allowed_actions) - 1)]
    
    if current_player == X:
        return max_value(board, best_action=None, additional={ 'depth': 1 })[1]
    else:
        return min_value(board, best_action=None, additional={ 'depth': 1 })[1]
