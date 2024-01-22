############################################################
# Tic-Tac-Toe
# Written by Jason Bere
# For Cis 3700 A2
# February 2022
############################################################

from itertools import count
from os import stat
from pickle import FALSE
from re import I, X
import sys
from time import time
import random

class State:

    def __init__(self, boardSize, playerStart, searchType, utility, depth):
        self.boardSize = boardSize
        self.playerStart = playerStart
        self.searchType = searchType
        self.utility = utility
        self.depth = depth
        self.turnNumber = 1
        self.board = [[' ',' ',' ',' ',' '], [' ',' ',' ',' ',' '], [' ',' ',' ',' ',' '], [' ',' ',' ',' ',' '], [' ',' ',' ',' ',' ']]

        #for i in range(0, boardSize -1):
        #    for j in range(0, boardSize-1):
        #        self.board[i][j] = '#'

    def printBoard(state):
        max = state.boardSize
        for j in range(0, max):
            for i in range(0, max):
                print(state.board[i][j], end ='')
                if(i < max -1):
                    print("|", end= '')
            
            print("")
            if(j < max -1):
                for k in range(0, max):
                    print("-", end ='')
                    if (k < max-1):
                        print("+", end ='')
            print("")

################################################
# Command line input parsers
################################################

# gets player move
def getPlayerInput(state):
    validPos = 0
    x = 0
    y = 0

    while validPos < 1:
        print("Please enter x value: ", end='')
        x = int(input())
        print("Please enter y value: ", end='')
        y = int(input())

        if (x >= state.boardSize or x < 0) or (y >= state.boardSize or y < 0):
            print("Invalid Position")
        elif state.board[x][y] != ' ':
            print("Position already occupied")
        else:
            validPos = 1
    
    return (x, y)

# returns whether user is player 1 or 2
def readPlayerState(argv):
    playerState = 1
    
    for i in range(1, len(argv), 2):
        if(argv[i-1] == '-p'):
            
            if (argv[i] == "1"): 
                playerState = 1
            elif(argv[i] == "2"):
                playerState = 2

    return playerState

# returns board size
def readBoardSize(argv):
    boardSize = 3
    for i in range(1, len(argv), 2):
        if (argv[i-1] == "-n"):
            if (argv[i] == '3'):
                boardSize = 3
            elif(argv[i] == '4'):
                boardSize = 4
            elif(argv[i] == '5'):
                boardSize = 5
    
    return boardSize

# returns search type 
def readSearchType(argv):
    searchType = getPlayerInput
    for i in range(1, len(argv), 2):
        if (argv[i-1] == "-s"):
            if (argv[i] == "MiniMax"):
                searchType = minimaxSearch
            elif(argv[i] == "AlphaBeta"):
                searchType = alphaBetaSearch
            else:
                searchType = getPlayerInput

    return searchType

# returns utility function
def readUtility(argv):
    utility = randomUtility
    for i in range(1, len(argv), 2):
        if (argv[i-1] == "-u"):
            if (argv[i] == "Util1"):
                utility = basicUtility
            elif(argv[i] == "Util2"):
                utility = advancedUtility
            else:
                utility = randomUtility

    return utility

# returns depth
def readDepth(argv):
    depth = 1
    for i in range(1, len(argv), 2):
        if (argv[i-1] == "-d"):
            if (int(argv[i]) > 0) and (int(argv[i]) <= 10):
                depth = int(argv[i])
    
    return depth

# count remaining moves
def countRemainingMoves(state):
    counter = 0
    for i in range(0, state.boardSize):
        for j in range(0, state.boardSize):
            if state.board[j][i] == ' ':
                counter += 1
    return counter

##########################################
# functions for checking for win condition 
##########################################

# checks for horizontal line of char
def checkHorizontalWin(state, char):
    counter = 0
    for i in range(0, state.boardSize):
        counter = 0
        for j in range(0, state.boardSize):
            if(state.board[j][i] == char):
                counter += 1
        if counter == state.boardSize:
            return 1
    return 0

# checks for vertical line of char
def checkVerticalWin(state, char):
    counter = 0
    for i in range(0, state.boardSize):
        counter = 0
        for j in range(0, state.boardSize):
            if(state.board[i][j] == char):
                counter += 1
        if counter == state.boardSize:
            return 1
    return 0

