import sys
import copy

rack = [['*' for x in range(7)] for x in range(6)]
globalDepth = int(sys.argv[1])
currPlayer = "R"
column = 0
game = "incomplete"


#Copies a list

def unshared_copy(inList):
    if isinstance(inList, list):
        return list( map(unshared_copy, inList) )
    return inList            

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
        return

    #There were not four consecutive pieces, the color changed
    if rack[row][column] != color:
        return

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
    
    #Assume a draw until we see an empty spot
    draw = True

    #For every spot in which there is a piece, check if there was a victory
    for row in range (0,6):
        for column in range (0, 7):
            #For the 8 directions
            for x in range (0, 8):
                if rack[row][column] == '*':
                    draw = False
                else:    
                    resultBlack = helper(x, "B", row, column, 0)
                    resultRed = helper(x, "R", row, column, 0)

    if draw == True:
        print("Draw.")
        sys.exit(0)
    else:
        return "incomplete"

#Make a move
def makeMove(theRack, column, color):
    column -= 1
    for x in range(5, -1, -1):
        if theRack[x][column] == '*':
            theRack[x][column] = color
            return

#Print out the rack
def printRack(theRack):
    print("")
    for x in range(0,6):
        row = ""
        for y in range(0,7):
            row += theRack[x][y]
        print(row)
    print("1234567")
    print("")

class rackNode:
    def __init__(self, newRack):
        #a hypothetical rack for tree building purposes
        self.futureRack = copy.deepcopy(newRack)
        self.children = []
        self.depth = 0
        self.retVal = 0
        self.prodigalSon = 0 #index of max or min child, depending on which kind of node it is
        self.alpha = -100000
        self.beta = 100000

    def explode(self):
        #For 7 children
        for index in range(0,7):
            #If there is room for a move to be made
            if self.futureRack[0][index] == '*':
                #Create a new node representing that move
                self.children.append(rackNode(self.futureRack))
                if(self.depth % 2 == 0):
                    makeMove(self.children[index].futureRack, index+1, "B")
                else:
                     makeMove(self.children[index].futureRack, index+1, "R")
                #Increment it's depth to 1 more than it's parent's
                self.children[index].depth = self.depth + 1
                #Initialize alpha and beta to that of parent node's
                self.children[index].alpha = self.alpha
                self.children[index].beta = self.beta
              
            else:
                #Otherwise, if a move cannot be made, put a null object
                #in the index
                self.children.append(None)


def minimax(aNode):
    #First expand the node
    aNode.explode()
    
    #Evaluate leaves if we are at maxDepth
    if(aNode.depth + 1 >= globalDepth):
        num = evaluate(aNode) #O(7)
        return num

    #For all 7 children
    for ii in range(0,7):
        #If there is a node at this index then recurse
        if(aNode.children[ii] != None):
            aNode.children[ii].alpha = aNode.alpha
            aNode.children[ii].beta = aNode.beta
            value = minimax(aNode.children[ii])
            
            #Max Node
            if(aNode.depth % 2 == 0):
                #prune
                if(value >= aNode.beta):
                    return aNode.beta
                    #update alpha
                if(value > aNode.alpha):
                    aNode.prodigalSon = ii
                    aNode.alpha = value
                        
            #Min Node
            else:
            #prune
                if(value <= aNode.alpha):
                    return aNode.alpha
                #updata beta
                if(value < aNode.beta):
                    aNode.prodigalSon = ii
                    aNode.beta = value
    if(aNode.depth % 2 == 0):
        return aNode.alpha
    else:
        return aNode.beta

#Evaluation function
def evaluate(parent):
    
    if(parent.depth % 2 == 0):  #Max Node
        retVal = parent.alpha
    else:
        retVal = parent.beta
    #For each child
    for index in range(0,7):
        #If the child is not null
        if parent.children[index] != None:
            value = 0
            #Check each space in the rack
            for row in range (0,6):
                for column in range (0, 7):
                    #For the 8 directions
                   # if parent.children[index].futureRack[row][column] != '*':
                    for x in range (0, 8):
                        #If there is a black piece here see if there are any rows coming from it
                        #and add that to the rack's score
                        if parent.children[index].futureRack[row][column] == "B":
                            value += int(evalHelper(parent.children[index].futureRack, row, column, 0, 0, "B", "B", "R", x))
                           # value += evalTwo(parent.children[index].futureRack, row, column, "B")
                        elif parent.children[index].futureRack[row][column] == "R":
                            value -= int(evalHelper(parent.children[index].futureRack, row, column, 0, 0, "R", "R", "B", x))
                           # value -= evalTwo(parent.children[index].futureRack, row, column, "R")
        #Return max or min of children, depending
            if(parent.depth % 2 == 0):  #Max Node
                if(value > retVal):
                    parent.prodigalSon = index
                    parent.alpha = value
                    retVal = value
            else:
                if(value < retVal):
                    parent.prodigalSon = index
                    parent.beta = value
                    retVal = value

    return retVal
 
          

