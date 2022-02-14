import logging
import threading
import random
import AIProject.environment.env as env
import time
from AIProject.robot import robot
import numpy as np

# The thread for the environment gestion



class environmentthread(threading.Thread):
    stopsignal = False  # This boolean is used to stop the thread when needed.

    def __init__(self, mutex):
        # Initialization of the thread
        self.mutex = mutex  # I learn we should use this for some reason (Might get removed)
        self.env = env.env()  # The environment associated with the thread
        threading.Thread.__init__(self)  # Put the class into a thread
        logging.info("Environment Thread    : Initialized")  # Log the thread has been initialized

    def run(self):
        # Run loop of the thread
        logging.info("Environment Thread    : Started !")  # Some logging
        while not self.stopsignal:  # Execution loop that stop when stopsignal boolean become True
            self.generateElement(20, "DUST") # Generate dust with probability 55%
            self.generateElement(10, "JEWELRY") # Generate Jewel with probability 40%
            time.sleep(3)

        logging.info("Environment Thread    : Stopped.")

    def stop(self):
        # Method to stop the thread
        # This method set the stopsignal boolean to True
        # Making the thread to stop by itself
        logging.info("Environment Thread    : Stop signal sent to Environment Thread")
        self.stopsignal = True

    def getenv(self):
        # Method to return to whole environment associated with the thread
        # This method will be mainly used to display the environment in a UI
        return self.env

    def generateElement(self, p , roomobject):
        if p >= random.uniform(0, 1) * 100:  # if random with probability p
            elementPlaced = False
            cantPlaceElement=False
            i = 0
            while not elementPlaced or cantPlaceElement:
                x = random.randint(0, 4)
                y = random.randint(0, 4)
                while not env.env.grid[x][y].setElement(roomobject) :
                    x = random.randint(0, 4)
                    y = random.randint(0, 4)
                    i += 1
                    if i >= 100 :
                        logging.info("Could not place element after " + str(i) + " try, aborting")
                        return False
                    """magic"""
                logging.info("Element added to the grid at the position " + str(x) + " " + str(y))
                elementPlaced = True

                # while not env.env.grid[x][y].setElement(roomobjects):

    def distanceToRobot(self,x,y):
        positionRobot = self.env.getRobot().position
        distance = abs(x-positionRobot[0]) + abs(y-positionRobot[1])

        return distance


    def computeCost(self):
        costgrid = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                if env.env.grid[i][j].hasJewelry and env.env.grid[i][j].hasDust:
                    costgrid[i][j] = 5
                elif env.env.grid[i][j].hasJewelry:
                    costgrid[i][j] = 15
                elif env.env.grid[i][j].hasDust:
                    costgrid[i][j] = 10
                costgrid[i][j] -= self.distanceToRobot(i, j)
        return costgrid

    def highestReward(self):
        highestRewardPosition = [0,0]
        highestReward = 0
        costgrid = self.computeCost()
        for i in range(5):
            for j in range(5):
                if costgrid[i][j] > highestReward:
                    highestRewardPosition = [i, j]
                    highestReward = costgrid[i][j]
        return highestRewardPosition