# check if diagonal win state has been encountered
def checkDiagonalWin(state, char):
    
    counter = 0
    #top left to bottom right
    for i in range(0, state.boardSize):
        if state.board[i][i] == char:
            counter += 1
    
    if counter == state.boardSize:
        return 1

    
    counter = 0
    max = state.boardSize -1
    #top right to bottom left
    for i in range(0, state.boardSize):
        if state.board[i][max -i] == char:
            counter += 1

    if counter == state.boardSize:
        return 1

    
    return 0

# check if square win state has been encountered
def checkSquareWin(state, char):
    for i in range(0, state.boardSize -1):
        for j in range(0, state.boardSize -1):
            if(state.board[j][i] == char) and (state.board[j+1][i] == char) and (state.board[j][i+1] == char) and (state.board[j+1][i+1] == char):
                return 1
    return 0

# check if diamond win state has been encountered
def checkDiamondWin(state, char):
    for i in range(1, state.boardSize -1):
        for j in range(1, state.boardSize -1):
            if (state.board[j-1][i] == char) and (state.board[j+1][i] == char) and (state.board[j][i-1] == char) and (state.board[j][i+1] == char):
                return 1
    return 0

# check if plus win state has been encountered
def checkPlusWin(state, char):
    for i in range(1, state.boardSize -1):
        for j in range(1, state.boardSize -1):
            if (state.board[j][i] == char) and (state.board[j-1][i] == char) and (state.board[j+1][i] == char) and (state.board[j][i-1] == char) and (state.board[j][i+1] == char):
                return 1
    return 0   

# check if an L win state has been encountered
def checkLWin(state, char):
    for i in range(1, state.boardSize -1):
        for j in range(1, state.boardSize -1):
            # L shape
            if (state.board[j-1][i-1] == char) and (state.board[j-1][i] == char) and (state.board[j-1][i+1] == char) and (state.board[j][i+1] == char) and (state.board[j+1][i+1] == char):
                return 1
            # backwards L shape
            if (state.board[j-1][i+1] == char) and (state.board[j][i+1] == char) and (state.board[j+1][i+1] == char) and (state.board[j+1][i] == char) and (state.board[j+1][i-1] == char):
                return 1
            # Upside down L
            if (state.board[j-1][i+1] == char) and (state.board[j-1][i] == char) and (state.board[j-1][i-1] == char) and (state.board[j][i-1] == char) and (state.board[j+1][i-1] == char):
                return 1 
            # backwards upside down L
            if (state.board[j-1][i-1] == char) and (state.board[j][i-1] == char) and (state.board[j+1][i-1] == char) and (state.board[j+1][i] == char) and (state.board[j+1][i+1] == char):
                return 1
    return 0 

# checks if a win state has been encountered
def checkWinCondition(state, char):
    counter = 0
    if (state.boardSize == 3):
        # size 3 board
        counter += checkHorizontalWin(state, char)
        counter += checkVerticalWin(state, char)
        counter += checkDiagonalWin(state, char)

    elif(state.boardSize == 4):
        # size 4 board
        counter += checkHorizontalWin(state, char)
        counter += checkVerticalWin(state, char)
        counter += checkDiagonalWin(state, char)
        counter += checkSquareWin(state, char)
        counter += checkDiamondWin(state, char)

    elif(state.boardSize == 5):
        # size 5 board
        counter += checkHorizontalWin(state, char)
        counter += checkVerticalWin(state, char)
        counter += checkDiagonalWin(state, char)
        counter += checkPlusWin(state, char)
        counter += checkLWin(state, char)

    if counter > 0:
        return 1
    
    return 0

# check if tie has been encountered
def checkTie(state):
    for i in range(0, state.boardSize):
        for j in range(0, state.boardSize):
            if state.board[j][i] == ' ':
                return 0
    return 1

################################################
# Helper functions for advanced utility function
################################################

# count potential horizontal win conditions
def countHorizontals(state, char):
    count = 0
    tempCount = 0

    for i in range(0, state.boardSize):
        tempCount = 0
        for j in range(0, state.boardSize):
            if state.board[j][i] == char:
                tempCount += 1
            elif (state.board[j][i] != char) and (state.board[j][i] != ' '):
                tempCount = 0
                break
        count += tempCount

    return count

# count potential vertical win conditions
def countVerticals(state, char):
    count = 0
    tempCount = 0

    for i in range(0, state.boardSize):
        tempCount = 0
        for j in range(0, state.boardSize):
            if state.board[i][j] == char:
                tempCount += 1
            elif (state.board[i][j] != char) and (state.board[i][j] != ' '):
                tempCount = 0
                break
        count += tempCount

    return count

