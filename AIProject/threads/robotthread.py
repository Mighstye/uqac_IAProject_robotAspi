import math
import time
import logging
import threading
import AIProject.enum.cardinals as card


class robotthread(threading.Thread):
    stopsignal = False

    def __init__(self, mutex, robot, mode, envthread, maxiteration):
        time.sleep(0.5)
        self.poidsN = 0
        self.poidsS = 0
        self.poidsE = 0
        self.poidsW = 0
        self.poidsMin = 0
        self.predictionPos = []
        self.possibleMove = []
        self.futurMove = None
        self.futurPriority = -1
        self.iteration = 0
        self.mutex = mutex
        self.robot = robot
        self.envthread = envthread
        self.mode = mode  # 0 : Non informe, 1 : Informe
        self.robot.maxiteration = maxiteration
        threading.Thread.__init__(self)
        logging.info("Robot Thread  : Initialized.")

    def run(self):
        logging.info("Robot Thread  : Started.")
        while not self.stopsignal:
            if self.mode == "0":
                self.noninforme()
            else:
                self.informe()
            self.iteration += 1
            time.sleep(3)
        logging.info("Poussiere aspire: " + str(self.robot.poussiere))
        logging.info("Bijoux recupere : " + str(self.robot.bijoux))
        logging.info("Bijoux aspire : " + str(self.robot.erreur))
        logging.info("Mouvement effectue : " + str(self.robot.mouvement))
        logging.info("Robot Thread  : Stopped.")

    def stop(self):
        logging.info("Robot Thread  : Stop signal sent to Robot Thread")
        self.stopsignal = True
        self.envthread.stop()

    def noninforme(self):
        if self.iteration == self.robot.maxiteration:
            self.stop()
            return
        if self.iteration < self.robot.inititeration:
            self.robot.randomMove()
        else:
            try:
                if self.robot.position[0] - 1 >= 0:
                    self.poidsN = self.robot.poids[self.robot.position[0] - 1][self.robot.position[1]]
                else:
                    self.poidsN = math.inf
            except:
                self.poidsN = math.inf
            try:
                if self.robot.position[0] + 1 < 5:
                    self.poidsS = self.robot.poids[self.robot.position[0] + 1][self.robot.position[1]]
                else:
                    self.poidsS = math.inf
            except:
                self.poidsS = math.inf
            try:
                if self.robot.position[1] + 1 < 5:
                    self.poidsE = self.robot.poids[self.robot.position[0]][self.robot.position[1] + 1]
                else:
                    self.poidsE = math.inf
            except:
                self.poidsE = math.inf
            try:
                if self.robot.position[1] - 1 >= 0:
                    self.poidsW = self.robot.poids[self.robot.position[0]][self.robot.position[1] - 1]
                else:
                    self.poidsW = math.inf
            except:
                self.poidsW = math.inf
            self.poidsMin = min(self.poidsN, self.poidsS, self.poidsE, self.poidsW)
            if [self.poidsN, self.poidsS, self.poidsE, self.poidsW].count(self.poidsMin) == 1:
                if self.poidsN == self.poidsMin:
                    self.robot.move(card.Cardinals.NORTH)
                if self.poidsS == self.poidsMin:
                    self.robot.move(card.Cardinals.SOUTH)
                if self.poidsE == self.poidsMin:
                    self.robot.move(card.Cardinals.EAST)
                if self.poidsW == self.poidsMin:
                    self.robot.move(card.Cardinals.WEST)
            else:
                self.possibleMove = [card.Cardinals.NORTH if self.poidsN == self.poidsMin else None,
                                     card.Cardinals.SOUTH if self.poidsS == self.poidsMin else None,
                                     card.Cardinals.EAST if self.poidsE == self.poidsMin else None,
                                     card.Cardinals.WEST if self.poidsW == self.poidsMin else None]
                for loop in range(len(self.possibleMove)):
                    if self.possibleMove[loop] is not None:
                        if self.possibleMove == card.Cardinals.NORTH:
                            self.predictionPos = self.robot.position + [-1, 0]
                        elif self.possibleMove == card.Cardinals.SOUTH:
                            self.predictionPos = self.robot.position + [-1, 0]
                        elif self.possibleMove == card.Cardinals.EAST:
                            self.predictionPos = self.robot.position + [-1, 0]
                        elif self.possibleMove == card.Cardinals.WEST:
                            self.predictionPos = self.robot.position + [-1, 0]
                    try:
                        if self.robot.lastmove.index(
                                self.predictionPos) < self.futurPriority or self.futurPriority == -1:
                            self.futurPriority = self.robot.lastmove.index(self.predictionPos)
                            self.futurMove = self.possibleMove[loop]
                    except ValueError:
                        self.futurPriority = -1
                    self.predictionPos = []
                if self.futurMove is not None:
                    self.robot.move(self.futurMove)
                    self.futurMove = None
                else:
                    self.robot.randomMoveInSet(list(filter(lambda a: a is not None, self.possibleMove)))
        if self.robot.environment.grid[self.robot.position[0]][self.robot.position[1]].hasJewelry and not \
                self.robot.environment.grid[self.robot.position[0]][self.robot.position[1]].hasDust:
            self.robot.takejewels()
        elif self.robot.environment.grid[self.robot.position[0]][self.robot.position[1]].hasDust:
            self.robot.vacuum()
        self.poidsN = 0
        self.poidsS = 0
        self.poidsE = 0
        self.poidsW = 0
        self.poidsMin = 0
        self.predictionPos = []
        self.possibleMove = []
        self.futurMove = None
        self.futurPriority = -1

    def informe(self):
        if self.iteration == self.robot.maxiteration:
            self.stop()
            return
        self.robot.goToHighestReward(self.envthread)
        # self.robot.randomMove()
        xRobot, yRobot = self.robot.position

        if self.envthread.getenv().grid[xRobot][yRobot].hasDust:  # If room contains Dust (or Dust and Jewel)
            self.robot.vacuum()
        if self.envthread.getenv().grid[xRobot][yRobot].hasJewelry:
            self.robot.takejewels()
