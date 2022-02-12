import logging
import threading


class robotthread(threading.Thread):
    stopsignal = False

    def __init__(self, mutex, robot):
        self.mutex = mutex
        self.robot = robot
        threading.Thread.__init__(self)
        logging.info("Robot Thread  : Initialized.")

    def run(self):
        logging.info("Robot Thread  : Started.")
        while not self.stopsignal:
            self.robot.deepSearch()

        logging.info("Robot Thread  : Stopped.")

    def stop(self):
        logging.info("Robot Thread  : Stop signal sent to Robot Thread")
        self.stopsignal = True