# count potential diagonal win conditions
def countDiagonals(state, char):
    tempCount = 0
    count = 0

    for i in range(0, state.boardSize):
        if state.board[i][i] == char:
            tempCount +=1
        elif (state.board[i][i] != char) and (state.board[i][i] != ' '):
            tempCount = 0
            break
        
    count += tempCount

    tempCount = 0

    for i in range(0, state.boardSize):
        if state.board[i][state.boardSize - (i+1)] == char:
            tempCount += 1
        elif (state.board[i][state.boardSize - (i+1)] != char) and (state.board[i][state.boardSize - (i+1)] != ' '):
            tempCount = 0
            break
    
    count += tempCount

    return count

# count potential square win conditions
def countSquares(state, char):
    count = 0
    opposite = 0

    for i in range(0, state.boardSize -1):
        for j in range(0, state.boardSize -1):
            #top left
            if state.board[i][j] == char:
                count += 1
            elif state.board[i][j] != ' ':
                opposite += 1
            #top right
            if state.board[i+1][j] == char:
                count += 1
            elif state.board[i+1][j] != ' ':
                opposite += 1
            #bottom left
            if state.board[i][j+1] == char:
                count += 1
            elif state.board[i][j+1] != ' ':
                opposite += 1
            #bottom right
            if state.board[i+1][j+1] == char:
                count += 1
            elif state.board[i+1][j+1] != ' ':
                opposite += 1

    if opposite == 0:
        return count

    return 0

# counts potential diamond win conditions
def countDiamonds(state, char):
    count = 0
    opposite = 0

    for i in range(1, state.boardSize -1):
        for j in range(1, state.boardSize -1):
            #left
            if state.board[i-1][j] == char:
                count +=1
            elif state.board[i-1][j] != ' ':
                opposite += 1
            #right
            if state.board[i+1][j] == char:
                count +=1
            elif state.board[i+1][j] != ' ':
                opposite += 1
            #up
            if state.board[i][j-1] == char:
                count +=1
            elif state.board[i][j-1] != ' ':
                opposite += 1
            #down
            if state.board[i][j+1] == char:
                count +=1
            elif state.board[i][j+1] != ' ':
                opposite += 1

    if opposite == 0:
        return count
    
    return 0

# counts potential plus win conditions
def countPluses(state, char):
    count = 0
    opposite = 0

    for i in range(1, state.boardSize -1):
        for j in range(1, state.boardSize -1):
            #centre
            if state.board[i][j] == char:
                count +=1
            elif state.board[i][j] != ' ':
                opposite += 1
            #left
            if state.board[i-1][j] == char:
                count +=1
            elif state.board[i-1][j] != ' ':
                opposite += 1
            #right
            if state.board[i+1][j] == char:
                count +=1
            elif state.board[i+1][j] != ' ':
                opposite += 1
            #up
            if state.board[i][j-1] == char:
                count +=1
            elif state.board[i][j-1] != ' ':
                opposite += 1
            #down
            if state.board[i][j+1] == char:
                count +=1
            elif state.board[i][j+1] != ' ':
                opposite += 1

    if opposite == 0:
        return count
    
    return 0

# helper function for countLs
def countLPos1(state, x, y, char):
    counter = 0
    opposite = 0
    #top left
    if state.board[x-1][y-1] == char:
        counter += 1
    elif state.board[x-1][y-1] != ' ':
        opposite += 1
    #centre left
    if state.board[x-1][y] == char:
        counter += 1
    elif state.board[x-1][y] != ' ':
        opposite += 1
    #bottom left
    if state.board[x-1][y+1] == char:
        counter += 1
    elif state.board[x-1][y+1] != ' ':
        opposite += 1
    #bottom centre
    if state.board[x][y+1] == char:
        counter += 1
    elif state.board[x][y+1] != ' ':
        opposite += 1
    #bottom right
    if state.board[x+1][y+1] == char:
        counter += 1
    elif state.board[x+1][y+1] != ' ':
        opposite += 1

    if opposite == 0:
        return counter

    return 0

