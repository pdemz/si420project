import sys
import copy

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
        return

    #There were not four consecutive pieces
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
def makeMove(theRack, column):
    column -= 1
    for x in range(5, -1, -1):
        if theRack[x][column] == '*':
            theRack[x][column] = currPlayer
            return

#Print out the board and change whose turn it is
def printRack(theRack):
    print("")
    for x in range(0,6):
        row = ""
        for y in range(0,7):
            row += theRack[x][y]
        print(row)
    print("1234567")
    print("")

class rackNode():
    #a hypothetical rack for tree building purposes
    futureRack = copy.deepcopy(rack)
    children = []
    depth = 0
    retVal = 0
    alpha = -1000
    beta = 1000

    def explode(self):

        #For 7 children
        for index in range(0,7):
            #If there is room for a move to be made
            if self.futureRack[0][len(self.children)] == '*':
                #Create a new node representing that move
                self.children.append(rackNode())
                self.children[index].futureRack = copy.deepcopy(rack)
                makeMove(self.children[index].futureRack, index+1)
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
    if(aNode.depth + 1 == globalDepth):
        return evaluate(aNode)

    #For all 7 children
    for ii in range(0,7):
        #If there is a node at this index then recurse
        if(aNode.children[ii] != None):
            value = minimax(aNode.children[ii])
            #Max Node
            if(aNode.depth % 2 == 0):
                #prune
                if(value >= aNode.beta):
                    return aNode.beta
                    #update alpha
                    if(value > aNode.alpha):
                        aNode.alpha = value
                        
            #Min Node
            else:
            #prune
                if(value <= aNode.alpha):
                    return aNode.beta
                #updata beta
                if(value < aNode.beta):
                    aNode.beta = value

#Evaluation function
def evaluate(parent):

    retVal = 0
    
    #For each child
    for index in range(0,7):

        #If the child is not null
        if parent.children[index] != None:

            for row in range (0,6):
                for column in range (0, 7):
                    #For the 8 directions
                    for x in range (0, 8):
                        #If there is a black piece here
                        if parent.children[index].futureRack[row][column] == "B":
                              value += evalHelper(parent.futureRack, row, column, 0, 0, "B", x)

        #Return max or min of children, depending
        if(parent.depth % 2 == 0): 
            if(value > retVal):
                retVal = value
        else:
            if(value < retVal):
                retVal = value

    return retVal

 
          

def evalHelper(evalRack, row, col, total, stars, color, direction ):
    
    #Winner! Return a big score
    if total == 4 and color == "B":
        return 888

    #Reached boundary, return ignore if cannot get 4
    if row < 0 or row > 5 or col < 0 or col > 6:
        if(stars + total >= 4):
            return total * total 
        else:
            return 0

    #Dead end at red, return
    if evalRack[row][col] == "R":
        if(stars + total >= 4):
            return total * total
        else:
            return 0

  #Count empty spaces for potential connect-fours
    if evalRack[row][col] == '*':
        color = "STAR"
        evalHelper(evalRack, row, col, total, stars + 1, color, direction )
  

    #Reached a gap in the star count
    if color == "STAR" and evalRack[row][column] == "B":
        if(stars + total >= 4):
            return total * total
        else:
            return 0

    #Keep trucking - check which direction to go in starting with
    #north and going clockwise numerically
    if direction == 0:
        row += 1
    elif direction == 1:
        row += 1
        col += 1
    elif direction == 2:
        col += 1
    elif direction == 3:
        row -= 1
        col += 1
    elif direction == 4:
        row -= 1
    elif direction == 5:
        row -= 1
        col -= 1
    elif direction == 6:
        col -= 1
    elif direction == 7:
        row += 1
        col -= 1

    #No obstacles yet, keep counting chips
    evalHelper(evalRack, row, col, total+1, stars, color, direction )


            

#Create a function that looks 4 moves ahead
#This requires making all (up to) 7 possible moves
#then doing the 7 moves after that and so forth.
#Use a modified rackCheck algorithm that determines if a move is legal

#Recursively call, adding boards to a tree. Add 7 child boards
#to the board. If less than 7 can be added (because column is full)
#child gets null

#Continue the game until the user enters a 'q'
printRack(rack)
itera = 0

while(game == "incomplete"):
    if currPlayer == "R":
        column = input("Black player, what's your move?\n")
        currPlayer = "B"
    else:
        column = input("Red player, what's your move?\n")
        currPlayer = "R"

    #Do not progress until a valid input is provided
    while column < 1 or column > 7 or not isinstance(column, int) or rack[0][column-1] != '*':
        column = input("Invalid move, try again.\n")
    
    #Make selected move, print the rack, and check for a win or draw
    makeMove(rack, column)
    printRack(rack)
    game = winOrDrawCheck()

    if itera >= 4:
        theNewRack = rackNode()
        theNewRack.explode()
        theNumber = evaluate(theNewRack)
        print("The evaluation was")
        print(theNumber)

    itera += 1