def evalHelper(evalRack, row, column, total, stars, currColor, initColor, oppColor, direction ):

    if total == 4 and currColor == initColor:
        return 1000
       
    #We went out of bounds or hit a red piece
    if row < 0 or row > 5 or column < 0 or column > 6 or evalRack[row][column] == oppColor or (currColor == "STAR" and evalRack[row][column] == initColor):
        if(stars + total > 3):
            return total*total
        else:
            return 0

    if evalRack[row][column] == '*':
        currColor = "STAR";

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

    if currColor == "STAR":
        return evalHelper(evalRack, row, column, total, stars+1, currColor, initColor, oppColor, direction)
    elif currColor == initColor:
        return evalHelper(evalRack, row, column, total+1, stars, currColor, initColor, oppColor, direction)

def evalTwo(aRack, row, col, color):
    total = 0
    stars = 0
    initRow = row
    initCol = col
    line = 0
    #check straight up
    if row >= 3:
        while row < 6 and row >= 0 and col < 7 and col >= 0 and aRack[row][col] == color:
            row -= 1
            line += 1
            if line == 4:
                total += 700
                break
        if line < 4:
            row = initRow + line
            while row < 6 and row >= 0 and col < 7 and col >= 0 and aRack[row][col] == '*':
                row -= 1
                stars += 1
                if line + stars == 4:
                    total += line * line * line
                    break
            

    row = initRow
    col = initCol
    stars = 0
    line = 0

    #check right
    if col < 4:
        while row < 6 and row >= 0 and col < 7 and col >= 0 and aRack[row][col] == color:
            col += 1
            line += 1
            if line == 4:
                total += 700
                break
        if line < 4:
            col = initCol + line
            while row < 6 and row >= 0 and col < 7 and col >= 0 and aRack[row][col] == '*':
                col += 1
                stars += 1
                if line + stars == 4:
                    total += line * line * line
                    break
    
    row = initRow
    col = initCol
    stars = 0
    line = 0

    #check right diag
    if row >= 3 and col <= 3:
        while row < 6 and row >= 0 and col < 7 and col >= 0 and aRack[row][col] == color:
            col += 1
            row -= 1
            line += 1
            if line == 4:
                total += 500
                break
        if line < 4:
            row = initRow - line
            col = initCol + line
            while row < 6 and row >= 0 and col < 7 and col >= 0 and aRack[row][col] == '*':
                row -= 1
                col += 1
                stars += 1
                if line + stars == 4:
                    total += line * line * line
                    break

    row = initRow
    col = initCol
    stars = 0
    line = 0

    #check left diag
    if row >= 3 and col >= 3:
        while row < 6 and row >= 0 and col < 7 and col >= 0 and aRack[row][col] == color:
            col += 1
            line += 1
            if line == 4:
                total += 500
                break
        if line < 4:
            row = initRow + line
            while row < 6 and row >= 0 and col < 7 and col >= 0 and aRack[row][col] == '*':
                row -= 1
                col -= 1
                stars += 1
                if line + stars == 4:
                    total += line * line * line
                    break
    
    return total
    

#Continue the game until the user enters a 'q'

printRack(rack)
i = 0

firstPlayer = raw_input("h or c goes first?\n")
if firstPlayer == 'h':
    currPlayer = "B"
elif firstPlayer == 'c':
    currPlayer = "R"
while(game == "incomplete"):
    if currPlayer == "R":
        print("Computer turn\n")
        currPlayer = "B"
        nodeWrapper = None
        nodeWrapper = rackNode(rack)
        minimax(nodeWrapper)
        column = nodeWrapper.prodigalSon+1
        makeMove(rack,column, "B")
    else:
        column = input("Human, what's your move?\n")
        currPlayer = "R"
        #Do not progress until a valid input is provided
        while column < 1 or column > 7 or not isinstance(column, int) or rack[0][column-1] != '*':
            column = input("Invalid move, try again.\n")
        makeMove(rack, column, "R")
    #Make selected move, print the rack, and check for a win or draw
    printRack(rack)
    game = winOrDrawCheck()
