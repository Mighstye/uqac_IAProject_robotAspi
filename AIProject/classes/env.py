import numpy as np
from AIProject.enum import tilestypes as tiles


def randomtiles():
    randomizer = np.randint(0, 100)
    if 0 <= randomizer < 15:
        return tiles.Tilestypes.DOUBLE
    if 15 <= randomizer < 40:
        return tiles.Tilestypes.POUSSIERE
    if 40 <= randomizer < 65:
        return tiles.Tilestypes.BIJOUX
    if 65 <= randomizer < 100:
        return tiles.Tilestypes.RIEN


class Environment:
    def __init__(self):
        self.env = np.full([5, 5], None)
        self.generate()

    def generate(self):
        for i in range(len(self.env)):
            for j in range(len(self.env)):
                self.env[i][j] = randomtiles()

    def returntiles(self, position):
        return self.env[position]
