from AIProject.enum import roomobjects
import numpy as np


class Room:
    inventory = []

    def __init__(self):
        randomizer = np.randint(0, 100)
        if 50 <= randomizer < 75:
            self.inventory.append(roomobjects.roomobjects.DUST)
        if 75 <= randomizer < 90:
            self.inventory.append(roomobjects.roomobjects.JEWELRY)
        if 90 <= randomizer < 100:
            self.inventory.append(roomobjects.roomobjects.DUST)
            self.inventory.append(roomobjects.roomobjects.JEWELRY)

    def clean(self):
        loot = self.inventory
        self.inventory = []
        return loot

    def ask(self):
        return self.inventory
