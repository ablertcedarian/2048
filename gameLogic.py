import random
import numpy as np
from copy import copy, deepcopy

class gameBoard:
    def __init__(self):
        self.board = np.array([[0,0,0,0] for _ in range(4)])
        self.moveCount = 0
        self.maxScore = 0
        self.live = True

        self.addRandom()
        self.addRandom()

    def addRandom(self):
        empties = [(x,y) for x in range(4) for y in range(4) if self.board[x][y] == 0]
        emptyCount = len(empties)
        chosenForInsert = random.randint(0, emptyCount - 1)

        numberInsertRandom = random.randint(0, 3)
        numberInsert = 2 if numberInsertRandom <= 2 else 4

        locationInsertX = empties[chosenForInsert][0]
        locationInsertY = empties[chosenForInsert][1]
        self.board[locationInsertX][locationInsertY] = numberInsert

    def rotateBoardCCW90(self, times=1):
        boardCopy = copy(self.board)
        self.board = np.rot90(np.array(boardCopy), k=times)

    def flipBoardHorizontal(self):
        self.board = [list(reversed(row)) for row in self.board]

    def flipBoardVertical(self):
        self.board = list(reversed(self.board))

    def move(self, direction):
        print(f"Processing {direction}")
        match direction:
            case "left":
                flip = True
                vertical = False
            case "right":
                flip = False
                vertical = False
            case "up":
                flip = True
                vertical = True
            case "down":
                flip = False
                vertical = True

        # print("     Rotating for move!")
        # self.printBoard()
        if flip and vertical:
            self.flipBoardVertical()
        elif flip:
            self.flipBoardHorizontal()

        # self.printBoard()
        if vertical:
            self.rotateBoardCCW90()

        # self.printBoard()

        # print("     Initiate move!")
        for i, row in enumerate(self.board):
            # print(i, row)
            resultRow = []
            lastNonZero = -1
            for elem in row[::-1]:
                if elem != 0:
                    # print(elem, resultRow, lastNonZero)
                    if lastNonZero == elem:
                        resultRow.pop()
                        resultRow.append(elem * 2)
                        lastNonZero = -1
                        if elem * 2 > self.maxScore:
                            self.maxScore = elem * 2
                    else:
                        resultRow.append(elem)
                        lastNonZero = elem

            while len(resultRow) < 4:
                resultRow.append(0)
            self.board[i] = list(reversed(resultRow))

        # self.printBoard()

        # print("     Rotating back")
        if vertical:
            self.rotateBoardCCW90(times=3)

        # self.printBoard()
        if flip and vertical:
            self.flipBoardVertical()
        elif flip:
            self.flipBoardHorizontal()

        # self.printBoard()

    def checkLive(self):
        # Check for empty spaces
        for row in range(4):
            for col in range(4):
                if self.board[row][col] == 0:
                    return

        # Check for vertical neighbors of same value
        for col in range(4):
            last = -1
            for row in range(4):
                if self.board[row][col] == last:
                    return
                last = self.board[row][col]

        # Check for horizontal neighbors of same value
        for row in range(4):
            last = -1
            for col in range(4):
                if self.board[row][col] == last:
                    return
                last = self.board[row][col]

        self.live = False

    def areBoardsDiff(self, board1, board2):
        for row in range(4):
            for col in range(4):
                if board1[row][col] != board2[row][col]:
                    return True
        return False

    def playerMove(self, direction):
        prevState = deepcopy(self.board)
        self.move(direction)

        if self.areBoardsDiff(self.board, prevState):
            print("     Detected board difference!")
            self.addRandom()

        self.printBoard()

        self.checkLive()

        if not self.live:
            print(f"Game over, high score: {self.maxScore} over {self.moveCount} moves")

        self.moveCount += 1


    def printBoard(self):
        print("---------------------------")
        for row in self.board:
            rowString = "|".join([str(elem).ljust(4).rjust(6) for elem in row])
            print(rowString)
        print("---------------------------")