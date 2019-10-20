#Made by Eugene Kuznetsov
import random
import copy
from collections import deque
from eugenek_players import eMinimaxComputerPlayer

class QuiescentSearch(eMinimaxComputerPlayer):
    def __init__(self):
        pass

    def get_move(self, board):
        emuBoard = copy.deepcopy(board);
        self.begin_minimax(emuBoard)

    def evaluate(self, board, symbol, last_move):
        eval = board.calc_scores()[symbol]
        if self.use_heuristic:
            if ((last_move[0] == 0 or last_move[0] == (board.get_size() - 1)) and (
                    last_move[1] == 0 or last_move[1] == (board.get_size() - 1))):
                eval = eval * 1.55
            elif ((last_move[0] == 0 or last_move[0] == (board.get_size() - 1)) or (
                    last_move[1] == 0 or last_move[1] == (board.get_size() - 1))):
                eval = eval * 1.35
        return eval;