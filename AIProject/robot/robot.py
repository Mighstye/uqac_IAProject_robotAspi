import logging

from AIProject.enum.cardinals import Cardinals
import random
import AIProject.environment.env as env


class Robot:
    poussiere = 0
    bijoux = 0
    erreur = 0
    mouvement = 0
    position = []  # Position of the robot on the grid
    lastmove = []
    poids = []

    def __init__(self, environment, coord):
        self.maxiteration = 50
        self.inititeration = 4
        self.lastmove = []
        self.malus = 0
        self.bonus = 0
        self.position = coord
        self.environment = environment  # We tell the robot which env it's attached to
        self.environment.grid[self.position[0]][self.position[1]].changerobotstate()
        self.poids = [[0 for j in range(5)] for i in range(5)]
        self.poussiere = 0
        self.bijoux = 0
        self.erreur = 0
        self.mouvement = 0
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
        if len(self.lastmove) == self.inititeration:
            self.lastmove.append(self.position)
            self.lastmove.pop(0)
        else:
            self.lastmove.append(self.position)
        self.poids[self.position[0]][self.position[1]] += 1
        self.mouvement += 1
        for ligne in self.poids:
            for elem in ligne:
                print(elem, end="")
            print()
        print("-------------")

    def vacuum(self):
        #  The robot vacuum everything in the room and put it in its dust bag (jewels included)
        loot = self.environment.grid[self.position[0]][self.position[1]].clean()
        if loot[1]:
            self.erreur += 1
        self.poussiere += 1
        logging.info("Robot     : Everything has been vacuumed on " + str(self.position))

    def takejewels(self):  # The robot take the jewels in the room
        #  The robot CANNOT take jewels if there is dust in the room and will vacuum otherwise
        #  The robot will put the jewels in its inventory
        logging.info("Robot     : Attempt to take jewels on " + str(self.position))
        roominfo = self.environment.grid[self.position[0]][self.position[1]].ask()
        if not roominfo[0]:
            logging.info("Robot     : Jewels has been taken on " + str(self.position))
            self.bijoux += 1
            self.environment.grid[self.position[0]][self.position[1]].clean()
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

    def randomMoveInSet(self, cards):
        a = random.randint(0, len(cards)-1)
        self.move(cards[a])

