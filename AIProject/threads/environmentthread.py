import logging
import AIProject.environment.env as env
import threading


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
            """Things happening here !"""
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
