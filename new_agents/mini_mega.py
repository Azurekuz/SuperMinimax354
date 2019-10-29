# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import copy, heapq
from reversi_board import ReversiBoard, _drawBoard
from base_player import MinimaxComputerPlayer
from datetime import datetime, timedelta

class MiniMega:

    def __init__(self, symbol, timeLimit):
        self.symbol = symbol
        self.root = None
        self.timeLimit = timedelta(seconds=(timeLimit - .06))
        self.tileCount = 0
        self.thingsToSearch = []

    def get_move(self, board):
        startTime = datetime.now()                  #Get the time the function started at
        tileCount = self.countPieces(board._board)

        if self.root is not None and tileCount > self.tileCount:  # Find out which move the opponents took and make that the root
            foundMove = False
            for c in self.root.children:
                if c.board._board == board._board:
                    self.root = c
                    foundMove = True
                    break
        if self.root is None or tileCount < self.tileCount or not foundMove:  # If we can't for some reason make a new root
            print("Generate new root")
            self.root = Node(None, board, None)
            self.root.eval = -110
            self.root.depth = self.countPieces(self.root.board._board)
            heapq.heappush(self.thingsToSearch, [self.root.depth - self.root.stability / 2, self.root])

        self.tileCount = tileCount
        self.root.parent = None                     #Cut off root from all the other nodes checked so the old root can be deleted

        self.trimQueue()        #Trim the self.thingsToSearch queue down to only items that are still relevant


        while self.thingsToSearch:               #Start main search loop
            if datetime.now() - startTime > self.timeLimit:     #If almost out of time, stop searching and return current best
                if self.root is not None and self.root.moveToBestChoice is not None:
                    move = self.root.moveToBestChoice  # If we've run out of time, return the best choice we found
                    self.root = self.root.bestChoice
                    print(self.root.validMoves)
                    print(move)
                    print(self.root.eval)
                    print(self.root.heuristicDepth - self.root.depth)
                    print(datetime.now() - startTime)
                else:
                    move = (-1, -1)
                return move

            workingNode = heapq.heappop(self.thingsToSearch)[1]
            self.evalAndGetMoves(workingNode)           #Get workingnode and calculate moves it could make, as well as evaluating it

            if len(workingNode.validMoves) > 0:             #If it has moves it could make, add them to the tree
                for move in workingNode.validMoves:
                    self.genBoard(workingNode, move)

            elif workingNode.board.game_continues():        #If it doesn't have moves it could make, swap it to the other player and do the above
                workingNode.max = not workingNode.max
                self.evalAndGetMoves(workingNode)
                for move in workingNode.validMoves:
                    self.genBoard(workingNode, move)

        if self.root is not None and self.root.moveToBestChoice is not None:
            move = self.root.moveToBestChoice                   #If we've calculated to the end of all possible branches, return the best choice
        else:
            move = (-1,-1)
        self.root = self.root.bestChoice
        return move



    def evalAndGetMoves(self, node):
        board = node.board._board
        size = len(board)
        diagSize = size * 2 - 5
        maxFlips = 0
        depthScaling = ((64 - node.depth)/64) + 1
        score = 0
        if node.max:
            mySymbol = self.symbol
            opponentSymbol = node.board.get_opponent_symbol(self.symbol)
        else:
            mySymbol = node.board.get_opponent_symbol(self.symbol)
            opponentSymbol = self.symbol
        validMoves = []

        vertCurrent = [None] * size
        horCurrent = [None] * size
        diagTLCurrent = [None] * diagSize
        diagTRCurrent = [None] * diagSize

        vertPreviousLoc = [(-1,-1)] * size
        horPreviousLoc = [(-1,-1)] * size
        diagTLPreviousLoc = [(-1,-1)] * diagSize
        diagTRPreviousLoc = [(-1,-1)] * diagSize

        vertPrevious = [None] * size
        horPrevious = [None] * size
        diagTLPrevious = [None] * diagSize
        diagTRPrevious = [None] * diagSize

        for j in range(0, size):
            for i in range(0, size):                                #Iterate through the entire board
                workingVal = board[i][j]

                ######################################################################Start eval section

                evalScore = 1

                if i == 0 or i == size - 1:
                    evalScore *= depthScaling
                if j == 0 or j == size - 1:
                    evalScore *= depthScaling
                if workingVal == self.symbol:
                    score += evalScore
                elif workingVal == node.board.get_opponent_symbol(self.symbol):
                    score -= evalScore

                ######################################################################Start vertical valid move check section

                if workingVal != vertCurrent[i]:                    #If the value on this tile is different from what we've been getting...
                    if (vertPrevious[i] == mySymbol and workingVal == ' ') or (vertPrevious[i] == ' ' and workingVal == mySymbol):  #And only one value on either end is a ''
                        if vertPrevious[i] == ' ':                      #If the tile on the previous end is the open space
                            if vertPreviousLoc[i] not in validMoves:
                                validMoves.append(vertPreviousLoc[i])   #Append the coords of that space to the list of valid moves
                                if vertPreviousLoc[i][1] - j - 1 > maxFlips:    #Check if this is the highest number of flips, if so update it
                                    maxFlips = j - vertPreviousLoc[i][1] - 1
                        else:                                       #If it's not the tile on the previous end it must be the one here
                            if (i,j) not in validMoves:
                                validMoves.append((i,j))                #Therefore append those coords instead
                                if vertPreviousLoc[i][1] - j - 1 > maxFlips:    #Check if this is the highest number of flips, if so update it
                                    maxFlips = j - vertPreviousLoc[i][1] - 1
                    vertPrevious[i] = vertCurrent[i]                #Either way make sure we update the recorded tile to the currently seen ones
                    vertCurrent[i] = workingVal                     #And update the currently seen one to the one we just saw
                    vertPreviousLoc[i] = (i,j - 1)                  #Also make sure to update the location of the new end tile to be the location of the currently seen tile, AKA one space behind us

                ######################################################################Start horizontal valid move check section

                if workingVal != horCurrent[j]:                     #If the value on this tile is different from what we've been getting...
                    if (horPrevious[j] == mySymbol and workingVal == ' ') or (horPrevious[j] == ' ' and workingVal == mySymbol):   #And only one value on either end is a ''
                        if horPrevious[j] == ' ':                       #If the tile on the previous end is the open space
                            if horPreviousLoc[i] not in validMoves:
                                validMoves.append(horPreviousLoc[j])    #Append the coords of that space to the list of valid moves
                                if horPreviousLoc[j][1] - i - 1 > maxFlips:    #Check if this is the highest number of flips, if so update it
                                    maxFlips = i - horPreviousLoc[j][1] - 1
                        else:                                       #If it's not the tile on the previous end it must be the one here
                            if (i,j) not in validMoves:
                                validMoves.append((i,j))                #Therefore append those coords instead
                                if i - horPreviousLoc[j][1] - 1 > maxFlips:    #Check if this is the highest number of flips, if so update it
                                    maxFlips = horPreviousLoc[j][1] - i - 1
                    horPrevious[j] = horCurrent[j]                  #Either way make sure we update the recorded tile to the currently seen ones
                    horCurrent[j] = workingVal                      #And update the currently seen one to the one we just saw
                    horPreviousLoc[j] = (i - 1,j)                   #Also make sure to update the location of the new end tile to be the location of the currently seen tile, AKA one space behind us

                ######################################################################Start diagonal top left valid move check section

                tlDiagIndex = i - j + size - 2
                if tlDiagIndex >= 0 and tlDiagIndex < diagSize:
                    if workingVal != diagTLCurrent[tlDiagIndex]:                            #If the value on this tile is different from what we've been getting...
                        if (diagTLPrevious[tlDiagIndex] == mySymbol and workingVal == ' ') or (diagTLPrevious[tlDiagIndex] == ' ' and workingVal == mySymbol):                    #And only one value on either end is a ''
                            if diagTLPrevious[tlDiagIndex] == ' ':                                        #If the tile on the previous end is the open space
                                if diagTLPreviousLoc[tlDiagIndex] not in validMoves:
                                    validMoves.append(diagTLPreviousLoc[tlDiagIndex])           #Append the coords of that space to the list of valid moves
                                    if (i + j - diagTLPreviousLoc[tlDiagIndex][0] - diagTLPreviousLoc[tlDiagIndex][0]) // 2 > maxFlips: #Check if this is the highest number of flips, if so update it
                                        maxFlips = (i + j - diagTLPreviousLoc[tlDiagIndex][0] - diagTLPreviousLoc[tlDiagIndex][0]) // 2
                            else:                                                           #If it's not the tile on the previous end it must be the one here
                                if (i, j) not in validMoves:
                                    validMoves.append((i,j))                                    #Therefore append those coords instead
                                    if (i + j - diagTLPreviousLoc[tlDiagIndex][0] - diagTLPreviousLoc[tlDiagIndex][0]) // 2 > maxFlips: #Check if this is the highest number of flips, if so update it
                                        maxFlips = (i + j - diagTLPreviousLoc[tlDiagIndex][0] - diagTLPreviousLoc[tlDiagIndex][0]) // 2
                        diagTLPrevious[tlDiagIndex] = diagTLCurrent[tlDiagIndex]            #Either way make sure we update the recorded tile to the currently seen ones
                        diagTLCurrent[tlDiagIndex] = workingVal                             #And update the currently seen one to the one we just saw
                        diagTLPreviousLoc[tlDiagIndex] = (i - 1,j - 1)                                #Also make sure to update the location of the new end tile to be the location of the currently seen tile, AKA one space behind us

                ######################################################################Start diagonal top right valid move check section

                trDiagIndex = i + j - 2
                if trDiagIndex >= 0 and trDiagIndex < diagSize:
                    if workingVal != diagTRCurrent[trDiagIndex]:  # If the value on this tile is different from what we've been getting...
                        if (diagTRPrevious[trDiagIndex] == mySymbol and workingVal == ' ') or (diagTRPrevious[trDiagIndex] == ' ' and workingVal == mySymbol):  # And only one value on either end is a ''
                            if diagTRPrevious[trDiagIndex] == ' ':  # If the tile on the previous end is the open space
                                if diagTRPreviousLoc[trDiagIndex] not in validMoves:
                                    validMoves.append(diagTRPreviousLoc[trDiagIndex])  # Append the coords of that space to the list of valid moves
                                    if (j + diagTRPreviousLoc[trDiagIndex][0] - i - diagTRPreviousLoc[trDiagIndex][0]) // 2 > maxFlips:  # Check if this is the highest number of flips, if so update it
                                        maxFlips = (j + diagTRPreviousLoc[trDiagIndex][0] - i - diagTRPreviousLoc[trDiagIndex][0]) // 2
                            else:  # If it's not the tile on the previous end it must be the one here
                                if (i, j) not in validMoves:
                                    validMoves.append((i, j))  # Therefore append those coords instead
                                    if (j + diagTRPreviousLoc[trDiagIndex][0] - i - diagTRPreviousLoc[trDiagIndex][0]) // 2 > maxFlips:  # Check if this is the highest number of flips, if so update it
                                        maxFlips = (j + diagTRPreviousLoc[trDiagIndex][0] - i - diagTRPreviousLoc[trDiagIndex][0]) // 2
                        diagTRPrevious[trDiagIndex] = diagTRCurrent[trDiagIndex]  # Either way make sure we update the recorded tile to the currently seen ones
                        diagTRCurrent[trDiagIndex] = workingVal  # And update the currently seen one to the one we just saw
                        diagTRPreviousLoc[trDiagIndex] = (i + 1,j - 1)  # Also make sure to update the location of the new end tile to be the location of the currently seen tile, AKA one space behind us

        node.stability = maxFlips
        node.eval = score * ((4 - node.stability) / 5 + 1)
        #_drawBoard(node.board._board)
        #print(validMoves)
        node.validMoves = validMoves
        if node.parent is not None:
            self.evalUp(node.parent)






    def genBoard(self, node, move):                     #Generate a new board and set it as the node's child based on the given move
        newBoard = copy.deepcopy(node.board)
        if node.max:
            newBoard.make_move(self.symbol, move)       #If max node, make a move
        else:
            opponentSymbol = node.board.get_opponent_symbol(self.symbol)    #If not, opponent makes a move
            newBoard.make_move(opponentSymbol, move)
        newNode = Node(node, newBoard, move)
        heapq.heappush(self.thingsToSearch, [newNode.depth - node.stability / 2, newNode])                #Add to list of things to eval
        node.children.append(newNode)

    def evalUp(self, node):                                     #The function to trickle the score upwards when we change it
        if(node.max):
            self.max(node)
        else:
            self.min(node)
        node.heuristicDepth = node.children[0].heuristicDepth
        if node.parent is not None:
            self.evalUp(node.parent)

    def max(self, node):
        node.eval = -110
        for c in node.children:
            if c.eval is not None and c.eval > node.eval:
                node.eval = c.eval
                node.bestChoice = c
                node.moveToBestChoice = c.move

    def min(self, node):
        node.eval = 110
        for c in node.children:
            if c.eval is not None and c.eval < node.eval:
                node.eval = c.eval
                node.bestChoice = c
                node.moveToBestChoice = c.move

    def isRelevant(self, node):
        if node == self.root:
            return True
        elif node.parent is None:
            return False
        else:
            return self.isRelevant(node.parent)

    def trimQueue(self):
        newPQ = []
        for i in self.thingsToSearch:
            if self.isRelevant(i[1]):
                heapq.heappush(newPQ, i)
        self.thingsToSearch = newPQ

    def countPieces(self, board):
        count = 0
        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                tile = board[i][j]
                if tile == "X" or tile == "O":
                    count += 1
        return count


    def __name__ (self):
        return "Minimega Player"


class Node:

    def __init__(self, parent, board, move):
        self.parent = parent
        if not parent is None:
            self.max = not parent.max
            self.depth = parent.depth + 1
        else:
            self.max = True
            self.depth = 0
        self.children = []
        self.eval = None
        self.stability = 1
        self.board = board
        self.validMoves = None
        self.bestChoice = None
        self.moveToBestChoice = None
        self.move = move
        self.heuristicDepth = self.depth

    def __lt__(self, other):
        if self.depth < other.depth:
            return True
        else:
            return False

    def __le__(self, other):
        if self.depth <= other.depth:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.depth > other.depth:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.depth >= other.depth:
            return True
        else:
            return False

