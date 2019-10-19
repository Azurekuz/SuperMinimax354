# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate #Eugene Kuznetsov
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

    def __init__(self, symbol, heuristic):
        self.symbol = symbol
        self.use_heuristic = heuristic

    def get_move(self, board):

        #This is the board used to emulate the board state.
        emuBoard = copy.deepcopy(board);
        valid_moves = emuBoard.calc_valid_moves(self.symbol)
        max = [0, self.emulateMove(emuBoard, valid_moves[0])]
        for i in range(1, len(valid_moves)):
            moveValue = self.emulateMove(emuBoard, valid_moves[i])

            if self.use_heuristic:
                if self.check_corner(emuBoard, valid_moves[i]):
                    moveValue = moveValue * 1.55
                elif self.check_edge(emuBoard, valid_moves[i]):
                    moveValue = moveValue * 1.35

            if moveValue > max[1]:
                max[0] = i;
                max[1] = moveValue;

        return valid_moves[max[0]]

    def check_edge(self, board, move):
        if(move[0] == 0 or move[0] == (board.get_size()-1)):
            return True
        elif((move[1] == 0 or move[1] == (board.get_size()-1))):
            return True
        return False
    def check_corner(self, board,move):
        if ((move[0] == 0 or move[0] == (board.get_size() - 1)) and (move[1] == 0 or move[1] == (board.get_size()-1))):
            return True
        return False
    def emulateMove(self, board, move):
        board.make_move(self.symbol, move);
        return board.calc_scores()[self.symbol]


class eMinimaxComputerPlayer:
    def __init__(self, symbol, depth, k_heuristic):
        self.symbol = symbol
        self.cutoff = depth;
        self.use_heuristic = k_heuristic

    def get_move(self, board):
        emuBoard = copy.deepcopy(board)
        max_val = None
        valid_moves = emuBoard.calc_valid_moves(self.symbol)
        for i in range(0, len(valid_moves)):
            cur_eval = self.minimax(emuBoard, self.cutoff-1, emuBoard.get_opponent_symbol(self.symbol), valid_moves[i])
            if max_val is None:
                max_val = [cur_eval, valid_moves[i]]
            elif cur_eval > (max_val[0]):
                max_val = [cur_eval, valid_moves[i]]
        return max_val[1]

    def minimax(self, board, depth, cur_symbol, last_move):
        emuboard = copy.deepcopy(board)
        emuboard.make_move(emuboard.get_opponent_symbol(cur_symbol), last_move)

        #The recursive base case along with where the evulation is done and then returned up the recursive stack.
        if depth <= 0 or len(emuboard.calc_valid_moves(cur_symbol)) <= 0:
            initVal = emuboard.calc_scores()[cur_symbol]
            if self.use_heuristic:
                if ((last_move[0] == 0 or last_move[0] == (emuboard.get_size() - 1)) and (last_move[1] == 0 or last_move[1] == (emuboard.get_size() - 1))):
                    initVal = initVal * 1.55
                elif ((last_move[0] == 0 or last_move[0] == (emuboard.get_size() - 1)) or (last_move[1] == 0 or last_move[1] == (emuboard.get_size() - 1))):
                    initVal = initVal * 1.35

            return initVal

        eval = None
        valid_moves = emuboard.calc_valid_moves(cur_symbol);
        for move in valid_moves:
            min_max_val = self.minimax(emuboard, depth - 1, emuboard.get_opponent_symbol(cur_symbol), move)
            if eval is None:
                eval = min_max_val
            else: #if min_max_val is not None
                if cur_symbol == self.symbol:
                    eval = self.min_max_eval(eval, min_max_val, False)
                elif cur_symbol != self.symbol:
                    eval = self.min_max_eval(eval, min_max_val, True)
        return eval

    def min_max_eval(self, val1, val2, get_max):
        if get_max:
            if(val1 > val2):
                return val1
            else:
                return val2
        elif not get_max:
            if (val1 < val2):
                return val1
            else:
                return val2

    #Greedy's evaluation
    def evaulateState(self, board, move):
        emuBoard = copy.deepcopy(board)
        emuBoard.make_move(self.symbol, move)
        return emuBoard.calc_scores()[self.symbol]