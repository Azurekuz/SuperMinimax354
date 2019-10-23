from player2 import orion_player, quiescent_search, lookup_table, alpha_beta_pruning, t_table_player, combinedAgent
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
    return alpha_beta_pruning.AlphaBetaPruning(symbol)


def get_player_b(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return quiescent_search.QuiescentSearch(symbol)


def get_player_c(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return lookup_table.lookup_table(symbol)


def get_player_d(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return t_table_player(symbol)


def get_combined_player(symbol):
    """
    :returns: the best combination of the minimax enhancements that your team can create
    """
    return combinedAgent(symbol)