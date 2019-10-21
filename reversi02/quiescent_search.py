#Made by Eugene Kuznetsov
import random
import copy
from collections import deque
from eugenek_players import eMinimaxComputerPlayer

class QuiescentSearch(eMinimaxComputerPlayer):
    def __init__(self, symbol, depth, k_heuristic):
        super.__init__(symbol, depth, k_heuristic);
        self.originalBoard = None;

    def get_move(self, board):
        emuBoard = copy.deepcopy(board);
        self.originalBoard = emuBoard;
        self.begin_minimax(emuBoard)

    def evaluate(self, board, symbol, last_move, quietEvaluated = False):
        eval = super.evaluate();
        valid_moves = board.calc_valid_moves;
        if len(valid_moves) <= 0:
            scores = board.calc_scores();
            opponent_symbol = board.get_opponent_symbol(symbol);
            if scores[symbol] > scores[opponent_symbol]:
                eval = eval + 1;
            elif scores[symbol] < scores[opponent_symbol]:
                eval = eval - 1;
            else:
                eval = eval + 0;
        elif not quietEvaluated:
            self.quiet_search(board, 3, board.get_opponent_symbol(symbol), last_move);
        return eval;

    def quiet_search(self, board, depth, cur_symbol, last_move):
        pass