<<<<<<< HEAD
from player2.orion_player import oMinimaxComputerPlayer
from player2.quiescent_search import QuiescentSearch;
from player2.alpha_beta_pruning import AlphaBetaPruning;
from player2.lookup_table import lookup_table;

def get_default_player(symbol):
    """
    :returns: a default minimax player that can operate successfully on a given 8x8 board
    """
    player = oMinimaxComputerPlayer(symbol);
    return player;


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
    player = lookup_table(symbol);
    return player;


def get_player_d(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    pass


def get_combined_player(symbol):
    """
    :returns: the best combination of the minimax enhancements that your team can create
    """
=======
from player2.orion_player import oMinimaxComputerPlayer
from player2.quiescent_search import QuiescentSearch;
from player2.alpha_beta_pruning import AlphaBetaPruning;
from player2.lookup_table import lookup_table;

def get_default_player(symbol):
    """
    :returns: a default minimax player that can operate successfully on a given 8x8 board
    """
    player = oMinimaxComputerPlayer(symbol);
    return player;


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
    player = lookup_table(symbol);
    return player;


def get_player_d(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    pass


def get_combined_player(symbol):
    """
    :returns: the best combination of the minimax enhancements that your team can create
    """
>>>>>>> master
    pass