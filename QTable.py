import random

class Qtable:
    def __init__(self):
        self.table = [[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]],
                      [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]],
                      [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]],
                      [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]],
                      [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]]

        self.alpha = 0
        self.gamma = 0
        for i in range(5):
            self.table[0][i][3] = -10000
            self.table[4][i][2] = -10000
            self.table[i][0][1] = -10000
            self.table[i][4][0] = -10000


    # set alpha value for Q value calculation
    def setalpha(self, value):
        self.alpha = value

    # get alpha value
    def getalpha(self):
        return self.alpha


    # set gamma value for Q value calculation
    def setgamma(self, value):
        self.gamma = value

    # get gamma value
    def getgamma(self):
        return self.gamma


        # to set a q value in the table
        # i, j provide location in the world
        # k value:
        # 0 - North
        # 1 - South
        # 2 - East
        # 3 - West
        # 4 - Pickup
        # 5 - Dropoff
    def setqvalue(self, i, j, k, value):
        self.table[i][j][k] = value


    # to retrieve a value from the table
        # i, j provide location in the world
        # k value:
        # 0 - North
        # 1 - South
        # 2 - East
        # 3 - West
        # 4 - Pickup
        # 5 - Dropoff
    def get(self, i, j, k):
        return self.table[i][j][k]


    # this can be used to determine the next move when using P-Exploit/P-Greedy policies
    # returns value 0-3 for north, south, east, west
    # I didn't include values for pickup/dropoff because I believe these actions happen automatically when applicable
    def maxdirection(self, i, j, isApplicable):
        max = self.get(i,j,0)
        direction = 0
        for k in range(6):
            value = self.get(i,j,k)

            if value > max:
                if k < 4 or isApplicable:
                    max = value
                    direction = k

            # if the values are the same, choose randomly
            elif (value == max):
                if (random.random() > 0.5):
                    max = value
                    direction = k
                else:
                    max = max

        return direction


    # used to update Q values in the table
    # avatar is was previously in state (i, j, k), and is now in (iprime, jprime, kprime),
    # where (i, j)/(iprime, jprime) are positions in the world, k is the last move performed,
    # and kprime is the next move about to be performed
        # k/kprime values:
        # 0 - North
        # 1 - South
        # 2 - East
        # 3 - West
        # 4 - Pickup
        # 5 - Dropoff
    def updateSARSA(self, i, j, k, iprime, jprime, kprime):
        alpha = self.getalpha()
        gamma = self.getgamma()

        # if the previous action was pickup of dropoff, set reward to 13, otherwise set to -1
        if (k == 5 or k == 4):
            reward = 13
        else:
            reward = -1

        # Update formula:
        # Q(i,j,k) <- (1-alpha) * Q(i,j,k) + alpha * [Reward(k) + gamma * Q(iprime, jprime, kprime)]
        # Q(i,j,k) is the previous state to be updated
        # Q(iprime, jprime, kprime) is the current state with the next action chosen as kprime

        newvalue = ((1-alpha) * self.get(i, j, k)) + alpha * (reward + gamma * self.get(iprime, jprime, kprime))
        self.setqvalue(i, j, k, newvalue)


    def updateSARSAV2(self,currX, currY, matrix, k, iprime, jprime):
        alpha = self.getalpha()
        gamma = self.getgamma()

        # if the previous action was pickup of dropoff, set reward to 13, otherwise set to -1
        if (k == 5 or k == 4):
            reward = 13
        else:
            reward = -1

        # Update formula:
        # Q(i,j,k) <- (1-alpha) * Q(i,j,k) + alpha * [Reward(k) + gamma * Q(iprime, jprime, kprime)]
        # Q(i,j,k) is the previous state to be updated
        # Q(iprime, jprime, kprime) is the current state with the next action chosen as kprime

        newvalue = ((1-alpha) * matrix[currX][currY]) + alpha * (reward + gamma * matrix[iprime][jprime])
        self.setqvalue(currX,currY,k, newvalue)
        matrix[currX][currY] = newvalue


    def updateQLEARNV2(self,currX, currY, matrix, k, iprime, jprime, isCarrying, actionApplicable):
        alpha = self.getalpha()
        gamma = self.getgamma()
        maxQ = 0


        if (iprime == 0 and jprime == 4) or (iprime == 2 and jprime == 4) or (iprime == 4 and jprime == 2):
            if isCarrying and actionApplicable:
                maxQ = matrix[iprime][jprime]
        elif (iprime == 0 and jprime == 0) or (iprime == 2 and jprime == 2) or (iprime == 4 and jprime == 4):
            if actionApplicable and not isCarrying:
                maxQ = matrix[iprime][jprime]

        #kprime = self.maxdirection(iprime, jprime)

        #northQ = matrix[iprime][jprime-1]
        #southQ = matrix[iprime][jprime+1]
        #westQ = matrix[iprime-1][jprime]
        #eastQ = matrix[iprime+1][jprime]
        elif k !=4 or k != 5:
            if iprime == 0 and jprime == 0:
                if matrix[iprime + 1][jprime] > matrix[iprime][jprime + 1]:
                    maxQ = matrix[iprime + 1][jprime]
                elif matrix[iprime + 1][jprime] < matrix[iprime][jprime + 1]:
                    maxQ = matrix[iprime][jprime + 1]
                else:
                    maxQ = random.choice([matrix[iprime + 1][jprime], matrix[iprime][jprime + 1]])
            elif iprime == 4 and jprime == 0:
                if matrix[iprime - 1][jprime] > matrix[iprime][jprime + 1]:
                    maxQ = matrix[iprime - 1][jprime]
                elif matrix[iprime - 1][jprime] < matrix[iprime][jprime + 1]:
                    maxQ = matrix[iprime][jprime + 1]
                else:
                    maxQ = random.choice([matrix[iprime - 1][jprime], matrix[iprime][jprime + 1]])
            elif iprime == 0 and jprime == 4:
                if matrix[iprime + 1][jprime] > matrix[iprime][jprime - 1]:
                    maxQ = matrix[iprime + 1][jprime]
                elif matrix[iprime + 1][jprime] < matrix[iprime][jprime - 1]:
                    maxQ = matrix[iprime][jprime - 1]
                else:
                    maxQ = random.choice([matrix[iprime + 1][jprime], matrix[iprime][jprime - 1]])
            elif iprime == 4 and jprime == 4:
                if matrix[iprime - 1][jprime] > matrix[iprime][jprime - 1]:
                    maxQ = matrix[iprime - 1][jprime]
                elif matrix[iprime - 1][jprime] < matrix[iprime][jprime - 1]:
                    maxQ = matrix[iprime][jprime - 1]
                else:
                    maxQ = random.choice([matrix[iprime - 1][jprime], matrix[iprime][jprime - 1]])
            elif iprime == 0 and jprime > 0 and jprime < 4:
                maxQ = max(matrix[iprime][jprime - 1], matrix[iprime][jprime + 1], matrix[iprime + 1][jprime])
            elif iprime == 4 and jprime > 0 and jprime < 4:
                maxQ = max(matrix[iprime][jprime - 1], matrix[iprime][jprime + 1], matrix[iprime - 1][jprime])
            elif jprime == 0 and iprime > 0 and iprime < 4:
                maxQ = max(matrix[iprime][jprime + 1], matrix[iprime + 1][jprime], matrix[iprime - 1][jprime])
            elif jprime == 4 and iprime > 0 and iprime < 4:
                maxQ = max(matrix[iprime][jprime - 1], matrix[iprime + 1][jprime], matrix[iprime - 1][jprime])
            else:
                maxQ = max(matrix[iprime][jprime - 1], matrix[iprime + 1][jprime], matrix[iprime - 1][jprime], matrix[iprime][jprime + 1])
        else:
            maxQ = matrix[currX,currY]



        if (k == 4 or k == 5):
            reward = 13
        else:
            reward = -1


        newvalue = ((1-alpha) * matrix[currX][currY]) + alpha * (reward + gamma * maxQ)
        self.setqvalue(currX,currY,k, newvalue)
        matrix[currX][currY] = newvalue

    # Copy/pasted from updateSARSA, except this does not include the kprime argument, as this value is chosen based
    # the maximum known value, not what move is actually being taken
    def updateQLEARN(self, i, j, k, iprime, jprime, isApplicable):
        alpha = self.getalpha()
        gamma = self.getgamma()

        kprime = self.maxdirection(iprime, jprime, isApplicable)

        # if the previous action was pickup of dropoff, set reward to 13, otherwise set to -1
        if (k == 4 or k == 5):
            reward = 13
        else:
            reward = -1

        # Update formula:
        # Q(i,j,k) <- (1-alpha) * Q(i,j,k) + alpha * [Reward(k) + gamma * maxQ(iprime, jprime, kprime)]
        # Q(i,j,k) is the previous state to be updated
        # Q(iprime, jprime, kprime) is the current state with the next action chosen as kprime
        newvalue = ((1-alpha) * self.get(i, j, k)) + alpha * (reward + gamma * self.get(iprime, jprime, kprime))
        self.setqvalue(i, j, k, newvalue)


    def print(self):
        print("Current Q Table -- Alpha =", self.getalpha(), ", Gamma =", self.getgamma())
        print("(x, y)\t[ N , S , E , W , P , D ]")
        for i in range(5):
            for j in range(5):
                print("(%d, %d)\t" % (i, j),end=' ')
                for k in range(6):
                    if self.table[i][j][k] == -10000:
                        print("-x-", end=" ")
                    else:
                        print("%.2f" % self.table[i][j][k], end=" ")
                print()
            print()
        print()



tableNew = Qtable()
for i in range(5):
    for j in range(5):
        for k in range(4):
            if i > 3:
                tableNew.setqvalue(i,j,k,2)
            elif j > 2:
                tableNew.setqvalue(i, j, k, 5)
            elif k > 2:
                tableNew.setqvalue(i, j, k, 9)
            else:
                tableNew.setqvalue(i, j, k, 7)

tableNew.print()