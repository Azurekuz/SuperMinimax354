from orion_player import MinimaxComputerPlayer
from alpha_beta_pruning import AlphaBetaPruning
from quiescent_search import QuiescentSearch
from transposition_table import TranspositionTable
from lookup_table import LookupTable
#from master_agent import MasterAgent

def get_default_player(symbol):
    """
    :returns: a default minimax player that can operate successfully on a given 8x8 board
    """
    player = MinimaxComputerPlayer(symbol, 3)
    return player


def get_player_a(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    player = AlphaBetaPruning(symbol);
    return player;


def get_player_b(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    player = QuiescentSearch(symbol);
    return player;


def get_player_c(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    player = TranspositionTable(symbol, 3, utt=True);
    return player;

def get_player_d(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    pass;

def get_combined_player(symbol):
    """
    :returns: the best combination of the minimax enhancements that your team can create
    """
    pass