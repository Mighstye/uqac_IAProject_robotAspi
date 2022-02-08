import random


# Room class, a room is instanced with a random number which define what roomobjects is in a room (Dust, jewelry or
# both) and put these in the room inventory.
class Room:
    hasDust = False
    hasJewelry = False

    def __init__(self):
        self.hasDust = False
        self.hasJewelry = False
        randomizer = random.randint(0, 100)
        if 50 <= randomizer < 75:
            self.hasDust = True
        if 75 <= randomizer < 90:
            self.hasJewelry = True
        if 90 <= randomizer < 100:
            self.hasDust = True
            self.hasJewelry = True

    def clean(self):
        # This method clear both boolean value and return what the
        # room possessed via an array as [DUST(TRUE/FALSE) , JEWELRY(TRUE/FALSE)]
        loot = [self.hasDust, self.hasJewelry]
        self.hasDust = False
        self.hasJewelry = False
        return loot

    def ask(self):
        # This method refers as the captor we should use
        # The robot can ask the captor of the room with this method,
        # and it'll return what the room contains
        return [self.hasDust, self.hasJewelry]

    def setElement(self, roomobject):
        # This method will set an element in a room
        if roomobject == "DUST":
            if self.hasDust:
                return False
            else:
                self.hasDust = True
                return True

        else:
            if self.hasJewelry:
                return False
            else:
                self.hasJewelry = True
                return True
