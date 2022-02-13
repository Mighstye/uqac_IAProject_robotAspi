import time
import logging
import threading
import AIProject.threads.environmentthread as envthread

class robotthread(threading.Thread):
    stopsignal = False

    def __init__(self, mutex, robot, envthread):
        time.sleep(0.5)
        self.mutex = mutex
        self.robot = robot
        self.envthread = envthread
        threading.Thread.__init__(self)
        logging.info("Robot Thread  : Initialized.")

    def run(self):
        logging.info("Robot Thread  : Started.")
        while not self.stopsignal:
            self.robot.goToHighestReward(self.envthread)
            # self.robot.randomMove()
            xRobot,yRobot = self.robot.position

            #if envthread.environmentthread.getenv(self).getGrid()[xRobot][yRobot].hasDust: # If room contains Dust (or Dust and Jewel)
            #    self.robot.vacuum()
            #if envthread.environmentthread.getenv(self).getGrid()[xRobot][yRobot].hasJewelry:
            #    self.robot.takejewels()

            time.sleep(3)
        logging.info("Robot Thread  : Stopped.")

    def stop(self):
        logging.info("Robot Thread  : Stop signal sent to Robot Thread")
        self.stopsignal = True

    def BellmanFord(self):
        #TODO shit happening here
        logging.info("A faire")

