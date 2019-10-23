from orion_player import oMinimaxComputerPlayer


class lookup_table(oMinimaxComputerPlayer):
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
        return oMinimaxComputerPlayer.get_move(self,board)

    def genBoard(self, workingNode, validMoves):
        return oMinimaxComputerPlayer.genBoard(self,workingNode, validMoves)

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
                node.eval += valueBoardScore
                node.eval = self.max(node.children)
            else:
                valuex = int(node.move[0])
                valuey = int(node.move[1])
                valueBoardScore = self.valueBoardEight[valuex][valuey]
                node.eval -= valueBoardScore
                node.eval = self.min(node.children)



    def max(self, children):
        max = children[0]
        for c in children:
            if(c.eval > max):
                max = c.eval
        return max

    def min(self, children):
        min = children[0]
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