from new_agents.orion_player import oMinimaxComputerPlayer


class lookup_table(oMinimaxComputerPlayer):
    def __init__(self, symbol, ult=False):
        super().__init__(symbol, 3)
        self.use_lookup_table = ult
        self.valueBoardEight=([32, 8, 8, 8, 8, 8, 8, 32],
                                [8, 16, 4, 4, 4, 4, 16, 8],
                                [8, 4, 8, 2, 2, 8, 4, 8],
                                [8, 4, 2, 0, 0, 2, 4, 8],
                                [8, 4, 2, 0, 0, 2, 4, 8],
                                [8, 4, 8, 2, 2, 8, 4, 8],
                                [8, 16, 4, 4, 4, 4, 16, 8],
                                [32, 8, 8, 8, 8, 8, 8, 32])

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
        if (len(node.children) == 0):
            if (self.useHeuristic):
                score = node.board.calc_heuristic()[self.symbol]
            else:
                score = node.board.calc_scores()[self.symbol]
                valuex = int(node.move[0])
                valuey = int(node.move[1])
                valueBoardScore = self.valueBoardEight[valuex][valuey]
                score += valueBoardScore
            node.eval = score
        else:
            if (node.max):
                node.eval = self.max(node.children)
            else:
                node.eval = self.min(node.children)
        '''
                valuex = int(node.move[0])
                valuey = int(node.move[1])
                valueBoardScore = self.valueBoardEight[valuex][valuey]
'''


    def max(self, children):
        max = -99999
        for c in children:
            if(c.eval > max):
                max = c.eval
        return max

    def min(self, children):
        min = 99999
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