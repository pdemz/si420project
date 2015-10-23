import sys

rack = [['*' for x in range(7)] for x in range(6)]

currPlayer = "R"
column = 0
game = "incomplete"

#Recursive function, checks the pieces
def helper(direction, color, row, column, total):
    if total == 4 and color == "B":
        print("Black is the winner! Congratulations!")
        sys.exit(0)
       
    if total == 4 and color == "R":
        print("Red is the winner! Congratulations!")
        sys.exit(0)

    #We went out of bounds, bail and bail hard
    if row < 0 or row > 5 or column < 0 or column > 6:
        return 0

    #There were not four consecutive pieces
    if rack[row][column] != color:
        return 0

    #Keep trucking - check which direction to go in starting with
    #north and going clockwise numerically
    if direction == 0:
        row += 1
    elif direction == 1:
        row += 1
        column += 1
    elif direction == 2:
        column += 1
    elif direction == 3:
        row -= 1
        column += 1
    elif direction == 4:
        row -= 1
    elif direction == 5:
        row -= 1
        column -= 1
    elif direction == 6:
        column -= 1
    elif direction == 7:
        row += 1
        column -= 1
    
    helper(direction, color, row, column, total+1)


#Check if a win or draw occurred
def winOrDrawCheck():
    resultRed = 0
    resultBlack = 0
    draw = True
    for row in range (0,6):
        for column in range (0, 7):
            for x in range (0, 8):
                if rack[row][column] == '*':
                    draw = False

                resultBlack = helper(x, "B", row, column, 0)
                resultRed = helper(x, "R", row, column, 0)

                if resultBlack == 1 or resultRed == 1:
                    print("yup")
                    return "complete"

    if draw == True:
        print("Draw.")
        sys.exit(0)
    else:
        return "incomplete"

#Make a move
def makeMove(column):
    column -= 1
    for x in range(5, -1, -1):
        if rack[x][column] == '*':
            rack[x][column] = currPlayer
            return

#Print out the board and change whose turn it is
def printBoard():
    print("")
    for x in range(0,6):
        row = ""
        for y in range(0,7):
            row += rack[x][y]
        print(row)
    print("1234567")
    print("")

#Continue the game until the user enters a 'q'
printBoard()
while(game == "incomplete"):
    if currPlayer == "R":
        column = input("Black player, what's your move?\n")
        currPlayer = "B"
    else:
        column = input("Red player, what's your move?\n")
        currPlayer = "R"
    while column < 1 or column > 7 or not isinstance(column, int):
        column = input("Invalid move, try again.\n")
    
    while rack[0][column-1] != '*':
        column = input("Invalid move, try again.\n")
    
    makeMove(column)
    printBoard()
    game = winOrDrawCheck()
    

    
