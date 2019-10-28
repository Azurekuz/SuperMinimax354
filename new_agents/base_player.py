# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import copy
from new_agents.reversi_board import ReversiBoard
from datetime import datetime, timedelta
from queue import Queue

class MinimaxComputerPlayer:

    def __init__(self, symbol, timeLimit, uh=False):
        self.symbol = symbol
        self.root = None
        self.curBoardArrayMax = None;
        self.timeLimit = timedelta(seconds=(timeLimit-.01))
        self.tileCount = 0
        self.thingsToSearch =  Queue()
        self.useHeuristic = uh

    def get_move(self, board):
        startTime = datetime.now()                  #Get the time the function started at for timing
        tileCount = self.countPieces(board._board)

        if self.root is not None and tileCount > self.tileCount:  # Find out which move the opponents took and make that the root
            foundMove = False
            for c in self.root.children:
                if c.board._board == board._board:
                    self.root = c
                    foundMove = True
                    break
        if self.root is None or tileCount < self.tileCount or not foundMove:  # If we can't for some reason make a new root
            print("Generate new root")
            self.root = Node(None, board, None)
            self.root.eval = -110
            self.thingsToSearch.put(self.root)

        self.tileCount = tileCount
        self.root.parent = None                     #Cut off root from all the other nodes checked so the old root can be deleted

        self.trimQueue()        #Trim the self.thingsToSearch queue down to only items that are still relevant


        while not self.thingsToSearch.empty():               #Start main search loop
            if datetime.now() - startTime > self.timeLimit:     #If almost out of time, stop searching and return current best
                if self.root is not None and self.root.moveToBestChoice is not None:
                    move = self.root.moveToBestChoice
                else:
                    move = (-1, -1)
                self.root = self.root.bestChoice
                return move

            workingNode = self.thingsToSearch.get()
            workingNode.validMoves = self.getValidMoves(workingNode)    #Get workingnode and calculate moves it could make

            if len(workingNode.validMoves) > 0:             #If it has moves it could make, add them to the tree
                if workingNode.max:
                    workingNode.eval = -110                 #Overwrite the old eval before dragging children's evaluations up
                else:
                    workingNode.eval = 110
                for move in workingNode.validMoves:
                    self.genBoard(workingNode, move)
                self.evalUp(workingNode)

            elif workingNode.board.game_continues():        #If it doesn't have moves it could make, swap it to the other player and do the above
                workingNode.max = not workingNode.max
                workingNode.validMoves = self.getValidMoves(workingNode)
                if workingNode.max:
                    workingNode.eval = -110                 #Overwrite the old eval before dragging children's evaluations up
                else:
                    workingNode.eval = 110
                for move in workingNode.validMoves:
                    self.genBoard(workingNode, move)
                self.evalUp(workingNode)

        if self.root is not None and self.root.moveToBestChoice is not None:
            move = self.root.moveToBestChoice                   #If we've calculated to the end of all possible branches, return the best choice
        else:
            move = (-1,-1)
        self.root = self.root.bestChoice
        return move

    def genBoard(self, node, move):                     #Generate a new board and set it as the node's child based on the given move
        newBoard = copy.deepcopy(node.board)
        if node.max:
            newBoard.make_move(self.symbol, move)       #If max node, make a move
        else:
            opponentSymbol = node.board.get_opponent_symbol(self.symbol)    #If not, opponent makes a move
            newBoard.make_move(opponentSymbol, move)
        newNode = Node(node, newBoard, move)
        self.thingsToSearch.put(newNode)                #Add to list of things to eval
        node.children.append(newNode)
        self.evalBottom(newNode)

    def getValidMoves(self, node):                          #Infrastructure to call calc_valid_moves appropriately
        if (node.max):
            return node.board.calc_valid_moves(self.symbol)
            #return self.genValidMoves(self.symbol, node.board)
        else:
            return node.board.calc_valid_moves(node.board.get_opponent_symbol(self.symbol))
            #return self.genValidMoves(node.board.get_opponent_symbol(self.symbol), node.board)


    def evalBottom(self, node):                                 #Evalutate a node that just created and has no children
        if self.useHeuristic:
            score = node.board.calc_heuristic()[self.symbol]    #If using heuristic, calc based on that
        else:
            score = node.board.calc_scores()[self.symbol]       #Otherwise just use the score the board gives
        node.eval = score

    def evalUp(self, node):                                     #The function to trickle the score upwards when we change it
        if(node.max):
            self.max(node)
        else:
            self.min(node)
        node.heuristicDepth = node.children[0].heuristicDepth
        if node.parent is not None:
            self.evalUp(node.parent)

    def max(self, node):
        node.eval = -110
        for c in node.children:
            if c.eval > node.eval:
                node.eval = c.eval
                node.bestChoice = c
                node.moveToBestChoice = c.move

    def min(self, node):
        node.eval = 110
        for c in node.children:
            if c.eval < node.eval:
                node.eval = c.eval
                node.bestChoice = c
                node.moveToBestChoice = c.move


    def trimQueue(self):
        size = self.thingsToSearch.qsize()
        for i in range(0, size):
            node = self.thingsToSearch.get()
            if self.isRelevant(node):
                self.thingsToSearch.put(node)

    def isRelevant(self, node):
        if node == self.root:
            return True
        elif node.parent is None:
            return False
        else:
            return self.isRelevant(node.parent)


    def countPieces(self, board):
        count = 0
        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                tile = board[i][j]
                if tile == "X" or tile =="O":
                    count += 1
        return count


    def __name__ (self):
        return "Revamped Minimax Player"

    def genValidMoves(self, symbol, board):
        # Returns a list of [x,y] lists of valid moves for the given player on the given board.
        validMoves = []
        for x in range(len(board._board)):
            for y in range(len(board._board)):
                if self.checkValidMove(board, x, y, symbol) != False:
                    validMoves.append([x, y])
        return validMoves

    def checkValidMove(self, board, xstart, ystart, tile):
        canFlip = False
        # Returns False if the player's move on space xstart, ystart is invalid.
        # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
        if board._board[xstart][ystart] != ' ' or not xstart >= 0 and (xstart <= self.curBoardArrayMax and ystart >= 0 and ystart <=self.curBoardArrayMax):
            return False

        board._board[xstart][ystart] = tile  # temporarily set the tile on the board.

        if tile == 'X':
            otherTile = 'O'
        else:
            otherTile = 'X'

        tilesToFlip = []
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection  # first step in the direction
            y += ydirection  # first step in the direction
            if (x <= self.curBoardArrayMax and y>= 0 and y <=self.curBoardArrayMax) and board._board[x][y] == otherTile:
                # There is a piece belonging to the other player next to our piece.
                tilesToFlip.append([x, y])
                tilesToFlip + self.checkDirection([xdirection, ydirection], board, tile, x, y, otherTile)
                if not (x <= self.curBoardArrayMax and y>= 0 and y <=self.curBoardArrayMax):
                    continue
        board._board[xstart][ystart] = ' '  # restore the empty space
        if len(tilesToFlip) == 0:  # If no tiles were flipped, this is not a valid move.
            return False
        return tilesToFlip

    def checkDirection(self, dirTuple, board, tile, x, y, otherTile):
        xdirection, ydirection = dirTuple
        tilesToFlip = []
        while board._board[x][y] == otherTile:
            tilesToFlip.append([x, y])
            x += xdirection
            y += ydirection
            if not (x <= self.curBoardArrayMax and y>= 0 and y <=self.curBoardArrayMax):  # break out of while loop, then continue in for loop
                break
            if board._board[x][y] == tile:
                return tilesToFlip
        return []

class Node:

    def __init__(self, parent, board, move):
        self.parent = parent
        if not parent is None:
            self.max = not parent.max
            self.depth = parent.depth + 1
        else:
            self.max = True
            self.depth = 0
        self.children = []
        self.eval = None
        self.board = board
        self.validMoves = None
        self.bestChoice = None
        self.moveToBestChoice = None
        self.move = move
        self.heuristicDepth = self.depth