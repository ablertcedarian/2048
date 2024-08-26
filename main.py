from gameLogic import gameBoard

game2048 = gameBoard()

game2048.printBoard()
# game2048.flipBoardHorizontal()
# game2048.flipBoardVertical()
# game2048.rotateBoardClockwise90()
# game2048.printBoard()
while game2048.live:
    direction = input("Pick a direction:")
    game2048.playerMove(direction)