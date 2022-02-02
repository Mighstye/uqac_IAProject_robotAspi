import time

import AIProject.enum.roomobjects as roomobj
import logging
import threading

import AIProject.threads.environmentthread as envithreads

if __name__ == "__main__":
    """Initialization"""

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Main      : Init")
    logging.info("Main      : Creating environment thread")
    environment = envithreads.environmentthread(threading.Lock())
    logging.info("Main      : Starting environment thread")
    environment.start()

    """Data Treatment"""
    grid = environment.getenv().grid
    visualgrid = [[[["☁", grid[i][j].inventory.count(roomobj.roomobjects.DUST)],
                    ["💎", grid[i][j].inventory.count(roomobj.roomobjects.JEWELRY)]] for j in range(5)] for i in
                  range(5)]
    logging.info("Main      : Visual Grid Initialized")


    def updatevisualgrid():
        logging.info("Main      : Updating Visual Grid...")
        visualgrid = [[[["☁", grid[i][j].inventory.count(roomobj.roomobjects.DUST)],
                        ["💎", grid[i][j].inventory.count(roomobj.roomobjects.JEWELRY)]] for j in range(5)] for i in
                      range(5)]
        logging.info("Main      : Visual Grid Updated !")


    def updateindividuals(i, j):
        logging.info("Main      : Performing individuals update for [", i, ",", j, "]")
        visualgrid[i][j] = [["☁", grid[i][j].inventory.count(roomobj.roomobjects.DUST)],
                            ["💎", grid[i][j].inventory.count(roomobj.roomobjects.JEWELRY)]]
        logging.info("Main      : Individual update performed !")


    updatevisualgrid()
    time.sleep(0.1)

    """Interface"""
    for line in visualgrid:
        for elem in line:
            print(elem, end=" | ")
        print()

    """Program end"""
    logging.info("Main      : Stopping environment thread.")
    environment.stop()
    time.sleep(0.1)
    logging.info("Main      : Main program stopped.")
