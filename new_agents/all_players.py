import base_player, alpha_beta_pruning, quiescent_search, lookup_table, transposition_table, mini_mega

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
    return alpha_beta_pruning.AlphaBetaPruning(symbol, True)


def get_player_b(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return quiescent_search.QuiescentSearch(symbol, 3, True)


def get_player_c(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return lookup_table.LookupTable(symbol, 2.5, ult=True)


def get_player_d(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return transposition_table.TranspositionTable(symbol, 3, utt=True)


def get_combined_player(symbol):
    """
    :returns: the best combination of the minimax enhancements that your team can create
    """
    return mini_mega.MiniMega(symbol, 2.5)