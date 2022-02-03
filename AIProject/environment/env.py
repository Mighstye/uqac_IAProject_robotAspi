import AIProject.environment.room as room


# Environment class, an environment consist of a 5x5 grid filled with rooms
class env:
    def __init__(self):
        env.grid = [[room.Room() for j in range(5)] for i in range(5)]
