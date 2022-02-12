import logging

from AIProject.enum.cardinals import Cardinals
import random
import AIProject.environment.env as env


# TODO DEBUG
class Robot:
    malus = 0
    bonus = 0
    position = []  # Position of the robot on the grid

    def __init__(self, environment, coord):
        self.malus = 0
        self.bonus = 0
        self.position = coord
        self.environment = environment  # We tell the robot which env it's attached to
        self.environment.grid[self.position[0]][self.position[1]].changerobotstate()
        # We tell the robot where the robot spawned that the robot is actually here

    def move(self, card):  # Make the robot move
        self.environment.grid[self.position[0]][self.position[1]].changerobotstate()  # Robot leave the room
        # logging.info(len(self.environment.grid[0][0]))
        # TODO Prevent the robot from going outside the grid, return FALSE when deplacement is not permitted
        if card == Cardinals.NORTH:
            self.position = [self.position[0], self.position[1] - 1]
            logging.info("Going north")
        if card == Cardinals.SOUTH:
            self.position = [self.position[0], self.position[1] + 1]
            logging.info("Going south")
        if card == Cardinals.EAST:
            self.position = [self.position[0] + 1, self.position[1]]
            logging.info("Going east")
        if card == Cardinals.WEST:
            self.position = [self.position[0] - 1, self.position[1]]
            logging.info("Going west")
        self.environment.grid[self.position[0]][self.position[1]].changerobotstate()  # Robot join the room

    def vacuum(self):
        #  The robot vacuum everything in the room and put it in its dust bag (jewels included)
        loot = self.environment.grid[self.position[0], self.position[1]].clean()
        if loot[1]:
            self.malus += 1
        logging.info("Robot     : Everything has been vacuumed on " + self.position)

    def takejewels(self):  # The robot take the jewels in the room
        #  The robot CANNOT take jewels if there is dust in the room and will vacuum otherwise
        #  The robot will put the jewels in its inventory
        logging.info("Robot     : Attempt to take jewels on " + self.position)
        roominfo = self.environment.grid[self.position[0], self.position[1]].ask()
        if not roominfo[0]:
            logging.info("Robot     : Jewels has been taken on " + self.position)
            self.bonus += 1
            self.environment.grid[self.position[1], self.position[1]].clean()
        else:
            logging.warning("Robot     : Can't take jewels when there is dust, too late !")

    def randomMove(self):
        a = random.randint(0, 3)
        if a == 0:
            self.move(Cardinals.NORTH)
        if a == 1:
            self.move(Cardinals.SOUTH)
        if a == 2:
            self.move(Cardinals.EAST)
        if a == 3:
            self.move(Cardinals.WEST)

    def searchValue(noVisitedRoom):

        for i in range(5):
            for j in range(5):
                if noVisitedRoom[i][j] ==True:

                    break
                    print('true')

        print('false')

    def deepSearch(self):

        noVisitedRoom = [[0 for i in range(5)] for j in range(5)]    # We build a boolean matrix to know visited rooms
        Mesures = [[0 for i in range(5)] for j in range(5)]         # We build a numeric matrix to have our metric performance in each room
        waitingList =[]
        waitingList.append(self.position)

        pos = waitingList[0]



        if self.environment.grid[pos[0]][pos[1]].hasJewelry and self.environment.grid[pos[0]][pos[1]].hasDust:
            Mesures[pos[0]][pos[1]] -= 1
        elif self.environment.grid[pos[0]][pos[1]].hasDust:
            Mesures[pos[0]][pos[1]] += 1
        elif self.environment.grid[pos[0]][pos[1]].hasJewelry:
            Mesures[pos[0]][pos[1]] += 2

        if noVisitedRoom[pos[0] - 1][pos[1]] == 0 and pos[0]-1 >= 0:

            if [pos[0] - 1, pos[1]] not in waitingList:
                waitingList.insert(0, [pos[0] - 1, pos[1]])

        if noVisitedRoom[pos[0]][pos[1] - 1] == 0 and pos[1]-1 >= 0:
            if [pos[0], pos[1] - 1] not in waitingList:
                waitingList.insert(0, [pos[0], pos[1] - 1])

        if noVisitedRoom[pos[0] + 1][pos[1]] == 0 and pos[0]+1 >= 0 >= 0:
            if [pos[0] + 1, pos[1]] not in waitingList:
                waitingList.insert(0, [pos[0] + 1, pos[1]])

        if noVisitedRoom[pos[0]][pos[1] + 1] == 0 and pos[1]+1 >= 0:
            if [pos[0], pos[1] + 1] not in waitingList:
                waitingList.insert(0, [pos[0], pos[1] + 1])

        noVisitedRoom[pos[0]][pos[1]] = 1
        waitingList.pop()



        print(Mesures)

