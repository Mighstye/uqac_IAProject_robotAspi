import time

import logging
import threading

import AIProject.threads.environmentthread as envithreads

if __name__ == "__main__":
    """Initialization"""

    # Logging format
    # To use logging :
    # logging.info(message)
    # logging.warning(message)
    # logging.error(message)
    # Please do use logging :)
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Main      : Init")
    logging.info("Main      : Creating environment thread")
    # Creation of the environment thread
    environment = envithreads.environmentthread(threading.Lock())
    logging.info("Main      : Starting environment thread")
    # Starting the environment thread (It actually runs the run() method of the thread)
    environment.start()

    """Data Treatment"""
    # Here, we will treat the environmental data
    # to be able to put these in a UI
    grid = environment.getenv().grid  # We get the grid of the environment
    # We create a visualgrid of the previous grid
    # The visualgrid consist of different string (Two per rooms)
    visualgrid = [[["☁" if grid[j][i].hasDust == True else " ",
                    "💎" if grid[j][i].hasJewelry == True else " "] for j in range(5)] for i in range(5)]
    logging.info("Main      : Visual Grid Initialized")


    def updatevisualgrid():
        # This method should be used to update the whole visual grid
        # Use this if major change happened to the env grid
        newgrid = environment.getenv().grid
        logging.info("Main      : Updating Visual Grid...")
        newvisualgrid = [[["☁" if newgrid[j][i].hasDust == True else " ",
                           "💎" if newgrid[j][i].hasJewelry == True else " "] for j in range(5)] for i in range(5)]
        logging.info("Main      : Visual Grid Updated !")
        return newvisualgrid


    def updateindividuals(i, j):  # TODO debug
        newvisualgrid = []
        # This method should be used to update a single room in the visual grid
        # Use this if only few rooms have changed, and if you know perfectly which rooms changed
        newgrid = environment.getenv().grid
        logging.info("Main      : Performing individuals update for [", i, ",", j, "]")
        newvisualgrid[i][j] = [["☁" if grid[j][i].hasDust == True else " ",
                                "💎" if grid[j][i].hasJewelry == True else " "]]
        logging.info("Main      : Individual update performed !")


    # Little time sleep to have a clear console display (Might get removed)
    time.sleep(0.1)

    """Interface"""
    # Displaying the visualgrid in the console atm
    # But we should on a way to display it in a UI
    # --> Tkinter

    """while True:
        visualgrid = updatevisualgrid()
        for list in visualgrid:
            for elem in list:
                print(elem, end=" | ")
            print("")
        time.sleep(5)
    """

    """Program end"""
    # End of the program
    # We stop the different thread
    logging.info("Main      : Stopping environment thread.")
    environment.stop()
    time.sleep(0.1)  # Little time sleep to have a clear console display (Might get removed)
    logging.info("Main      : Main program stopped.")
