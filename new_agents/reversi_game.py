# Written by Toby Dragon

import copy
import random
from datetime import datetime
from new_agents.reversi_board import ReversiBoard, _drawBoard
from new_agents.all_players import get_default_player, get_player_a, get_player_b, get_player_c, get_player_d, get_combined_player;

from new_agents.mini_mega import Node

class ReversiGame:

    def __init__(self, player1, player2, show_status=True, board_size=8, board_filename=None):
        self.player1 = player1
        self.player2 = player2
        self.show_status = show_status
        if board_filename is None:
            self.board = ReversiBoard(board_size)
        else:
            self.board = ReversiBoard(board_filename=board_filename)
        self.decision_times = {self.player1.symbol: 0, self.player2.symbol: 0}
        self.play_game()

    def play_game(self):
        if self.show_status:
            self.board.draw_board()
        while self.board.game_continues():
            self.play_round()
        if self.show_status:
            print("Game over, Final Scores:")
            print_scores(self.board.calc_scores())

    def play_round(self):
        start = datetime.now()
        self.play_move(self.player1)
        self.decision_times[self.player1.symbol] += (datetime.now()-start).total_seconds()
        start = datetime.now()
        self.play_move(self.player2)
        self.decision_times[self.player2.symbol] += (datetime.now()-start).total_seconds()

    def play_move(self, player):
        if self.board.calc_valid_moves(player.symbol):
            chosen_move = player.get_move(copy.deepcopy(self.board))
            if not self.board.make_move(player.symbol, chosen_move):
                print("Error: invalid move made")
            elif self.show_status:
                self.board.draw_board()
                print_scores(self.board.calc_scores())
        elif self.show_status:
            print(player.symbol, "can't move.")

    def calc_winner(self):
        scores = self.board.calc_scores()
        if scores[self.player1.symbol] > scores[self.player2.symbol]:
            return self.player1.symbol
        if scores[self.player1.symbol] < scores[self.player2.symbol]:
            return self.player2.symbol
        else:
            return "TIE"

    def get_decision_times(self):
        return self.decision_times


def print_scores(score_map):
    for symbol in score_map:
        print(symbol, ":", score_map[symbol], end="\t")
    print()


def compare_players(player1, player2, board_size=8, board_filename=None, tests=4):
    game_count_map = {"X": 0, "O": 0, "TIE": 0}
    time_elapsed_map = {"X": 0, "O": 0}
    for i in range(1, tests + 1):
        if i % 1 == 0:
            print(i, "games finished")
        if (i % 2 == 0):
            game = ReversiGame(player1, player2, show_status=True, board_size=board_size, board_filename=board_filename)
        else:
            game = ReversiGame(player2, player1, show_status=True, board_size=board_size, board_filename=board_filename)
        winner = game.calc_winner()
        game_count_map[winner] += 1
        for symbol in game.get_decision_times():
            time_elapsed_map[symbol] += game.get_decision_times()[symbol]

    print(player1.symbol + ": " + player1.__name__())
    print(player2.symbol + ": " + player2.__name__())
    print(game_count_map)
    print(time_elapsed_map)

def testValidMoveAlgorithm():
    board = genRandomBoard()
    oldValidMoveAlgorithm = genRandomBoard().calc_valid_moves("X")
    oldValidMoveAlgorithm.sort()
    player = get_combined_player("X")
    node = Node(None, board, None)
    player.evalAndGetMoves(node)
    newValidMoveAlgorithm = node.validMoves
    newValidMoveAlgorithm.sort()
    _drawBoard(board._board)
    print("Old: " + str(oldValidMoveAlgorithm))
    print("New: " + str(newValidMoveAlgorithm))

def genRandomBoard():
    board = ReversiBoard(8)
    physicalBoard = board._board
    tileChoices = ['X', 'O', ' ']
    for i in range(len(physicalBoard)):
        for j in range(len(physicalBoard)):
            physicalBoard[i][j] = random.choice(tileChoices)
    return board

def main():
    compare_players(get_combined_player("O"), get_combined_player("X"), board_size=8, tests= 1)
    #for i in range(10):
    #    testValidMoveAlgorithm()

if __name__ == "__main__":
    main()