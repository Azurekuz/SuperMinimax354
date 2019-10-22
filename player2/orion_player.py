<<<<<<< HEAD
# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import random
import copy
from reversi_board import ReversiBoard

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

    def __str__(self):
        return "Human Player"


class RandomComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        return random.choice(board.calc_valid_moves(self.symbol))

    def __str__(self):
        return "Random Player"


class GreedyComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        highestScore = 0
        bestMove = (-1,-1)
        validMoves = board.calc_valid_moves(self.symbol)
        for move in validMoves:
            workingBoard = copy.deepcopy(board)
            workingBoard.make_move(self.symbol, move)
            if(self.evalBoard(workingBoard) > highestScore):
                highestScore = self.evalBoard(workingBoard)
                bestMove = move
        return bestMove

    def evalBoard(self, board):
        return board.calc_scores()[self.symbol]

    def __str__(self):
        return "Greedy Player"

class oMinimaxComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol
        self.root = None
        self.thingsToEval = []

    def get_move(self, board):
        evalDepth = 3
        currentDepth = 0
        self.root = Node(None, board, None)
        self.thingsToEval.append(self.root)
        evalLen = 1
        while (evalLen > 0):
            workingNode = self.thingsToEval[evalLen - 1]
            validMoves = self.getValidMoves(workingNode)
            if(len(workingNode.children) < len(validMoves) and currentDepth < evalDepth):
                self.genBoard(workingNode, validMoves)
                currentDepth += 1
            elif(len(validMoves) > 0 or currentDepth >= evalDepth or not workingNode.board.game_continues()):
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
            score = node.board.calc_scores()[self.symbol]
            node.eval = score
        else:
            if(node.max):
                node.eval = self.max(node.children)
            else:
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
# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import random
import copy
from reversi_board import ReversiBoard

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

    def __str__(self):
        return "Human Player"


class RandomComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        return random.choice(board.calc_valid_moves(self.symbol))

    def __str__(self):
        return "Random Player"


class GreedyComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        highestScore = 0
        bestMove = (-1,-1)
        validMoves = board.calc_valid_moves(self.symbol)
        for move in validMoves:
            workingBoard = copy.deepcopy(board)
            workingBoard.make_move(self.symbol, move)
            if(self.evalBoard(workingBoard) > highestScore):
                highestScore = self.evalBoard(workingBoard)
                bestMove = move
        return bestMove

    def evalBoard(self, board):
        return board.calc_scores()[self.symbol]

    def __str__(self):
        return "Greedy Player"

class oMinimaxComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol
        self.root = None
        self.thingsToEval = []

    def get_move(self, board):
        evalDepth = 3
        currentDepth = 0
        self.root = Node(None, board, None)
        self.thingsToEval.append(self.root)
        evalLen = 1
        while (evalLen > 0):
            workingNode = self.thingsToEval[evalLen - 1]
            validMoves = self.getValidMoves(workingNode)
            if(len(workingNode.children) < len(validMoves) and currentDepth < evalDepth):
                self.genBoard(workingNode, validMoves)
                currentDepth += 1
            elif(len(validMoves) > 0 or currentDepth >= evalDepth or not workingNode.board.game_continues()):
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
            score = node.board.calc_scores()[self.symbol]
            node.eval = score
        else:
            if(node.max):
                node.eval = self.max(node.children)
            else:
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