# helper function for countLs
def countLPos2(state, x, y, char):
    counter = 0
    opposite = 0
    #top right
    if state.board[x+1][y-1] == char:
        counter += 1
    elif state.board[x+1][y-1] != ' ':
        opposite += 1
    #centre right
    if state.board[x+1][y] == char:
        counter += 1
    elif state.board[x+1][y] != ' ':
        opposite += 1
    #bottom right
    if state.board[x+1][y+1] == char:
        counter += 1
    elif state.board[x+1][y+1] != ' ':
        opposite += 1
    #bottom centre
    if state.board[x][y+1] == char:
        counter += 1
    elif state.board[x][y+1] != ' ':
        opposite += 1
    #bottom right
    if state.board[x-1][y+1] == char:
        counter += 1
    elif state.board[x-1][y+1] != ' ':
        opposite += 1

    if opposite == 0:
        return counter
        
    return 0

# helper function for countLs
def countLPos3(state, x, y, char):

    counter = 0
    opposite = 0
    #top left
    if state.board[x-1][y-1] == char:
        counter += 1
    elif state.board[x-1][y-1] != ' ':
        opposite += 1
    #top centre
    if state.board[x][y-1] == char:
        counter += 1
    elif state.board[x][y-1] != ' ':
        opposite += 1
    #top right
    if state.board[x+1][y-1] == char:
        counter += 1
    elif state.board[x+1][y-1] != ' ':
        opposite += 1
    #centre right
    if state.board[x+1][y] == char:
        counter += 1
    elif state.board[x+1][y] != ' ':
        opposite += 1
    #bottom right
    if state.board[x+1][y+1] == char:
        counter += 1
    elif state.board[x+1][y+1] != ' ':
        opposite += 1

    if opposite == 0:
        return counter
        
    return 0

# helper function for countLs
def countLPos4(state, x, y, char):
    counter = 0
    opposite = 0
    
    #top right
    if state.board[x+1][y-1] == char:
        counter += 1
    elif state.board[x+1][y-1] != ' ':
        opposite += 1
    #top centre
    if state.board[x][y-1] == char:
        counter += 1
    elif state.board[x][y-1] != ' ':
        opposite += 1
    #top left
    if state.board[x-1][y-1] == char:
        counter += 1
    elif state.board[x-1][y-1] != ' ':
        opposite += 1
    #centre left
    if state.board[x-1][y] == char:
        counter += 1
    elif state.board[x-1][y] != ' ':
        opposite += 1
    #bottom left
    if state.board[x-1][y+1] == char:
        counter += 1
    elif state.board[x-1][y+1] != ' ':
        opposite += 1
    
    if opposite == 0:
        return counter
        
    return 0

# counts potential L win conditions
def countLs(state, char):
    counter = 0
    for i in range(1, state.boardSize -1):
        for j in range(1, state.boardSize -1):
            counter += countLPos1(state, j, i, char)
            counter += countLPos2(state, j, i, char)
            counter += countLPos3(state, j, i, char)
            counter += countLPos4(state, j, i, char)

    return counter

# counts all potential win conditions
def countPotentialWins(state, char):
    counter = 0
    if state.boardSize == 3:
        counter += countHorizontals(state, char)
        counter += countVerticals(state, char)
        counter += countDiagonals(state, char)
    elif state.boardSize == 4:
        counter += countHorizontals(state, char)
        counter += countVerticals(state, char)
        counter += countDiagonals(state, char)
        counter += countSquares(state, char)
        counter += countDiamonds(state, char)
    elif state.boardSize == 5:
        counter += countHorizontals(state, char)
        counter += countVerticals(state, char)
        counter += countDiagonals(state, char)
        counter += countPluses(state, char)
        counter += countLs(state, char)
    return counter

################################################
# Utility functions
################################################

# basic utility function
def basicUtility(state, char):
    
    #state.printBoard()
    #print("Basic utility char =", char, end = '')

    if checkWinCondition(state, char) == 1:
        #print("v = 1")
        return 1
    
    if char == 'X':
        if checkWinCondition(state, 'O') == 1:
            #print("v = -1")
            return -1
    else:
        if checkWinCondition(state, 'X') == 1:
            #print("v = -1")
            return -1
    
    #print(" v = 0")

    return 0

