# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 18:45:45 2019
@author: marcc
"""
import pygame
import random
from QTable import Qtable

# this will be used as the object inside the matix to hold all of the data in each position
class contents:
    def __init__(self):

        # list of weights for the drop off model
        # initalizing as 0 to represent has not visited
        self.dropoffweights = [0, 0, 0, 0]  # order is north, south, east, west

        # list of weights for the pickup model
        # initalizing as "-" to represent has not visited
        self.pickupweighrs = [0, 0, 0, 0]  # order is north, south, east, west

        # identifyers if the block is special
        self.dropoff = False
        self.pickup = False

    def __str__(self):
        if (self.isdropoff()):
            return "2"
        elif (self.ispickup()):
            return "1"
        else:
            return "0"

    # toggle dropoff
    def tdropoff(self):
        if (self.dropoff == True):
            self.dropoff = False
        else:
            self.dropoff = True

    # toggle pickup
    def tpickup(self):
        if (self.pickup == True):
            self.pickup = False
        else:
            self.pickup = True

    # returns if it is drop off
    def isdropoff(self):
        return self.dropoff

    # returns if it is pickup
    def ispickup(self):
        return self.pickup

    # using d as dropoff and p as pickup for function names
    # using N as North, S as South, E as East, W as West for function names

    # dropoffweight functions
    def dsetN(self, value):  # give a new value to set north to
        self.dropoffweights[0] = value

    def dsetS(self, value):  # give a new value to set south to
        self.dropoffweights[1] = value

    def dsetE(self, value):  # give a new value to set east to
        self.dropoffweights[2] = value

    def dsetW(self, value):  # give a new value to set west to
        self.dropoffweights[3] = value

    # used to increment and decrement weights a certain ammount

    # incrementing functions
    def dincN(self, value):  # give a new value to increment north to
        self.dropoffweights[0] += value

    def dincS(self, value):  # give a new value to increment south to
        self.dropoffweights[1] += value

    def dincE(self, value):  # give a new value to increment east to
        self.dropoffweights[2] += value

    def dincW(self, value):  # give a new value to increment west to
        self.dropoffweights[3] += value

    # decrementing functions
    def ddecN(self, value):  # give a new value to increment north to
        self.dropoffweights[0] -= value

    def ddecS(self, value):  # give a new value to increment south to
        self.dropoffweights[1] -= value

    def ddecE(self, value):  # give a new value to increment east to
        self.dropoffweights[2] -= value

    def ddecW(self, value):  # give a new value to increment west to
        self.dropoffweights[3] -= value

    # pickup weight functions
    def psetN(self, value):  # give a new value to set north to
        self.pickupweights[0] = value

    def psetS(self, value):  # give a new value to set south to
        self.pickupweights[1] = value

    def psetE(self, value):  # give a new value to set east to
        self.pickupweights[2] = value

    def psetW(self, value):  # give a new value to set west to
        self.pickupweights[3] = value

    # used to increment and decrement weights a certain ammount

    # incrementing functions
    def pincN(self, value):  # give a new value to increment north to
        self.pickupweights[0] += value

    def pincS(self, value):  # give a new value to increment south to
        self.pickupweights[1] += value

    def pincE(self, value):  # give a new value to increment east to
        self.pickupweights[2] += value

    def pincW(self, value):  # give a new value to increment west to
        self.pickupweights[3] += value

    # decrementing functions
    def pdecN(self, value):  # give a new value to increment north to
        self.pickupweights[0] -= value

    def pdecS(self, value):  # give a new value to increment south to
        self.pickupweights[1] -= value

    def pdecE(self, value):  # give a new value to increment east to
        self.pickupweights[2] -= value

    def pdecW(self, value):  # give a new value to increment west to
        self.pickupweights[3] -= value


# used to check if cordinate is out of bounds aka a wall
def isvalidcord(mat, x, y):  # pass in the matrix to ensure correctness
    # if col cord is within range
    if (x >= 0 and x < 5):
        # if row cord is within range
        if (y >= 0 and y < 5):
            return True
    return False


# used to "move" and determine the weights in the matix
class avatar:
    def __init__(self):
        # cordinates
        self.x = 0
        self.y = 4
        # carrying block
        self.carrying = False

    def __str__(self):
        return ("(" + str(self.x) + "," + str(self.y) + ") carrying = " + str(self.iscarrying()))

    # returns x cordinate
    def getX(self):
        return self.x

    # returns y cordinate
    def getY(self):
        return self.y

    # "moves" avatar north ###NEEDS SOME FORM OF CHECK TO SEE IF IT IS A VALID POSITION!!!! as in isvalidcord(matrix,x,y)
    def moveN(self):
        self.y += 1

    ##"moves" avatar south ###NEEDS SOME FORM OF CHECK TO SEE IF IT IS A VALID POSITION!!!!
    def moveS(self):
        self.y -= 1

    # "moves" avatar east ###NEEDS SOME FORM OF CHECK TO SEE IF IT IS A VALID POSITION!!!!
    def moveE(self):
        self.x += 1

    # "moves" avatar west ###NEEDS SOME FORM OF CHECK TO SEE IF IT IS A VALID POSITION!!!!
    def moveW(self):
        self.x -= 1

    # use when starts carrying block
    def startcarrying(self):
        self.carrying = True

    # use when drops block off
    def stopcarrying(self):
        self.carrying = False

    # use to check if it is currently carrying anything
    def iscarrying(self):
        return self.carrying

    def aplop(self):  # determine applicable operators

        op = []  # will return array of numbers such that
        # 0 = North
        # 1 = South
        # 2 = East
        # 3 = West
        # 4 = Pickup
        # 5 = Dropoff

        if self.x == 0:  # cannot move west
            if self.y == 0:
                op.extend([1, 2])
            elif self.y == 4:
                op.extend([0, 2])
            else:
                op.extend([0, 1, 2])

        elif self.x == 4:  # cannot move east
            if self.y == 0:
                op.extend([1, 3])
            elif self.y == 4:
                op.extend([0, 3])
            else:
                op.extend([0, 1, 3])

        elif self.y == 0:  # cannot move north
            if self.x == 0:
                op.extend([1, 2])
            elif self.x == 4:
                op.extend([1, 3])
            else:
                op.extend([1, 2, 3])

        elif self.y == 4:  # cannot move south
            if self.x == 0:
                op.extend([0, 2])
            elif self.x == 4:
                op.extend([0, 3])
            else:
                op.extend([0, 2, 3])

        else:  # somewhere in the middle
            op.extend([0, 1, 2, 3])

        if (self.iscarrying()):  # in dropoff location
            if (self.x == 4 and self.y == 1) or (self.x == 2 and self.y == 4) or (
                    self.x == 0 and self.y == 4):
                op.extend([5])

        else:  # in pickup location
            if (self.x == 0 and self.y == 0) or (self.x == 2 and self.y == 2) or (
                    self.x == 4 and self.y == 4):
                op.extend([4])

        return op

    def randomPolicy(self, matrix, isApplicable):
        while 1:
            i = random.randrange(0, 100)
            x_old = self.x
            y_old = self.y
            if self.carrying is False and matrix.getdataat(x_old, y_old).pickup and isApplicable == True:
                self.carrying = True
                return [self.x, self.y, 4, x_old, y_old]
            if self.carrying is True and matrix.getdataat(x_old, y_old).dropoff and isApplicable == True:
                self.carrying = False
                return [self.x, self.y, 5, x_old, y_old]
            if i < 25 and isvalidcord(matrix, x_old+1, y_old):
                self.moveE()
                return [x_old, y_old, 2, self.x,self.y]
            if i < 50 and i >= 25 and isvalidcord(matrix, x_old, y_old+1):
                self.moveN()
                return [x_old, y_old, 0, self.x,self.y]
            if i < 75 and i >= 50 and isvalidcord(matrix, x_old-1, y_old):
                self.moveW()
                return [x_old, y_old, 3, self.x,self.y]
            if i < 100 and i >= 75 and isvalidcord(matrix, x_old, y_old-1):
                self.moveS()
                return [x_old, y_old, 1, self.x,self.y]

    def greedyPolicy(self, matrix, isApplicable,  table, table2):
        applOp = aplop(self)
        #print(applOp)
        if self.carrying:
            qvalMatrix = table
        else:
            qvalMatrix = table2
        while 1:
            x_old = self.x
            y_old = self.y
            if self.carrying is False and matrix.getdataat(x_old, y_old).pickup and isApplicable == True:
                self.carrying = True
                return [self.x, self.y, 4, x_old, y_old]
            if self.carrying is True and matrix.getdataat(x_old, y_old).dropoff and isApplicable == True:
                self.carrying = False
                return [self.x, self.y, 5, x_old, y_old]

            maxQ = -10000
            checkQ = -10001
            anyEqual = []
            for i in range(len(applOp)):
                if i == 0:
                    # 0 = North
                    # 1 = South
                    # 2 = East
                    # 3 = West
                    if applOp[0] == 0:
                        maxQ = qvalMatrix.get(x_old, y_old, 0)
                    elif applOp[0] == 1:
                        maxQ = qvalMatrix.get(x_old, y_old, 1)
                    elif applOp[0] == 2:
                        maxQ = qvalMatrix.get(x_old, y_old, 2)
                    elif applOp[0] == 3:
                        maxQ = qvalMatrix.get(x_old, y_old, 3)

                    anyEqual.extend([applOp[0]])

                else:
                    if applOp[i] == 0:
                        checkQ = qvalMatrix.get(x_old, y_old, 0)
                    elif applOp[i] == 1:
                        checkQ = qvalMatrix.get(x_old, y_old, 1)
                    elif applOp[i] == 2:
                        checkQ = qvalMatrix.get(x_old, y_old, 2)
                    elif applOp[i] == 3:
                        checkQ = qvalMatrix.get(x_old, y_old, 3)

                    #print(maxQ, checkQ)

                    if checkQ > maxQ:
                        maxQ = checkQ
                        anyEqual = []
                        anyEqual.extend([applOp[i]])
                    elif checkQ == maxQ:
                        anyEqual.extend([applOp[i]])


            # print("Len of any equal is ", len(anyEqual))
            if len(anyEqual) > 1:
                # random.seed(5)
                val = random.randint(0, len(anyEqual) - 1)
                # print("val is", val)
                # print("anyEqual[val] = ",anyEqual[val] )
                if anyEqual[val] == 0:
                    self.moveN()
                    return [x_old, y_old, 0, self.x, self.y]
                elif anyEqual[val] == 1:
                    self.moveS()
                    return [x_old, y_old, 1, self.x, self.y]
                elif anyEqual[val] == 2:
                    self.moveE()
                    return [x_old, y_old, 2, self.x, self.y]
                elif anyEqual[val] == 3:
                    self.moveW()
                    return [x_old, y_old, 3, self.x, self.y]

            else:
                if anyEqual[0] == 0:
                    self.moveN()
                    return [x_old, y_old, 0, self.x, self.y]
                elif anyEqual[0] == 1:
                    self.moveS()
                    return [x_old, y_old, 1, self.x, self.y]
                elif anyEqual[0] == 2:
                    self.moveE()
                    return [x_old, y_old, 2, self.x, self.y]
                elif anyEqual[0] == 3:
                    self.moveW()
                    return [x_old, y_old, 3, self.x, self.y]


    def exploitPolicy(self, matrix, isApplicable, table, table2):
        maxQ = -10000
        checkQ = -10001
        anyEqual = []
        applOp = aplop(self)
        x_old = self.x
        y_old = self.y
        if self.carrying is False and matrix.getdataat(x_old, y_old).pickup and isApplicable == True:
            self.carrying = True
            return [self.x, self.y, 4, x_old, y_old]
        if self.carrying is True and matrix.getdataat(x_old, y_old).dropoff and isApplicable == True:
            self.carrying = False
            return [self.x, self.y, 5, x_old, y_old]

        if self.carrying:
            qvalMatrix = table
        else:
            qvalMatrix = table2
        for i in range(len(applOp)):
            if i == 0:
                # 0 = North
                # 1 = South
                # 2 = East
                # 3 = West
                if applOp[0] == 0:
                    maxQ = qvalMatrix.get(x_old, y_old, 0)
                elif applOp[0] == 1:
                    maxQ = qvalMatrix.get(x_old, y_old, 1)
                elif applOp[0] == 2:
                    maxQ = qvalMatrix.get(x_old, y_old, 2)
                elif applOp[0] == 3:
                    maxQ = qvalMatrix.get(x_old, y_old, 3)

                anyEqual.extend([applOp[0]])

            else:
                if applOp[i] == 0:
                    checkQ = qvalMatrix.get(x_old, y_old, 0)
                elif applOp[i] == 1:
                    checkQ = qvalMatrix.get(x_old, y_old, 1)
                elif applOp[i] == 2:
                    checkQ = qvalMatrix.get(x_old, y_old, 2)
                elif applOp[i] == 3:
                    checkQ = qvalMatrix.get(x_old, y_old, 3)

                # print(maxQ, checkQ)

                if checkQ > maxQ:
                    maxQ = checkQ
                    anyEqual = []
                    anyEqual.extend([applOp[i]])
                elif checkQ == maxQ:
                    anyEqual.extend([applOp[i]])

        r = random.randint(0, 100)
        if r < 80 or len(applOp) <= len(anyEqual):
            print("GREEDY MOVEMENT")
            i_new = self.greedyPolicy(matrix, isApplicable, table, table2)
            return i_new
        else:
            print("RANDOM MOVEMENT")
            ops = aplop(self)
            for h in anyEqual:
                ops.remove(h)
            r = random.randint(0, len(ops)-1)
            operator = ops[r]
            if operator == 0:
                self.moveN()
                return [x_old, y_old, 0, self.x, self.y]
            elif operator == 1:
                self.moveS()
                return [x_old, y_old, 1, self.x, self.y]
            elif operator == 2:
                self.moveE()
                return [x_old, y_old, 2, self.x, self.y]
            elif operator == 3:
                self.moveW()
                return [x_old, y_old, 3, self.x, self.y]


#####

def aplop(avatar):    # determine applicable operators

    op = []   # will return array of numbers such that
              # 0 = North
              # 1 = South
              # 2 = East
              # 3 = West
              # 4 = Pickup
              # 5 = Dropoff

    if avatar.x == 0:  #cannot move west
        if avatar.y == 4:
            op.extend([1,2])
        elif avatar.y == 0:
            op.extend([0,2])
        else:
            op.extend([0,1,2])

    elif avatar.x == 4:  #cannot move east
        if avatar.y == 4:
            op.extend([1,3])
        elif avatar.y == 0:
            op.extend([0,3])
        else:
            op.extend([0,1,3])

    elif avatar.y == 4: #cannot move north
        if avatar.x == 4:
            op.extend([1,2])
        elif avatar.x == 0:
            op.extend([1,3])
        else:
            op.extend([1,2,3])

    elif avatar.y == 0: #cannot move south
        if avatar.x == 4:
            op.extend([0,2])
        elif avatar.x == 0:
            op.extend([0,3])
        else:
            op.extend([0,2,3])

    else:   #somewhere in the middle
        op.extend([0,1,2,3])



    return op
#end aplop




###############################################################################
# matrix code

class matrix:

    def __init__(self):
        self.matrix = []

    # used to fill in a matrix with a default value for a certain number of rows and columns
    def initialize(self, data, nrows,
                   ncols):  # data is default values in matrix , nrows is number of rows, ncols is number of columns
        for i in range(nrows):
            # reset row to put in each col value
            row = []
            for i in range(ncols):
                # append default data for amount of columns
                # using use case due to shadowcopy
                row.append(contents())

            # put the row into the matrix
            (self.matrix).append(row)

    def getdataat(self, x, y):
        # print("data at (" +str(x)+ ","+str(y)+") is:"+str((self.matrix[y])[x]))
        return (self.matrix[y])[x]

    # used to create a string form of the matrix
    # data inside must be able to convert to string
    def sprint(self):
        temp = ""

        for i in range(len(self.matrix)):
            for j in self.matrix[i]:
                temp += str(j) + " "

            temp += "\n"

        return temp

    # how the matrix will be represented when used as a string
    def __str__(self):
        return self.sprint()

    def __repr__(self):
        return self.matrix


# Test matrix (TO LEARN)
testmatrix = matrix()
testmatrix.initialize(contents(), 5, 5)

print("Inital Matrix:")
print(testmatrix)

#(testmatrix.getdataat(0, 0)).tdropoff()
#(testmatrix.getdataat(0, 2)).tpickup()
(testmatrix.getdataat(0, 0)).tpickup()
(testmatrix.getdataat(2, 2)).tpickup()
(testmatrix.getdataat(4, 4)).tpickup()

(testmatrix.getdataat(0, 4)).tdropoff()
(testmatrix.getdataat(2, 4)).tdropoff()
(testmatrix.getdataat(4, 1)).tdropoff()

print("Matrix with three pickups(1) and dropoffs(2)")
print(testmatrix)

# avatar creation
ava = avatar()
print(ava)

# test for avatar movement
#ava.moveN()
#print(ava)

# Testing Table
table = Qtable()
table2 = Qtable()
table3 = Qtable()
table4 = Qtable()
table.setalpha(0.5)
table.setgamma(0.5)
table2.setalpha(0.5)
table2.setgamma(0.5)
table3.setalpha(0.5)
table3.setgamma(0.5)
table4.setalpha(0.5)
table4.setgamma(0.5)
i_old = ava.randomPolicy(testmatrix, True)

pygame.init()

#Initializing size of window and title of window
gameDisplay = pygame.display.set_mode((800,800))
pygame.display.set_caption('Avatar w/ live q-values')

#Color variables for easy use later
white = (150,150,150)
black = (0,0,0)
red = (255,0,0)
green = (0, 200,0)
yellow = (200, 200, 50)
gameExit = False

#Used to set FPS of visualization, it is called near the end of the code
clock = pygame.time.Clock()

#Functions to display the values of the q-tables on screen
#The reason there is 2 separate ones is for the size of the text
#Initially I had the function call font inside, that way I could modify the
#font size per call, but calling font every time slows the game down
#immensely, like capping at 8-9 FPS
font = pygame.font.SysFont(None, 25)
def text_to_screen(msg, color, locX, locY):
    #font = pygame.font.SysFont(None, fontSize)
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [locX, locY])

font2 = pygame.font.SysFont(None, 70)
def text_to_screen_Big(msg, color, locX, locY):
    #font = pygame.font.SysFont(None, fontSize)
    screen_text = font2.render(msg, True, color)
    gameDisplay.blit(screen_text, [locX, locY])

#To determine the location of where to draw the avatar (square) in the visualization
squareLocX = 0
squareLocY = 0

#Variables used to color the 100 triangles and color of text
#When one is white the other is black and vice versa
triangleColor = white
textColor = black

#Array for pickup and dropoff locations
pickupArr = [5,5,5]
pickUp = [[0, 0], [2, 2], [4, 4]]
dropoffArr = [0,0,0]
dropOff = [[0, 4], [2, 4], [4, 1]]
isActionApplicable = True
learnType = input("Q or SARSA: ")
policy = input("random or greedy or exploit: ")
#Main game loop
while not gameExit:
    #To exit out
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
    if dropoffArr[0] == 5 and dropoffArr[1] == 5 and dropoffArr[2] == 5:
        continue

    #Test code for either QLearn or SARSA
    if policy == "greedy":
        if learnType == "Q":
            i_new = ava.greedyPolicy(testmatrix, isActionApplicable, table, table2)
            if (ava.carrying and i_new[2] < 4):
                table.updateQLEARN(i_new[0], i_new[1], i_new[2], i_new[3], i_new[4],isActionApplicable)
            elif ava.carrying == False and i_new[2] < 4:
                table2.updateQLEARN(i_new[0], i_new[1], i_new[2], i_new[3], i_new[4],isActionApplicable)
            elif i_new[2] == 4:
                table2.updateQLEARN(i_new[0], i_new[1], i_new[2], i_new[3], i_new[4],isActionApplicable)
            elif i_new[2] == 5:
                table.updateQLEARN(i_new[0], i_new[1], i_new[2], i_new[3], i_new[4],isActionApplicable)
        else:
            i_new = ava.greedyPolicy(testmatrix, isActionApplicable, table, table2)
            if (ava.carrying and i_new[2] < 4 and i_old[2] < 4):
                table.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            elif ava.carrying == False and i_new[2] < 4 and i_old[2] < 4:
                table2.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            elif i_new[2] == 4:
                table2.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            elif i_new[2] == 5:
                table.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            elif i_old[2] == 4:
                table2.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            elif i_old[2] == 5:
                table.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            i_old = i_new
    elif policy == "random":
        if learnType == "Q":
            i_new = ava.randomPolicy(testmatrix, isActionApplicable)
            if (ava.carrying and i_new[2] < 4):
                table.updateQLEARN(i_new[0], i_new[1], i_new[2], i_new[3], i_new[4],isActionApplicable)
            elif ava.carrying == False and i_new[2] < 4:
                table2.updateQLEARN(i_new[0], i_new[1], i_new[2], i_new[3], i_new[4],isActionApplicable)
            elif i_new[2] == 4:
                table2.updateQLEARN(i_new[0], i_new[1], i_new[2], i_new[3], i_new[4],isActionApplicable)
            elif i_new[2] == 5:
                table.updateQLEARN(i_new[0], i_new[1], i_new[2], i_new[3], i_new[4],isActionApplicable)
        else:
            i_new = ava.randomPolicy(testmatrix, isActionApplicable)
            if (ava.carrying and i_new[2] < 4 and i_old[2] < 4):
                table.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            elif ava.carrying == False and i_new[2] < 4 and i_old[2] < 4:
                table2.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            elif i_new[2] == 4:
                table2.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            elif i_new[2] == 5:
                table.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            elif i_old[2] == 4:
                table2.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            elif i_old[2] == 5:
                table.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            i_old = i_new
    else:
        if learnType == "Q":
            i_new = ava.exploitPolicy(testmatrix, isActionApplicable, table, table2)
            if (ava.carrying and i_new[2] < 4):
                table.updateQLEARN(i_new[0], i_new[1], i_new[2], i_new[3], i_new[4],isActionApplicable)
            elif ava.carrying == False and i_new[2] < 4:
                table2.updateQLEARN(i_new[0], i_new[1], i_new[2], i_new[3], i_new[4],isActionApplicable)
            elif i_new[2] == 4:
                table2.updateQLEARN(i_new[0], i_new[1], i_new[2], i_new[3], i_new[4],isActionApplicable)
            elif i_new[2] == 5:
                table.updateQLEARN(i_new[0], i_new[1], i_new[2], i_new[3], i_new[4],isActionApplicable)
        else:
            i_new = ava.exploitPolicy(testmatrix, isActionApplicable, table, table2)
            if (ava.carrying and i_new[2] < 4 and i_old[2] < 4):
                table.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            elif ava.carrying == False and i_new[2] < 4 and i_old[2] < 4:
                table2.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            elif i_new[2] == 4:
                table2.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            elif i_new[2] == 5:
                table.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            elif i_old[2] == 4:
                table2.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            elif i_old[2] == 5:
                table.updateSARSA(i_old[0], i_old[1], i_old[2], i_old[3], i_old[4], i_new[2])
            i_old = i_new


    #The locations of the pickup/dropoff relative to the array is left --> right
    #i.e. for pickup, the locations are (0,0) = pickupArr[0], (2,2) = pickupArr[1], (4,4) = pickupArr[2]
    if ava.iscarrying():
        gameDisplay.fill(black)
        triangleColor = white
        textColor = white
        text_to_screen_Big(str(dropoffArr[0]), red, 70, 710)
        text_to_screen_Big(str(dropoffArr[1]), red, 390, 710)
        text_to_screen_Big(str(dropoffArr[2]), red, 710, 210)
    else:
        gameDisplay.fill(white)
        triangleColor = black
        textColor = black
        text_to_screen_Big(str(pickupArr[0]), red, 70, 70)
        text_to_screen_Big(str(pickupArr[1]), red, 390, 390)
        text_to_screen_Big(str(pickupArr[2]), red, 710, 710)



    #To draw avatar in proper location based on its actual location
    if ava.x  == 0:
        squareLocX = 60
    elif ava.x == 1:
        squareLocX = 220
    elif ava.x == 2:
        squareLocX = 380
    elif ava.x == 3:
        squareLocX = 540
    elif ava.x == 4:
        squareLocX = 700

    if ava.y == 0:
        squareLocY = 60
    elif ava.y == 1:
        squareLocY = 220
    elif ava.y == 2:
        squareLocY = 380
    elif ava.y == 3:
        squareLocY = 540
    elif ava.y == 4:
        squareLocY = 700

    avatarDisplayColor = [0,0,0]
    if ava.iscarrying():
        avatarDisplayColor = [0, 0, 255]        #carrying is blue
    else:
        avatarDisplayColor = [0, 150, 0]        #not carrying green

    #Draw avatar
    pygame.draw.rect(gameDisplay, avatarDisplayColor, [squareLocX, squareLocY, 40, 40])

    #These if statements check if a pickup location has no more things to pickup
    #or if a dropoff location is full at 5, if so, P/D would NOT be an applicable operator
    #at that location
    if ava.iscarrying() == False:
        if ava.x == 0 and ava.y == 0 and pickupArr[0] != 0:
            pickupArr[0] = pickupArr[0] - 1
            isActionApplicable = True
        elif ava.x == 0 and ava.y == 0 and pickupArr[0] == 0:
            isActionApplicable = False

        if ava.x == 2 and ava.y == 2 and pickupArr[1] != 0:
            pickupArr[1] = pickupArr[1] - 1
            isActionApplicable = True
        elif ava.x == 2 and ava.y == 2 and pickupArr[1] == 0:
            isActionApplicable = False

        if ava.x == 4 and ava.y == 4 and pickupArr[2] != 0:
            pickupArr[2] = pickupArr[2] - 1
            isActionApplicable = True
        elif ava.x == 4 and ava.y == 4 and pickupArr[2] == 0:
            isActionApplicable = False


    if ava.iscarrying() == True:
        if ava.x == 0 and ava.y == 4 and dropoffArr[0] < 5:
            dropoffArr[0] = dropoffArr[0] + 1
            isActionApplicable = True
        elif ava.x == 0 and ava.y == 4 and dropoffArr[0] == 5:
            isActionApplicable = False

        if ava.x == 2 and ava.y == 4 and dropoffArr[1] < 5:
            dropoffArr[1] = dropoffArr[1] + 1
            isActionApplicable = True
        elif ava.x == 2 and ava.y == 4 and dropoffArr[1] == 5:
            isActionApplicable = False

        if ava.x == 4 and ava.y == 1 and dropoffArr[2] < 5:
            dropoffArr[2] = dropoffArr[2] + 1
            isActionApplicable = True
        elif ava.x == 4 and ava.y == 1 and dropoffArr[2] == 5:
            isActionApplicable = False



    #This for loop draws over the 100 triangles and 100 q-values
    for i in range(5):
        x = 0
        a = 0
        if i == 1:
            x = 160
        if i == 2:
            x = 320
        if i == 3:
            x = 480
        if i == 4:
            x = 640

        for j in range(5):
            y = 0
            b = 0
            if j == 1:
                y = 160
            if j == 2:
                y = 320
            if j == 3:
                y = 480
            if j == 4:
                y = 640


            pygame.draw.polygon(gameDisplay, triangleColor, [(0+x, 0+y), (0+x, 160+y), (80+x, 80+y)], 3)
            pygame.draw.polygon(gameDisplay, triangleColor, [(0+x, 0+y), (160+x, 0+y), (80+x, 80+y)], 3)
            pygame.draw.polygon(gameDisplay, triangleColor, [(160+x, 0+y), (160+x, 160+y), (80+x, 80+y)], 3)
            pygame.draw.polygon(gameDisplay, triangleColor, [(160+x, 160+y), (0+x, 160+y), (80+x, 80+y)], 3)


            for k in range(4):
                p = table.table[i][j][k]
                m = table2.table[i][j][k]
                textColor1 = white
                textColor2 = black
                if m == -10000:
                    m = 0
                if p == -10000:
                    p = 0
                if p < -0.5:
                    textColor1 = red
                elif p < 0:
                    textColor1 = yellow
                elif p > 0:
                    textColor1 = green
                if m < -0.5:
                    textColor2 = red
                elif m < 0:
                    textColor2 = yellow
                elif m > 0:
                    textColor2 = green

                if ava.iscarrying():
                    if k == 0:
                        text_to_screen(("%.3f" % p), textColor1, 60 + x, 120 + y)
                        # text_to_screen(str(p), white, 25 + x, 90 + y)
                    if k == 1:
                        text_to_screen(("%.3f" % p), textColor1, 60 + x, 30 + y)
                        # text_to_screen(str(p), white, 25 + x, 90 + y)
                        # text_to_screen(str(p), white, 140 + x, 90 + y)
                    if k == 2:
                        text_to_screen(("%.3f" % p), textColor1, 100 + x, 70 + y)
                        # text_to_screen(str(p), white, 90 + x, 40 + y)
                    if k == 3:
                        text_to_screen(("%.3f" % p), textColor1, 15 + x, 70 + y)
                        # text_to_screen(str(p), white, 90 + x, 40 + y)
                        # text_to_screen(str(p), white, 90 + x, 140 + y)
                else:
                    if k == 0:
                        text_to_screen(("%.3f" % m), textColor2, 60 + x, 120 + y)
                        # text_to_screen(str(p), white, 25 + x, 90 + y)
                    if k == 1:
                        text_to_screen(("%.3f" % m), textColor2, 60 + x, 30 + y)
                        # text_to_screen(str(p), white, 25 + x, 90 + y)
                        # text_to_screen(str(p), white, 140 + x, 90 + y)
                    if k == 2:
                        text_to_screen(("%.3f" % m), textColor2, 100 + x, 70 + y)
                        # text_to_screen(str(p), white, 90 + x, 40 + y)
                    if k == 3:
                        text_to_screen(("%.3f" % m), textColor2, 15 + x, 70 + y)
                        # text_to_screen(str(p), white, 90 + x, 40 + y)
                        # text_to_screen(str(p), white, 90 + x, 140 + y)

            #pygame.draw.polygon(gameDisplay, white, [(p1x, p1y), (p2x, p2y), (p3x, p3y)])
            #pygame.draw.polygon(gameDisplay, white, [(p1x, p1y), (p2y, p2x), (p3x, p3y)])
            #pygame.draw.polygon(gameDisplay, white, [(p2y, p1x), (p2y, p2y), (p3x, p3y)])
            #pygame.draw.polygon(gameDisplay, white, [(p2y, p2y), (p1x, p2y), (p3x, p3y)])



    pygame.display.update()

    clock.tick(10)  #FPS
    #print(clock.get_fps())    #Print out the FPS to double check


#print("Q LEARNING: ")
#print("Carrying: ")
#table.print()
#print("Not Carrying: ")
#table2.print()






print("Carrying: ")
table.print()
print("Not Carrying: ")
table2.print()
