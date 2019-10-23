# Written by Toby Dragon

import copy
from datetime import datetime
from reversi02.reversi_board import ReversiBoard
from player2 import all_players, alpha_beta_pruning, combinedAgent, lookup_table, orion_player, quiescent_search, t_table_player;
'''
from reversi02.desmondl_players import HumanPlayer, RandomComputerPlayer, GreedComputerPlayer,  dMiniMaxComputerPlayer
from reversi02.cobi_players import HumanPlayer, RandomComputerPlayer, GreedyComputerPlayer, cMinimaxPlayer
from reversi02.eugenek_players import HumanPlayer, RandomComputerPlayer, GreedyComputerPlayer, eMinimaxComputerPlayer
from reversi02.orion_player import HumanPlayer, RandomComputerPlayer, GreedyComputerPlayer, oMinimaxComputerPlayer
from reversi02.t_table_player import tTableMinimaxComputerPlayer
from reversi02.quiescent_search import QuiescentSearch;
from reversi02.alpha_beta_pruning import AlphaBetaPruning;
from reversi02.lookup_table import lookup_table;
'''

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


def compare_players(player1, player2, board_size=8, board_filename=None, tests=10):
    game_count_map = {"X": 0, "O": 0, "TIE": 0}
    time_elapsed_map = {"X": 0, "O": 0}
    for i in range(1, tests + 1):
        if i % 1 == 0:
            print(i, "games finished")
        if (i % 2 == 0):
            game = ReversiGame(player1, player2, show_status=False, board_size=board_size, board_filename=board_filename)
        else:
            game = ReversiGame(player2, player1, show_status=False, board_size=board_size, board_filename=board_filename)
        winner = game.calc_winner()
        game_count_map[winner] += 1
        for symbol in game.get_decision_times():
            time_elapsed_map[symbol] += game.get_decision_times()[symbol]

    print(player1.symbol + ": " + player1.__name__())
    print(player2.symbol + ": " + player2.__name__())
    print(game_count_map)
    print(time_elapsed_map)

def get_default_player(symbol):
    """
    :returns: a default minimax player that can operate successfully on a given 8x8 board
    """
    player = orion_player.oMinimaxComputerPlayer(symbol, 3, uh=False)
    return player


def get_player_a(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    player = alpha_beta_pruning.AlphaBetaPruning(symbol);
    return player;


def get_player_b(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    player = quiescent_search.QuiescentSearch(symbol);
    return player;


def get_player_c(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    player = t_table_player.tTableMinimaxComputerPlayer(symbol, 10, utt=True, uh=False);
    return player;

def get_player_d(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return lookup_table.lookup_table(symbol)

def get_combined_player(symbol):
    """
    :returns: the best combination of the minimax enhancements that your team can create
    """
    return combinedAgent.CombinedAgent(symbol)


def main():
    #ReversiGame(MinimaxComputerPlayer("O", 4, True), HumanPlayer("X")) #board_filename="board4by4nearEnd.json"
    print("")
    #compare_players(get_player_b("O"), get_player_d("X"), board_size=8)
    #compare_players(get_player_b("O"), get_player_c("X"), board_size=8)
    compare_players(get_default_player("O"), get_default_player("X"), board_size=8)
    #get_combined_player("X")
if __name__ == "__main__":
    main()