# advanced utility function
def advancedUtility(state, char):
    
    remMoves = countRemainingMoves(state) 
    posCount = countPotentialWins(state, char)
    negCount = 0
    count = 0
    utility = 0

    if checkWinCondition(state, char) == 1:
        utility += 1000
    elif char == 'X':
        if checkWinCondition(state, 'O') == 1:
            utility = utility - 1000
    else:
        if checkWinCondition(state, 'X') == 1:
            utility = utility - 1000
            
    if char =='X':
        negCount = countPotentialWins(state, 'O')
    else:
        negCount = countPotentialWins(state, 'X')
    
    count = posCount - negCount

    utility += count
    if remMoves == 0:
        remMoves = 1

    utility = utility * remMoves

    #print("Utility 2 returned: ", utility)
    #state.printBoard()
    #print("")

    return utility

# returns a random utility value
def randomUtility(state, char):
    return random.random()

################################################
# MiniMax search functions
################################################

# maximum value function
def maxValue(state, char, curDepth):
    #print("max value")
    # check if in terminal state
    if curDepth == state.depth or checkWinCondition(state, 'X') == 1 or checkWinCondition(state, 'O') == 1 or checkTie(state) == 1:
        #print("depth =", curDepth)
        return (-1, -1, state.utility(state, char), 1, curDepth)

    v = float("-inf")
    n = 0
    c = 0
    tempV = 0.0
    tempX = 0
    tempY = 0
    tempN = 0
    tempC = 0
    x = 0
    y = 0


    for i in range(0, state.boardSize):
        for j in range(0, state.boardSize):
            if state.board[j][i] == ' ':
                state.board[j][i] = char
                tempX, tempY, tempV, tempN, tempC = minValue(state, char, curDepth+1)
                state.board[j][i] = ' '

                n += tempN

                if tempV > v:
                        v = tempV
                        x = j
                        y = i
                
                if tempC > c:
                    c = tempC

    #print("max value returns x=", x,", y=", y, "v=", v, "n=",n )
    return (x, y, v, n, c)

# minimum value function
def minValue(state, char, curDepth):
    #print("min value")
    # check if in terminal state
    if curDepth == state.depth or checkWinCondition(state, 'X') == 1 or checkWinCondition(state, 'O') == 1 or checkTie(state) == 1:
        #print("depth =", curDepth)
        return (-1, -1, state.utility(state, char), 1, curDepth)

    v = float("inf")
    n = 0
    x = 0
    y = 0
    c = 0
    tempV = 0.0
    tempX = 0
    tempY = 0
    tempN = 0
    tempC = 0

   
    if(char == 'X'):
        for i in range(0, state.boardSize):
            for j in range(0, state.boardSize):
                if state.board[j][i] == ' ':

                    state.board[j][i] = 'O'
                    tempX, tempY, tempV, tempN, tempC = maxValue(state, char, curDepth+1)
                    state.board[j][i] = ' '

                    n += tempN

                    if tempV < v:
                        v = tempV
                        x = j
                        y = i
                    
                    if tempC > c:
                        c = tempC
    else:
        for i in range(0, state.boardSize):
            for j in range(0, state.boardSize):
                if state.board[j][i] == ' ':
                    state.board[j][i] = 'X'
                    tempX, tempY, tempV, tempN, tempC = maxValue(state, char, curDepth+1)
                    state.board[j][i] = ' '
                    
                    n += tempN
                    
                    if tempV < v:
                        v = tempV
                        x = j
                        y = i
                    
                    if tempC > c:
                        c = tempC
    
    #print("min value returns x=", x,", y=", y, "v=", v, "n=",n )
    return (x, y, v, n, c)

# minimax search function
def minimaxSearch(state):
    print("MiniMax Search ...")
    char = ''
    x = 0
    y = 0
    v = 0
    n = 0
    t1 = 0.0
    t2 = 0.0
    if state.playerStart == 1:
        char = 'O'
    else:
        char = 'X'

    t1 = time()
    x, y, v, n, c = maxValue(state, char, 0)
    t2 = time()

    print("Mini-Max took ", t2-t1, "seconds to explore ", n, "nodes, and returned a value of ", v, "for coordinates", x,y, " at a max depth of", c)

    return (x, y)


#############################
# Alpha Beta Search Functions
#############################

# alpha beta search
def alphaBetaSearch(state):
    print("Alpha Beta...")
    char = ''
    if state.playerStart == 1:
        char = 'O'
    else:
        char = 'X'
    
    x = 0
    y = 0
    v = 0
    n = 0
    c = 0
    t1 = 0.0
    t2 = 0.0

    t1 = time()
    x, y, v, n, c = abMaxValue(state, char, 0, float("-inf"), float("inf"))
    t2 = time()
    print("Alpha-Beta took ", t2-t1, "seconds to explore ", n, "nodes, and returned a value of ", v, "for coordinates", x,y, "with a max depth of", c)
    
    return (x, y)

