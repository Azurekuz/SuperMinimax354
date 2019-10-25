# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import copy
from reversi_board import ReversiBoard
from base_player import MinimaxComputerPlayer
from datetime import datetime, timedelta
from queue import Queue

class LookupTable(MinimaxComputerPlayer):

    def __init__(self, symbol, timeLimit, uh=False, ult=False):
        super().__init__(symbol, timeLimit, uh)
        self.useLookupTable = ult
        self.valueBoardEight = [[32, 8, 8, 8, 8, 8, 8, 32],
                                [8, 16, 4, 4, 4, 4, 16, 8],
                                [8, 4, 8, 2, 2, 8, 4, 8],
                                [8, 4, 2, 0, 0, 2, 4, 8],
                                [8, 4, 2, 0, 0, 2, 4, 8],
                                [8, 4, 8, 2, 2, 8, 4, 8],
                                [8, 16, 4, 4, 4, 4, 16, 8],
                                [32, 8, 8, 8, 8, 8, 8, 32]]

    def get_move(self, board):
        startTime = datetime.now()                  #Get the time the function started at
        tileCount = self.countPieces(board._board)
        if self.root is None or tileCount < self.tileCount:                       #If we're just starting the game and have no root, set a null root
            print("Generate new Root")
            self.root = Node(None, board, None)
            self.root.eval = -110
            self.thingsToSearch.put(self.root)
        else:                                       #Otherwise find out which move the opponents took and make that the root
            for c in self.root.children:
                if c.board._board == board._board:
                    self.root = c
                    break
        self.tileCount = tileCount
        self.root.parent = None                     #Cut off root from all the other nodes checked so the old root can be deleted

        self.trimQueue()        #Trim the self.thingsToSearch queue down to only items that are still relevant


        while not self.thingsToSearch.empty():               #Start main search loop
            if datetime.now() - startTime > self.timeLimit:     #If almost out of time, stop searching and return current best
                if self.root is not None and self.root.moveToBestChoice is not None:
                    move = self.root.moveToBestChoice  # If we've calculated to the end of all possible branches, return the best choice
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
        else:
            return node.board.calc_valid_moves(node.board.get_opponent_symbol(self.symbol))

    def evalBottom(self, node):                                 #Evalutate a node that just created and has no children
        if self.useHeuristic:
            score = node.board.calc_heuristic()[self.symbol]    #If using heuristic, calc based on that
        else:
            score = node.board.calc_scores()[self.symbol]       #Otherwise just use the score the board gives
        if self.useLookupTable and len(node.board._board) == 8:
            score += self.valueBoardEight[node.move[0]][node.move[1]]
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