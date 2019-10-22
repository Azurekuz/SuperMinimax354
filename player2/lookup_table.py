<<<<<<< HEAD
from orion_player import oMinimaxComputerPlayer


class lookup_table(oMinimaxComputerPlayer):
    def __init__(self, symbol):
        super().__init__(symbol)
        self.originalBoard = None;
        self.valueBoardEight={[16, 8, 8, 0, 8, 8, 8, 16],
                        [8, 8, 4, 4, 4, 4, 8, 8],
                        [8, 4, 4, 2, 2, 4, 4, 8],
                        [8, 4, 2, 0, 0, 2, 4, 8],
                        [8, 4, 2, 0, 0, 2, 4, 8],
                        [8, 4, 4, 2, 2, 4, 4, 8],
                        [8, 8, 4, 4, 4, 4, 8, 8],
                        [16, 8, 8, 8, 8, 8, 8, 16]}

    def get_move(self, board):
        return oMinimaxComputerPlayer.get_move()

    def genBoard(self, workingNode, validMoves):
        return oMinimaxComputerPlayer.genBoard()

    def getValidMoves(self, workingNode):
        if (workingNode.max):
            return workingNode.board.calc_valid_moves(self.symbol)
        else:
            return workingNode.board.calc_valid_moves(workingNode.board.get_opponent_symbol(self.symbol))

    def evalNode(self, node):
        if(len(node.children) == 0):
            score = node.board.calc_scores()[self.symbol]
            node.eval = score
            valueBoardScore = self.valueBoardEight[node.children.move[0]][node.children.move[1]]
        else:
            if(node.max):
                valueBoardScore = self.valueBoardEight[node.children.move[0]][node.children.move[1]]
                node.eval += valueBoardScore
                node.eval = self.max(node.children)
            else:
                valueBoardScore = self.valueBoardEight[node.children.move[0]][node.children.move[1]]
                node.eval -= valueBoardScore
                node.eval = self.min(node.children)



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
=======
from orion_player import oMinimaxComputerPlayer


class lookup_table(oMinimaxComputerPlayer):
    def __init__(self, symbol):
        super().__init__(symbol)
        self.originalBoard = None;
        self.valueBoardEight={[16, 8, 8, 0, 8, 8, 8, 16],
                        [8, 8, 4, 4, 4, 4, 8, 8],
                        [8, 4, 4, 2, 2, 4, 4, 8],
                        [8, 4, 2, 0, 0, 2, 4, 8],
                        [8, 4, 2, 0, 0, 2, 4, 8],
                        [8, 4, 4, 2, 2, 4, 4, 8],
                        [8, 8, 4, 4, 4, 4, 8, 8],
                        [16, 8, 8, 8, 8, 8, 8, 16]}

    def get_move(self, board):
        return oMinimaxComputerPlayer.get_move()

    def genBoard(self, workingNode, validMoves):
        return oMinimaxComputerPlayer.genBoard()

    def getValidMoves(self, workingNode):
        if (workingNode.max):
            return workingNode.board.calc_valid_moves(self.symbol)
        else:
            return workingNode.board.calc_valid_moves(workingNode.board.get_opponent_symbol(self.symbol))

    def evalNode(self, node):
        if(len(node.children) == 0):
            score = node.board.calc_scores()[self.symbol]
            node.eval = score
            valueBoardScore = self.valueBoardEight[node.children.move[0]][node.children.move[1]]
        else:
            if(node.max):
                valueBoardScore = self.valueBoardEight[node.children.move[0]][node.children.move[1]]
                node.eval += valueBoardScore
                node.eval = self.max(node.children)
            else:
                valueBoardScore = self.valueBoardEight[node.children.move[0]][node.children.move[1]]
                node.eval -= valueBoardScore
                node.eval = self.min(node.children)



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
>>>>>>> master
        self.move = move