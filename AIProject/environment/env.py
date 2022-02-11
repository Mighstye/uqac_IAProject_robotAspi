import AIProject.environment.room as room
import AIProject.robot.robot as robot


# Environment class, an environment consist of a 5x5 grid filled with rooms
class env:
    def __init__(self):
        env.grid = [[room.Room() for j in range(5)] for i in range(5)]

    def putrobot(self):  # Put a new robot in the env TODO DEBUG
        env.robot = robot.Robot(self, [2, 2])
        #  TODO The robot have to show up in the visual grid
        #  To do so, use the robothere boolean of rooms
        return env.robot
