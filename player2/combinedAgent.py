from player2 import orion_player, lookup_table, alpha_beta_pruning, quiescent_search, transposition_table


class CombinedAgent(orion_player.oMinimaxComputerPlayer):
    def __init__(self, symbol):
        super().__init__(symbol, 3, True)
        self.ab_prune = alpha_beta_pruning.AlphaBetaPruning(symbol, False)
        self.lookup_table = lookup_table.lookup_table(symbol, True)
        self.quiet_search = quiescent_search.QuiescentSearch(symbol, True)
        #self.t_table = t_table_player.tTableMinimaxComputerPlayer(symbol, 3, True, True)
        self.t_table = transposition_table.TranspositionTable(symbol, 3, True, True)
        self.originalBoard = None

    def get_move(self, board):
        self.originalBoard = board
        currentDepth = 0
        if self.t_table.useTTable:
            self.root = transposition_table.Node(None, board, None, self.t_table.movesTaken * 2)
        else:
            self.root = orion_player.Node(None, board, None)
        if self.t_table.useTTable and board in self.t_table.tTable and self.t_table.tTable[board][1] >= self.evalDepth + self.root.depth:
            self.root.eval = self.t_table.tTable[board]
        self.thingsToEval.append(self.root)
        evalLen = 1
        alpha = None
        beta = None
        while evalLen > 0:
            workingNode = self.thingsToEval[evalLen - 1]
            validMoves = self.getValidMoves(workingNode)
            if len(workingNode.children) < len(validMoves) and currentDepth < self.evalDepth:
                if self.t_table.useTTable:
                    self.t_table.genBoard(workingNode, validMoves,currentDepth)
                else:
                    self.genBoard(workingNode, validMoves)

                currentDepth += 1
            elif (len(validMoves) > 0 or currentDepth >= self.evalDepth or not workingNode.board.game_continues()):
                self.thingsToEval.remove(workingNode)
                if not self.ab_prune.use_ab_prune:
                    super().evalNode(workingNode)
                else:
                    alpha_beta_array = self.evalNode(workingNode, alpha, beta, currentDepth)
                    alpha = alpha_beta_array[0]
                    beta = alpha_beta_array[1]
                # print("Node evaluated @ depth " + str(currentDepth) + ": " + str(workingNode.eval))
                if(self.quiet_search.use_quiet_search):
                    self.quiet_search.originalBoard = board
                    if (currentDepth >= self.evalDepth and self.quiet_search.check_quiet_iterative(workingNode)):
                        # print("Node not quiet")
                        workingNode.eval = self.quiet_search.quiet_search(workingNode.board, 3, workingNode.board.get_opponent_symbol(self.quiet_searchderive_symbol(workingNode.max,workingNode.board)));
                currentDepth -= 1
            else:
                workingNode.max = not workingNode.max
            evalLen = len(self.thingsToEval)
        for c in self.root.children:
            if (c.eval == self.root.eval):
                return c.move
        return -1, -1

    def evalNode(self, node, alpha=None, beta=None, depth=None):
        if(len(node.children) == 0):
            score = node.board.calc_scores()[self.symbol]
            node.eval = score
            return [alpha, beta]
        else:
            if(node.max):
                if (self.ab_prune.use_ab_prune):
                    max_array = self.ab_prune.max(node.children, alpha, beta)
                    node.eval = max_array[0]
                    alpha = max_array[1]
                    beta = max_array[2]

                if(self.lookup_table.use_lookup_table and node.parent is not None):
                    node.eval += self.lookup_table.valueBoardEight[node.move[0]][node.move[1]]

                return [alpha, beta]
            else:
                if(self.ab_prune.use_ab_prune):
                    min_array = self.ab_prune.min(node.children, alpha, beta)
                    node.eval = min_array[0]
                    alpha = min_array[1]
                    beta = min_array[2]

                if (self.lookup_table.use_lookup_table and node.parent is not None):
                    node.eval -= self.lookup_table.valueBoardEight[node.move[0]][node.move[1]]
            if self.t_table.useTTable and depth is not None:
                self.t_table.permutateBoardState(node, depth, node.eval)

                return [alpha, beta]