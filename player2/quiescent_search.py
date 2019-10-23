#Made by Eugene Kuznetsov
import copy
from player2.orion_player import oMinimaxComputerPlayer, Node

class QuiescentSearch(oMinimaxComputerPlayer):
    def __init__(self, symbol, uqs=False):
        super().__init__(symbol, 3)
        self.use_quiet_search = uqs
        self.originalBoard = None;

    def get_move(self, board):
        if(not self.use_quiet_search):
            return super().get_move(board);
        self.originalBoard = board;
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
                if (currentDepth >= self.evalDepth and self.check_quiet_iterative(workingNode)):
                    #print("Node not quiet")
                    workingNode.eval = self.quiet_search(workingNode.board, 3, workingNode.board.get_opponent_symbol(self.derive_symbol(workingNode.max, workingNode.board)));
                #print("Node evaluated @ depth " + str(currentDepth) + ": " + str(workingNode.eval))
                currentDepth -= 1
            else:
                workingNode.max = not workingNode.max
            evalLen = len(self.thingsToEval)
        for c in self.root.children:
            if(c.eval == self.root.eval):
                return c.move
        return -1, -1

    def derive_symbol(self, max, board):
        if max:
            return self.symbol;
        else:
            return board.get_opponent_symbol(self.symbol);

    def check_quiet_iterative(self, workingNode):
        cur_symbol = self.derive_symbol(workingNode.max, workingNode.board)
        first_node_eval = self.originalBoard.calc_scores();
        cur_node_eval = workingNode.board.calc_scores();
        if(cur_node_eval[cur_symbol] > cur_node_eval[workingNode.board.get_opponent_symbol(cur_symbol)]) != (first_node_eval[cur_symbol] > first_node_eval[workingNode.board.get_opponent_symbol(cur_symbol)]):
            return True
        return False

    def check_quiet_recursive(self, board, cur_symbol):
        first_node_eval = self.originalBoard.calc_scores();
        cur_node_eval = board.calc_scores();
        if (cur_node_eval[cur_symbol] > cur_node_eval[board.get_opponent_symbol(cur_symbol)]) != (first_node_eval[cur_symbol] > first_node_eval[board.get_opponent_symbol(cur_symbol)]):
            return True
        return False

    def quiet_search(self, board, depth, cur_symbol, last_move=None):
        emuboard = copy.deepcopy(board)
        if last_move != None:
            emuboard.make_move(emuboard.get_opponent_symbol(cur_symbol), last_move)

        if self.check_quiet_recursive(emuboard, cur_symbol) or depth <= 0 or len(emuboard.calc_valid_moves(cur_symbol)) <= 0:
            return board.calc_scores()[cur_symbol];

        eval = None
        valid_moves = emuboard.calc_valid_moves(cur_symbol);
        for move in valid_moves:
            min_max_val = self.quiet_search(emuboard, depth - 1, emuboard.get_opponent_symbol(cur_symbol), move)
            if eval is None:
                eval = min_max_val
            elif min_max_val is not None:
                if cur_symbol == self.symbol:
                    eval = self.min_max_eval(eval, min_max_val, False)
                elif cur_symbol != self.symbol:
                    eval = self.min_max_eval(eval, min_max_val, True)
        return eval

    def min_max_eval(self, val1, val2, get_max):
        if get_max:
            if(val1 > val2):
                return val1
            else:
                return val2
        elif not get_max:
            if (val1 < val2):
                return val1
            else:
                return val2