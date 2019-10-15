# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import random
import copy
from collections import deque


class HumanPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        # Let the player type in their move.
        # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
        valid_digits = []
        for i in range(1, board.get_size()+1):
            valid_digits.append(str(i))
        no_valid_move = True
        while no_valid_move:
            move = input(self.symbol + ', enter your move:').lower()
            if len(move) == 2 and move[0] in valid_digits and move[1] in valid_digits:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if board.is_valid_move(self.symbol, ( x, y) ):
                    no_valid_move = False
                    return [x, y]
                else:
                    print('Not a valid move.')
            else:
                print('Bad input. Type valid x digit, then the y digit.')


class RandomComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        return random.choice(board.calc_valid_moves(self.symbol))

class GreedyComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):

        #This is the board used to emulate the board state.
        emuBoard = copy.deepcopy(board);
        max = [0, self.emulateMove(emuBoard, board.calc_valid_moves(self.symbol)[0])]
        for i in range(1, len(board.calc_valid_moves(self.symbol))):
            moveValue = self.emulateMove(emuBoard, board.calc_valid_moves(self.symbol)[i])
            if(self.check_corner(emuBoard, board.calc_valid_moves(self.symbol)[i])):
                moveValue = moveValue * 1.55
            elif(self.check_edge(emuBoard, board.calc_valid_moves(self.symbol)[i])):
                moveValue = moveValue * 1.35

            if moveValue > max[1]:
                max[0] = i;
                max[1] = moveValue;

        return board.calc_valid_moves(self.symbol)[max[0]]

    def check_edge(self, board, move):
        if(move[0] == 0 or move[0] == (board.get_size()-1)):
            return True
        elif((move[1] == 0 or move[1] == (board.get_size()-1))):
            return True
    def check_corner(self, board,move):
        if ((move[0] == 0 or move[0] == (board.get_size() - 1)) and (move[1] == 0 or move[1] == (board.get_size()-1))):
            return True

    def emulateMove(self, board, move):
        board.make_move(self.symbol, move);
        return board.calc_scores()[self.symbol]


class MinimaxComputerPlayer:
    def __init__(self, symbol, depth):
        self.symbol = symbol
        self.cutoff = depth;

    def get_move(self, board):
        emuBoard = copy.deepcopy(board)
        max_val = None
        valid_moves = board.calc_valid_moves(self.symbol)
        for i in range(0, len(valid_moves)):
            cur_eval = self.minimax(emuBoard, self.cutoff, board.get_opponent_symbol(self.symbol), valid_moves[i])
            if max_val is None:
                max_val = [cur_eval, valid_moves[i]]
            elif cur_eval > (max_val[0]):
                max_val = [cur_eval, valid_moves[i]]
        return max_val[1]

    def minimax(self, board, depth, cur_symbol, last_move):
        board.make_move(cur_symbol, last_move)

        if depth == 0 or len(board.calc_valid_moves(cur_symbol)) == 0:
            initVal = board.calc_scores()[cur_symbol]
            if ((last_move[0] == 0 or last_move[0] == (board.get_size() - 1)) and (last_move[1] == 0 or last_move[1] == (board.get_size() - 1))):
                initVal = initVal * 1.55
            elif ((last_move[0] == 0 or last_move[0] == (board.get_size() - 1)) and (last_move[1] == 0 or last_move[1] == (board.get_size() - 1))):
                initVal = initVal * 1.35
            return initVal

        if cur_symbol == self.symbol:
            max_val = None
            for move in board.calc_valid_moves(cur_symbol):
                min_max_val = self.minimax(board, depth - 1, board.get_opponent_symbol(self.symbol), move)
                if max_val is None:
                    max_val = min_max_val
                else:
                    max_val = self.min_max_eval(max_val, min_max_val, "max")
            return max_val
        elif cur_symbol != self.symbol:
            min_val = None
            for move in board.calc_valid_moves(cur_symbol):
                min_max_val = self.minimax(board, depth - 1, self.symbol, move)
                if min_val is None:
                    min_val = min_max_val
                else:
                    min_val = self.min_max_eval(min_val, min_max_val, "min")
            return min_val

    def min_max_eval(self, val1, val2, min_or_max):
        if min_or_max.lower() == "max":
            if(val1 > val2):
                return val1
            else:
                return val2
        elif min_or_max.lower() == "min":
            if (val1 < val2):
                return val1
            else:
                return val2

    def evaulateState(self, board, move):
        board.make_move(self.symbol, move)
        return board.calc_scores()[self.symbol]