from AIProject.enum import roomobjects
import random


# Room class, a room is instanced with a random number which define what roomobjects is in a room (Dust, jewelry or
# both) and put these in the room inventory.
class Room:
    inventory = []

    def __init__(self):
        self.inventory = []
        randomizer = random.randint(0, 100)
        if 50 <= randomizer < 75:
            self.inventory.append(roomobjects.roomobjects.DUST)
        if 75 <= randomizer < 90:
            self.inventory.append(roomobjects.roomobjects.JEWELRY)
        if 90 <= randomizer < 100:
            self.inventory.append(roomobjects.roomobjects.DUST)
            self.inventory.append(roomobjects.roomobjects.JEWELRY)

    def clean(self):
        # This method will be used by the robot when it goes in a room. It cleans the room (aka empty the inventory
        # of this room) and return what the robot aspired in the room (loot)
        loot = self.inventory
        self.inventory = []
        return loot

    def ask(self):
        # This method refers as the captor we should use
        # The robot can ask the captor of the room with this method,
        # and it'll return what's in the room inventory
        return self.inventory
