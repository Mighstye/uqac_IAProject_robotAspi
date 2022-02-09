import logging

from AIProject.enum.cardinals import Cardinals


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

    def move(self, card):  # Make the robot move (TODO Check if the direction are right)
        self.environment.grid[self.position[0], self.position[1]].changerobotstate()  # Robot leave the room
        if card == Cardinals.NORTH:
            self.position = [self.position[0] + 1, self.position[1]]
        if card == Cardinals.SOUTH:
            self.position = [self.position[0] - 1, self.position[1]]
        if card == Cardinals.EAST:
            self.position = [self.position[0], self.position[1] + 1]
        if card == Cardinals.WEST:
            self.position = [self.position[0], self.position[1] - 1]
        self.environment.grid[self.position[0], self.position[1]].changerobotstate()  # Robot join the room

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
