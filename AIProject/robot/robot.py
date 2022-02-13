import logging

from AIProject.enum.cardinals import Cardinals
import random
import AIProject.environment.env as env
import AIProject.threads.environmentthread


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
        if card == Cardinals.NORTH:
            self.position = [self.position[0] - 1, self.position[1]]
            logging.info("Going north")
        if card == Cardinals.SOUTH:
            self.position = [self.position[0] + 1, self.position[1]]
            logging.info("Going south")
        if card == Cardinals.EAST:
            self.position = [self.position[0], self.position[1] + 1]
            logging.info("Going east")
        if card == Cardinals.WEST:
            self.position = [self.position[0], self.position[1] - 1]
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
        if a == 0 and self.position[0] - 1 >= 0:
            self.move(Cardinals.NORTH)
        elif a == 1 and self.position[0] + 1 < 5:
            self.move(Cardinals.SOUTH)
        elif a == 2 and self.position[1] + 1 < 5:
            self.move(Cardinals.EAST)
        elif a == 3 and self.position[1] - 1 >= 0:
            self.move(Cardinals.WEST)
        else:
            self.randomMove()

    def goToPosition(self, x, y):
        if x != self.position[0]:
            if self.position[0] > x:
                self.move(Cardinals.EAST)
            else:
                self.move(Cardinals.WEST)
        elif y != self.position[1]:
            if self.position[1] > y:
                self.move(Cardinals.NORTH)
            else:
                self.move(Cardinals.SOUTH)
        else:
            logging.info("Already at position [" + str(x) + "," + str(y) + "]")
            return False

    def goToHighestReward(self, env):
        self.goToPosition(env.highestReward())
