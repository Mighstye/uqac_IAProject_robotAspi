import logging
import AIProject.environment.env as env
import threading


class environmentthread(threading.Thread):
    stopsignal = False

    def __init__(self, mutex):
        self.mutex = mutex
        self.env = env.env()
        threading.Thread.__init__(self)
        logging.info("Environment Thread    : Initialized")

    def run(self):
        logging.info("Environment Thread    : Started !")
        while not self.stopsignal:
            """Things happening here !"""
        logging.info("Environment Thread    : Stopped.")

    def stop(self):
        logging.info("Stop signal sent to Environment Thread")
        self.stopsignal = True

    def getenv(self):
        return self.env