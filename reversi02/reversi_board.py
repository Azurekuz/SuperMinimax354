# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import json


class ReversiBoard:

    def __init__(self, size=8, board_filename=None):
        if board_filename is None:
            self._board = _getNewBoard(size)
        else:
            self._board = _board_from_json(board_filename)

    def draw_board(self):
        _drawBoard(self._board)

    def is_valid_move(self, symbol, position):
        return _isValidMove(self._board, symbol, position[0], position[1])

    def calc_scores(self):
        return _getScoreOfBoard(self._board)

    def calc_heuristic(self):
        return _getHeuristicOfBoard(self._board)

    def make_move(self, symbol, position):
        return _makeMove(self._board, symbol, position[0], position[1])

    def calc_valid_moves(self, symbol):
        return _checkValidMoves(self._board, symbol)

    def game_continues(self):
        return self.calc_valid_moves("X") != [] or self.calc_valid_moves("O") != []

    def get_size(self):
        return len(self._board)

    def get_symbol_for_position(self, position):
        return self._board[position[0]][position[1]]

    def get_opponent_symbol(self, symbol):
        if symbol == 'X':
            return 'O'
        else:
            return 'X'

    def to_json_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self._board, f, ensure_ascii=False)

    def flip_vertical(self):
        b = ReversiBoard(len(self._board))
        b._board = flipV(self._board)
        return b

    def flip_horizontal(self):
        b = ReversiBoard(len(self._board))
        b._board = flipH(self._board)
        return b

    def flip_diagonal_tr_bl(self):
        b = ReversiBoard(len(self._board))
        b._board = flipTRBL(self._board)
        return b

    def flip_diagonal_tl_br(self):
        b = ReversiBoard(len(self._board))
        b._board = flipTLBR(self._board)
        return b

    def rotate_clockwise(self):
        b = ReversiBoard(len(self._board))
        b._board = rotCW(self._board)
        return b

    def rotate_counterclockwise(self):
        b = ReversiBoard(len(self._board))
        b._board = rotCCW(self._board)
        return b

    def rotate_around(self):
        b = ReversiBoard(len(self._board))
        b._board = rot180(self._board)
        return b

    def __hash__(self):
        return hash(str(self._board))

    def __eq__(self, other):
        return self._board == other._board

    def __ne__(self, other):
        return not (self == other)


def flipH(board):
    size = len(board)
    newBoard = _getNewBoard(size)
    for i in range(0, size):
        for j in range(0, size):
            newBoard[size - 1 - i][j] = board[i][j]
    return newBoard

def flipV(board):
    size = len(board)
    newBoard = _getNewBoard(size)
    for i in range(0, size):
        for j in range(0, size):
            newBoard[i][size - 1 - j] = board[i][j]
    return newBoard

def flipTRBL(board):
    size = len(board)
    newBoard = _getNewBoard(size)
    for i in range(0, size):
        for j in range(0, size):
            newBoard[i][j] = board[j][i]
    return newBoard

def flipTLBR(board):
    size = len(board)
    newBoard = _getNewBoard(size)
    for i in range(0, size):
        for j in range(0, size):
            newBoard[size - 1 - i][size - 1 - j] = board[j][i]
    return newBoard

def rotCW(board):
    size = len(board)
    newBoard = _getNewBoard(size)
    for i in range(0, size):
        for j in range(0, size):
            newBoard[size - 1 - i][j] = board[j][i]
    return newBoard

def rotCCW(board):
    size = len(board)
    newBoard = _getNewBoard(size)
    for i in range(0, size):
        for j in range(0, size):
            newBoard[i][size - 1 - j] = board[j][i]
    return newBoard

def rot180(board):
    size = len(board)
    newBoard = _getNewBoard(size)
    for i in range(0, size):
        for j in range(0, size):
            newBoard[size - 1 - i][size - 1 - j] = board[i][j]
    return newBoard

def _getNewBoard(size):
    # Creates a brand new, blank board data structure.
    board = []
    for i in range(size):
        board.append([' '] * size)
    # Starting pieces:
    mid = size//2
    board[mid-1][mid-1] = 'X'
    board[mid-1][mid] = 'O'
    board[mid][mid-1] = 'O'
    board[mid][mid] = 'X'
    return board


def _drawBoard(board):
    size = len(board)
    column_label = " "
    for i in range(1, size+1):
        column_label += "   " + str(i)
    divider = "  " + ("+---" * size)

    print(column_label + "\n" + divider)
    for y in range(size):
        print(y + 1, end=' ')
        for x in range(size):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        print(divider)


def _isOnBoard(x, y, size):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= size-1 and y >= 0 and y <=size-1


def _isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    if board[xstart][ystart] != ' ' or not _isOnBoard(xstart, ystart, len(board)):
        return False

    board[xstart][ystart] = tile  # temporarily set the tile on the board.

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection  # first step in the direction
        y += ydirection  # first step in the direction
        if _isOnBoard(x, y, len(board)) and board[x][y] == otherTile:
            # There is a piece belonging to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not _isOnBoard(x, y, len(board)):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not _isOnBoard(x, y, len(board)):  # break out of while loop, then continue in for loop
                    break
            if not _isOnBoard(x, y, len(board)):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = ' '  # restore the empty space
    if len(tilesToFlip) == 0:  # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip

def _makeMove(board, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = _isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def _checkValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    validMoves = []
    for x in range(len(board)):
        for y in range(len(board)):
            if _isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

def _getScoreOfBoard(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
    xscore = 0
    oscore = 0
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}

def _getHeuristicOfBoard(board):
    # Determine the heuristic by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
    xscore = 0
    oscore = 0
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] == 'X':
                if x==0 and y==0:
                    xscore += 5
                elif x==0 or y==0:
                    xscore += 2
                else:
                    xscore += 1
            if board[x][y] == 'O':
                if x == 0 and y == 0:
                    oscore += 5
                elif x == 0 or y == 0:
                    oscore += 2
                else:
                    oscore += 1
    return {'X':xscore, 'O':oscore}

def _board_from_json(board_filename):
    with open(board_filename) as json_file:
        return json.load(json_file)
