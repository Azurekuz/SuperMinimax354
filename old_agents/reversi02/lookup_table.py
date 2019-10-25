<<<<<<< HEAD
from orion_player import oMinimaxComputerPlayer
import copy
=======
from orion_player import MinimaxComputerPlayer

>>>>>>> 6d53e1892bc879ac316892f81ab96593c3e0c241

class LookupTable(MinimaxComputerPlayer):
    def __init__(self, symbol, ult=False):
        super().__init__(symbol, 3)
        self.use_lookup_table = ult
        self.valueBoardEight=([16, 8, 8, 0, 8, 8, 8, 16],
                                [8, 8, 4, 4, 4, 4, 8, 8],
                                [8, 4, 4, 2, 2, 4, 4, 8],
                                [8, 4, 2, 0, 0, 2, 4, 8],
                                [8, 4, 2, 0, 0, 2, 4, 8],
                                [8, 4, 4, 2, 2, 4, 4, 8],
                                [8, 8, 4, 4, 4, 4, 8, 8],
                                [16, 8, 8, 8, 8, 8, 8, 16])

    def get_move(self, board):
        evalDepth = 3
        currentDepth = 0
        self.root = Node(None, board, None)
        self.thingsToEval.append(self.root)
        evalLen = 1
        while (evalLen > 0):
            workingNode = self.thingsToEval[evalLen - 1]
            validMoves = self.getValidMoves(workingNode)
            if (len(workingNode.children) < len(validMoves) and currentDepth < evalDepth):
                self.genBoard(workingNode, validMoves)
                currentDepth += 1
            elif (len(validMoves) > 0 or currentDepth >= evalDepth or not workingNode.board.game_continues()):
                self.thingsToEval.remove(workingNode)
                self.evalNode(workingNode)
                # print("Node evaluated @ depth " + str(currentDepth) + ": " + str(workingNode.eval))
                currentDepth -= 1
            else:
                workingNode.max = not workingNode.max
            evalLen = len(self.thingsToEval)
        for c in self.root.children:
            if (c.eval == self.root.eval):
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
        workingNode.children.append(self.thingsToEval[len(self.thingsToEval) - 1])

    def getValidMoves(self, workingNode):
        if (workingNode.max):
            return workingNode.board.calc_valid_moves(self.symbol)
        else:
            return workingNode.board.calc_valid_moves(workingNode.board.get_opponent_symbol(self.symbol))

    def evalNode(self, node):
        if(not self.use_lookup_table):
            super().evalNode(node)
            return
        if(len(node.children) == 0):
            score = node.board.calc_scores()[self.symbol]
            node.eval = score
            #valueBoardScore = self.valueBoardEight[node.move[0]][node.move[1]]
        elif(node.parent is not None):
            if(node.max):
                valuex = int(node.move[0])
                valuey = int(node.move[1])
                valueBoardScore = self.valueBoardEight[valuex][valuey]
                node.eval = self.max(node.children)
                #print(node.eval)
                node.eval += valueBoardScore
                #print(node.eval)
            else:
                valuex = int(node.move[0])
                valuey = int(node.move[1])
                valueBoardScore = self.valueBoardEight[valuex][valuey]
                node.eval = self.min(node.children)
                #print(node.eval)
                node.eval -= valueBoardScore
                #print(node.eval)



    def max(self, children):
        max = 0
        for c in children:
            if(c.eval > max):
                max = c.eval
        return max

    def min(self, children):
        min = 64
        for c in children:
            if(c.eval < min):
                min = c.eval
        return min

    def __str__(self):
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