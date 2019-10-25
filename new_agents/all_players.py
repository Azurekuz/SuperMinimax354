from new_agents import base_player
from old_agents.player2 import orion_player

def get_old_player(symbol):
    return orion_player.oMinimaxComputerPlayer(symbol, 3)

def get_default_player(symbol):
    """
    :returns: a default minimax player that can operate successfully on a given 8x8 board
    """
    return base_player.MinimaxComputerPlayer(symbol, 2.5)

def get_player_a(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    #return alpha_beta_pruning.AlphaBetaPruning(symbol, True)
    pass


def get_player_b(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    #return quiescent_search.QuiescentSearch(symbol, True)
    pass


def get_player_c(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    #return lookup_table.lookup_table(symbol, True)
    pass


def get_player_d(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    #return transposition_table.TranspositionTable(symbol, 3, True, True)
    pass


def get_combined_player(symbol):
    """
    :returns: the best combination of the minimax enhancements that your team can create
    """
    #return combinedAgent(symbol)
    pass