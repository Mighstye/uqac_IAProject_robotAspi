from AIProject.enum import cardinals as card


class Aspirobot:
    inventory = []

    def __init__(self, position, envi):
        self.env = envi
        self.position = position
        self.tile = envi.returntiles(self.position)

    def move(self, direction):
        temp = self.position
        if direction == card.Cardinals.NORTH:
            self.position = [temp[0], temp[1]+1]
        if direction == card.Cardinals.SOUTH:
            self.position = [temp[0], temp[1]-1]
        if direction == card.Cardinals.WEST:
            self.position = [temp[0]+1, temp[1]]
        if direction == card.Cardinals.EAST:
            self.position = [temp[0]-1, temp[1]]
        self.tile = self.env.returntiles(self.position)

