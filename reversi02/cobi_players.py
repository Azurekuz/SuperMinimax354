# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import random
import copy


class HumanPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        # Let the player type in their move.
        # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
        valid_digits = []
        for i in range(1, board.get_size()+1):
            valid_digits.append(str(i))
        no_valid_move = True
        while no_valid_move:
            move = input(self.symbol + ', enter your move:').lower()
            if len(move) == 2 and move[0] in valid_digits and move[1] in valid_digits:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if board.is_valid_move(self.symbol, ( x, y) ):
                    no_valid_move = False
                    return [x, y]
                else:
                    print('Not a valid move.')
            else:
                print('Bad input. Type valid x digit, then the y digit.')


class RandomComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        return random.choice(board.calc_valid_moves(self.symbol))


class GreedyComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        best_move = None
        max_score = -1000
        new_board = copy.deepcopy(board)
        valid_moves = board.calc_valid_moves(self.symbol)
        for x in range(len(valid_moves)):
            new_board.make_move(self.symbol, valid_moves[x])
            my_score = new_board.calc_scores()[self.symbol]
            if my_score > max_score:
                max_score = my_score
                best_move = valid_moves[x]

        return best_move


class cMinimaxPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        return self.max_function(board, 3, None)[1]

    def max_function(self, board, depth, move):
        if len(board.calc_valid_moves(self.symbol)) == 0 or depth > 2:
            player_score = board.calc_scores()[self.symbol]
            opp_score = board.calc_scores()[board.get_opponent_symbol(self.symbol)]
            if player_score > opp_score:
                return player_score, move
            elif player_score < opp_score:
                return opp_score * -1, move
            else:
                return 0, move
        else:
            outcomes = []
            for moves in board.calc_valid_moves(self.symbol):
                new_board = copy.deepcopy(board)
                new_board.make_move(self.symbol, moves)
                if depth == 0:
                    move = moves
                val = self.min_function(new_board, depth+1, move)
                outcomes.append(val)
            return max(outcomes)

    def min_function(self, board, depth, move):
        opp_symbol = board.get_opponent_symbol(self.symbol)
        if len(board.calc_valid_moves(opp_symbol)) == 0 or depth > 2:
            player_score = board.calc_scores()[self.symbol]
            opp_score = board.calc_scores()[opp_symbol]
            if player_score > opp_score:
                return player_score, move
            elif player_score < opp_score:
                return opp_score * -1, move
            else:
                return 0, move
        else:
            outcomes = []
            for moves in board.calc_valid_moves(opp_symbol):
                new_board = copy.deepcopy(board)
                new_board.make_move(opp_symbol, moves)
                if depth == 0:
                    move = moves
                val = self.max_function(new_board, depth+1, move)
                outcomes.append(val)
            return min(outcomes)


class ElonsGreedyComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        newboard = copy.deepcopy(board)
        oldcount = board.calc_scores().get(self.symbol)
        validmoves = board.calc_valid_moves(self.symbol)
        scores = {}
        size = board.get_size() - 1
        i = 0
        for move in validmoves:
            newboard.make_move(self.symbol, move)
            currscore = newboard.calc_scores().get(self.symbol) - oldcount
            # if a corner move
            if move == [0, 0] or move == [0, size] or move == [size, 0] or move == [size, size]:
                currscore += 6
            # if an edge move
            elif move[0] == 0 or move[0] == size or move[1] == 0 or move[1] == size:
                currscore += 3
            scores[i] = currscore
            i += 1

        maxscore = scores.get(0)
        maxscorekey = 0
        # look through the dictionary and find the max score
        for key, val in scores.items():
            if val > maxscore:
                maxscore = val
                maxscorekey = key
        return validmoves[maxscorekey]








