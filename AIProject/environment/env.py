import AIProject.environment.room as room
import AIProject.robot.robot as robot


# Environment class, an environment consist of a 5x5 grid filled with rooms
class env:
    robot = None
    grid = None

    def __init__(self):
        env.grid = [[room.Room() for j in range(5)] for i in range(5)]
        env.robot = None

    def putrobot(self):  # Put a new robot in the env
        env.robot = robot.Robot(self, [2, 2])
        #  To do so, use the robothere boolean of rooms
        return env.robot

    def getRobot(self):
        return self.robot

    def getGrid(self):
        return self.grid