# alpha beta Max value function
def abMaxValue(state, char, curDepth, alpha, beta):
    # check if in terminal state
    if curDepth == state.depth or checkWinCondition(state, 'X') == 1 or checkWinCondition(state, 'O') == 1 or checkTie(state) == 1:
        #print("depth =", curDepth)
        return (-1, -1, state.utility(state, char), 1, curDepth)

    v = float("-inf")
    x = 0
    y = 0
    n = 0
    c = 0
    tempV = 0.0
    tempX = 0
    tempY = 0
    tempN = 0
    tempC = 0

    for i in range(0, state.boardSize):
        for j in range(0, state.boardSize):
            if state.board[j][i] == ' ':

                if char == 'X':
                    state.board[j][i] = 'X'
                else:
                    state.board[j][i] = 'O'
                tempX, tempY, tempV, tempN, c = abMinValue(state, char, curDepth+1, alpha, beta)    
                state.board[j][i] = ' '

                n += tempN

                if tempV > v:
                    x = j
                    y = i
                    v = tempV
                    alpha = max(alpha, v)

                if c < tempC:
                    c = tempC

                if v >= beta:
                    return (x, y, v, n, c)

    return (x, y, v, n, c)

def abMinValue(state, char, curDepth, alpha, beta):
    # check if in terminal state
    if curDepth == state.depth or checkWinCondition(state, 'X') == 1 or checkWinCondition(state, 'O') == 1 or checkTie(state) == 1:
        #print("depth =", curDepth)
        return (-1, -1, state.utility(state, char), 1, curDepth)

    v = float("inf")
    x = 0
    y = 0
    n = 0
    c = 0
    tempV = 0.0
    tempX = 0
    tempY = 0
    tempN = 0
    tempC = 0

    
    for i in range(0, state.boardSize):
        for j in range(0, state.boardSize):
            if state.board[j][i] == ' ':

                if char == 'X':
                    state.board[j][i] = 'O'
                else:
                    state.board[j][i] = 'X'
                tempX, tempY, tempV, tempN, c = abMaxValue(state, char, curDepth+1, alpha, beta)    
                state.board[j][i] = ' '

                n += tempN

                if tempV < v:
                    x = j
                    y = i
                    v = tempV
                    beta = min(beta, v)

                if c < tempC:
                    c = tempC

                if v <= alpha:
                    return (x, y, v, n, c)

    return (x, y, v, n, c)

###########
# runs game
###########

# run tictactoe game
def runGame(state):
    x = 0
    y = 0
    for i in range(0, state.boardSize*state.boardSize):
        state.printBoard()
        #x, y = getPlayerInput(state)
        
        if(state.playerStart == 1):
            if(i%2 == 0):
                x, y = getPlayerInput(state)
            else:
                x, y = state.searchType(state)
        elif(state.playerStart == 2):
            if(i%2 == 1):
                x, y = state.searchType(state)
            else:
                x, y = getPlayerInput(state)


        if(i % 2 == 0):
            print("set (",x , ",", y, ") to X")
            state.board[x][y] = 'X'
            if checkWinCondition(state, 'X') == 1:
                print("X wins")
                state.printBoard()
                return
        else:
            print("set (",x , ",", y, ") to O")
            state.board[x][y] = 'O'
            if checkWinCondition(state, 'O') == 1:
                print("O wins")
                state.printBoard()
                return
    
    state.printBoard()
    print("Tie")
    return

# main function 
def main(argv):
    #print("hello world")

    n = len(argv)
    for i in range(0, n):
        print(argv[i], end = " ")
    print("\n")

    playerStart = readPlayerState(argv)
    boardSize = readBoardSize(argv)
    search = readSearchType(argv)
    util = readUtility(argv)
    depth = readDepth(argv)
    print(playerStart, " ", boardSize, " ", search, " ", util, " ", depth)


    state = State(boardSize, playerStart, search, util, depth)

    #state.printBoard()
    #state.board[0][0] = "X"
    #state.printBoard()

    #getPlayerInput(state)
    runGame(state)

    return
    


if __name__ == "__main__":
    main(sys.argv[1:])