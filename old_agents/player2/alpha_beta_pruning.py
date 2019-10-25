#Cobi alpha beta pruning - not yet working properly

import random
import copy
from core.reversi_board import ReversiBoard
from player2.orion_player import oMinimaxComputerPlayer;

class AlphaBetaPruning(oMinimaxComputerPlayer):

    def __init__(self, symbol, uabp=False):
        super().__init__(symbol, 3);
        '''
        self.symbol = symbol
        self.root = None
        self.thingsToEval = []
        '''
        self.use_ab_prune = uabp;

    def get_move(self, board):
        if(not self.use_ab_prune):
            return super().get_move(board);
        currentDepth = 0
        self.root = Node(None, board, None)
        self.thingsToEval.append(self.root)
        evalLen = 1
        alpha = None
        beta = None
        while (evalLen > 0):
            workingNode = self.thingsToEval[evalLen - 1]
            validMoves = self.getValidMoves(workingNode)
            if(len(workingNode.children) < len(validMoves) and currentDepth < self.evalDepth):
                self.genBoard(workingNode, validMoves)
                currentDepth += 1
            elif(len(validMoves) > 0 or currentDepth >= self.evalDepth or not workingNode.board.game_continues()):
                self.thingsToEval.remove(workingNode)
                '''
                if alpha is not None and beta is not None:
                    alpha_beta_array = self.evalNode(workingNode, alpha, beta)
                    alpha = alpha_beta_array[0]
                    beta = alpha_beta_array[1]
                elif alpha is None and beta is not None:
                    alpha_beta_array = self.evalNode(workingNode, None, beta)
                    alpha = alpha_beta_array[0]
                    beta = alpha_beta_array[1]
                elif alpha is not None and beta is None:
                    alpha_beta_array = self.evalNode(workingNode, alpha, None)
                    alpha = alpha_beta_array[0]
                    beta = alpha_beta_array[1]
                else:
                    alpha_beta_array = self.evalNode(workingNode, None, None)
                    alpha = alpha_beta_array[0]
                    beta = alpha_beta_array[1]
                '''
                alpha_beta_array = self.evalNode(workingNode, alpha, beta)
                alpha = alpha_beta_array[0]
                beta = alpha_beta_array[1]

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

    def evalNode(self, node, alpha=None, beta=None):
        if(len(node.children) == 0):
            score = node.board.calc_scores()[self.symbol]
            node.eval = score
            return [alpha, beta]
        else:
            if(node.max):
                max_array = self.max(node.children, alpha, beta)
                node.eval = max_array[0]
                alpha = max_array[1]
                beta = max_array[2]
                return [alpha, beta]
            else:
                min_array = self.min(node.children, alpha, beta)
                node.eval = min_array[0]
                alpha = min_array[1]
                beta = min_array[2]
                return [alpha, beta]

    def max(self, children, alpha, beta):
        max = 0
        for c in children:
            if beta is not None:
                if c.eval >= beta:
                    max = c.eval
                    break
            if alpha is not None:
                if c.eval > alpha:
                    alpha = c.eval
            if(c.eval > max):
                max = c.eval
        if alpha is None:
            alpha = max
        return [max, alpha, beta]

    def min(self, children, alpha, beta):
        min = 64
        for c in children:
            if alpha is not None:
                if c.eval <= alpha:
                    min = c.eval
                    break
            if beta is not None:
                if c.eval < beta:
                    beta = c.eval
            if(c.eval < min):
                min = c.eval
        if beta is None:
            beta = min
        return [min, alpha, beta]

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