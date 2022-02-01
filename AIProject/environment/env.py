import room


class env:
    def __init__(self):
        env.grid = [[room.Room for j in range(5)] for i in range(5)]