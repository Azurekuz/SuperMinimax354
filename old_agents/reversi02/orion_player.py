# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import copy
from core.reversi_board import ReversiBoard

class MinimaxComputerPlayer:

    def __init__(self, symbol, depth, uh=False):
        self.symbol = symbol
        self.root = None
        self.thingsToEval = []
        self.evalDepth = depth
        self.useHeuristic = uh

    def get_move(self, board):
        currentDepth = 0
        self.root = Node(None, board, None)
        self.thingsToEval.append(self.root)
        evalLen = 1
        while (evalLen > 0):
            workingNode = self.thingsToEval[evalLen - 1]
            validMoves = self.getValidMoves(workingNode)
            if(len(workingNode.children) < len(validMoves) and currentDepth < self.evalDepth):
                self.genBoard(workingNode, validMoves)
                currentDepth += 1
            elif(len(validMoves) > 0 or currentDepth >= self.evalDepth or not workingNode.board.game_continues()):
                self.thingsToEval.remove(workingNode)
                self.evalNode(workingNode)
                #print("Node evaluated @ depth " + str(currentDepth) + ": " + str(workingNode.eval))
                currentDepth -= 1
            else:
                workingNode.max = not workingNode.max
            evalLen = len(self.thingsToEval)
        for c in self.root.children:
            if(c.eval == self.root.eval):
                return c.move
        return -1, -1

    def genBoard(self, workingNode, validMoves):
        newBoard = copy.deepcopy(workingNode.board)
        move = validMoves[len(workingNode.children)]
        if workingNode.max:
            newBoard.make_move(self.symbol, move)
        else:
            opponentSymbol = workingNode.board.get_opponent_symbol(self.symbol)
            newBoard.make_move(opponentSymbol, move)
        self.thingsToEval.append(Node(workingNode, newBoard, move))
        workingNode.children.append(self.thingsToEval[len(self.thingsToEval)-1])

    def getValidMoves(self, workingNode):
        if (workingNode.max):
            return workingNode.board.calc_valid_moves(self.symbol)
        else:
            return workingNode.board.calc_valid_moves(workingNode.board.get_opponent_symbol(self.symbol))

    def evalNode(self, node):
        if(len(node.children) == 0):
            if (self.useHeuristic):
                score = node.board.calc_heuristic()[self.symbol]
            else:
                score = node.board.calc_scores()[self.symbol]
            node.eval = score
        else:
            if(node.max):
                node.eval = self.max(node.children)
            else:
                node.eval = self.min(node.children)

    def max(self, children):
        max = -110
        for c in children:
            if(c.eval > max):
                max = c.eval
        return max

    def min(self, children):
        min = 110
        for c in children:
            if(c.eval < min):
                min = c.eval
        return min

    def __name__ (self):
        return "Minimax Player"


class Node:

    def __init__(self, parent, board, move):
        self.parent = parent
        if(parent != None):
            self.max = not parent.max
        else:
            self.max = True
        self.children = []
        self.eval = -1
        self.board = board
        self.move = move