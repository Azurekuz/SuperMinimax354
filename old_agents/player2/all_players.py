from player2 import orion_player, quiescent_search, lookup_table, alpha_beta_pruning, t_table_player, combinedAgent, transposition_table
def get_default_player(symbol):
    """
    :returns: a default minimax player that can operate successfully on a given 8x8 board
    """
    return orion_player.oMinimaxComputerPlayer(symbol)

def get_player_a(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return alpha_beta_pruning.AlphaBetaPruning(symbol, True)


def get_player_b(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return quiescent_search.QuiescentSearch(symbol, True)


def get_player_c(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return lookup_table.lookup_table(symbol, True)


def get_player_d(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return transposition_table.TranspositionTable(symbol, 3, True, True)


def get_combined_player(symbol):
    """
    :returns: the best combination of the minimax enhancements that your team can create
    """
    return combinedAgent(symbol)