# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import copy
from reversi_board import ReversiBoard

class tTableMinimaxComputerPlayer:

    def __init__(self, symbol, depth, utt=False, uh=False):
        self.symbol = symbol
        self.root = None
        self.thingsToEval = []
        self.evalDepth = depth
        self.useTTable = utt
        self.useHeuristic = uh
        self.movesTaken = 0
        if utt:
            self.tTable = {}

    def get_move(self, board):
        currentDepth = 0
        self.root = Node(None, board, None, self.movesTaken*2)
        if self.useTTable and board in self.tTable and self.tTable[board][1] >= self.evalDepth + self.root.depth:
            self.root.eval = self.tTable[board]
        self.thingsToEval.append(self.root)     #initialize needed Variables for the search
        evalLen = 1     #Keep track of the number of items in thingsToEval


        while evalLen > 0:
            workingNode = self.thingsToEval[evalLen - 1]    #Grab node to evaluate
            validMoves = self.getValidMoves(workingNode)    #Get list of valid moves from said node
            if(len(workingNode.children) < len(validMoves) and currentDepth < self.evalDepth):      #If not all children have been generated and we're not at the required depth:
                self.genBoard(workingNode, validMoves, currentDepth)      #Evaluate board for the first child
                currentDepth += 1                           #Also adjust depth so we don't go too far
            elif(len(validMoves) > 0 or currentDepth >= self.evalDepth or not workingNode.board.game_continues()):
                self.thingsToEval.remove(workingNode)
                self.evalNode(workingNode, currentDepth)
                #print("Node evaluated @ depth " + str(currentDepth) + ": " + str(workingNode.eval))
                currentDepth -= 1
            else:
                workingNode.max = not workingNode.max
            evalLen = len(self.thingsToEval)

        print("Optimal move's heuristic is: " + str(self.root.eval))
        self.movesTaken += 1

        for c in self.root.children:
            if(c.eval == self.root.eval):
                return c.move
        return -1, -1

    def genBoard(self, workingNode, validMoves, depth):
        """
        :param workingNode: The node that is currently being worked on by the search algorithm
        :param validMoves: A list of valid moves from that node
        :param depth: how deep the search currently is
        :return: None
        :side effect: Takes a move and adds the new board state as a child of workingNode, also sets it up to be
        evaluated if not found in tTable
        """
        newBoard = copy.deepcopy(workingNode.board)
        move = validMoves[len(workingNode.children)]
        if workingNode.max:
            newBoard.make_move(self.symbol, move)
        else:
            opponentSymbol = workingNode.board.get_opponent_symbol(self.symbol)
            newBoard.make_move(opponentSymbol, move)

        if self.useTTable and newBoard in self.tTable and self.tTable[newBoard][1] >= self.evalDepth - depth + workingNode.depth:
            newNode = Node(workingNode, newBoard, move, self.movesTaken*2 + depth)
            newNode.eval = self.tTable[newBoard][0]
            workingNode.children.append(newNode)
        else:
            self.thingsToEval.append(Node(workingNode, newBoard, move, self.movesTaken*2 + depth))
            workingNode.children.append(self.thingsToEval[len(self.thingsToEval)-1])

    def getValidMoves(self, workingNode):
        if workingNode.max:
            return workingNode.board.calc_valid_moves(self.symbol)
        else:
            return workingNode.board.calc_valid_moves(workingNode.board.get_opponent_symbol(self.symbol))

    def evalNode(self, node, depth):
        if len(node.children) == 0:
            if self.useHeuristic:
                scores = node.board.calc_heuristic()
                score = scores[self.symbol] - scores[node.board.get_opponent_symbol(self.symbol)]
            else:
                scores = node.board.calc_heuristic()
                score = scores[self.symbol] - scores[node.board.get_opponent_symbol(self.symbol)]
        else:
            if node.max:
                score = self.max(node.children)
            else:
                score = self.min(node.children)
        node.eval = score
        if self.useTTable:
            self.permutateBoardState(node, depth, score)

    def permutateBoardState(self, node, depth, score):
        depthScore = self.evalDepth - depth + node.depth
        workingBoard = node.board
        if workingBoard not in self.tTable or self.tTable[workingBoard][1] < depthScore:
            self.tTable[workingBoard] = (score, depthScore)
        workingBoard = node.board.flip_vertical()
        if workingBoard not in self.tTable or self.tTable[workingBoard][1] < depthScore:
            self.tTable[workingBoard] = (score, depthScore)
        workingBoard = node.board.flip_horizontal()
        if workingBoard not in self.tTable or self.tTable[workingBoard][1] < depthScore:
            self.tTable[workingBoard] = (score, depthScore)
        workingBoard = node.board.flip_diagonal_tr_bl()
        if workingBoard not in self.tTable or self.tTable[workingBoard][1] < depthScore:
            self.tTable[workingBoard] = (score, depthScore)
        workingBoard = node.board.flip_diagonal_tl_br()
        if workingBoard not in self.tTable or self.tTable[workingBoard][1] < depthScore:
            self.tTable[workingBoard] = (score, depthScore)
        workingBoard = node.board.rotate_clockwise()
        if workingBoard not in self.tTable or self.tTable[workingBoard][1] < depthScore:
            self.tTable[workingBoard] = (score, depthScore)
        workingBoard = node.board.rotate_counterclockwise()
        if workingBoard not in self.tTable or self.tTable[workingBoard][1] < depthScore:
            self.tTable[workingBoard] = (score, depthScore)
        workingBoard = node.board.rotate_around()
        if workingBoard not in self.tTable or self.tTable[workingBoard][1] < depthScore:
            self.tTable[workingBoard] = (score, depthScore)

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

    def __name__(self):
        str = "Minimax "
        if self.useTTable:
            str += "with "
        else:
            str += "without "
        str += "Transposition Table"
        return str


class Node:

    def __init__(self, parent, board, move, depth):
        self.parent = parent
        if(parent != None):
            self.max = not parent.max
        else:
            self.max = True
        self.children = []
        self.eval = -1
        self.board = board
        self.move = move
        self.depth = depth