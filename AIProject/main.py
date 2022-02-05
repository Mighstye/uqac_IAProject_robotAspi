import time

import AIProject.enum.roomobjects as roomobj
import logging
import threading
import AIProject.environment.room as room
from tkinter import *

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
    visualgrid = [[[["☁", grid[i][j].inventory.count(roomobj.roomobjects.DUST)],
                    ["💎", grid[i][j].inventory.count(roomobj.roomobjects.JEWELRY)]] for j in range(5)] for i in
                  range(5)]
    logging.info("Main      : Visual Grid Initialized")


    def updatevisualgrid(fenetre):
        # This method should be used to update the whole visual grid
        # Use this if major change happened to the env grid
        newgrid = environment.getenv().grid
        logging.info("Main      : Updating Visual Grid...")
        newvisualgrid = [[[["☁", newgrid[i][j].inventory.count(roomobj.roomobjects.DUST)],
                           ["💎", newgrid[i][j].inventory.count(roomobj.roomobjects.JEWELRY)]] for j in range(5)] for i
                         in
                         range(5)]
        logging.info("Main      : Visual Grid Updated !")
        print(visualgrid[1][1])
        for ligne in range(5):
            for colonne in range(5):
                if newvisualgrid[ligne][colonne][0][1] == 1 and newvisualgrid[ligne][colonne][1][1] == 0:
                    Label(fenetre, text="☁", borderwidth=1).grid(row=ligne, column=colonne)
                if newvisualgrid[ligne][colonne][0][1] == 1 and newvisualgrid[ligne][colonne][1][1] == 1:
                    Label(fenetre, text="☁💎", borderwidth=1).grid(row=ligne, column=colonne)
                if newvisualgrid[ligne][colonne][0][1] == 0 and newvisualgrid[ligne][colonne][1][1] == 1:
                    Label(fenetre, text="💎", borderwidth=1).grid(row=ligne, column=colonne)
                if newvisualgrid[ligne][colonne][0][1] == 0 and newvisualgrid[ligne][colonne][1][1] == 0:
                    Label(fenetre, text=" ", borderwidth=1).grid(row=ligne, column=colonne)
        return newvisualgrid


    def updateindividuals(i, j):  # TODO debug
        newvisualgrid = []
        # This method should be used to update a single room in the visual grid
        # Use this if only few rooms have changed, and if you know perfectly which rooms changed
        newgrid = environment.getenv().grid
        logging.info("Main      : Performing individuals update for [", i, ",", j, "]")
        newvisualgrid[i][j] = [["☁", newgrid[i][j].inventory.count(roomobj.roomobjects.DUST)],
                               ["💎", newgrid[i][j].inventory.count(roomobj.roomobjects.JEWELRY)]]
        logging.info("Main      : Individual update performed !")


    fenetre = Tk()
    visualgrid = updatevisualgrid(fenetre)

    # Little time sleep to have a clear console display (Might get removed)
    time.sleep(0.1)

    """Interface"""
    # Displaying the visualgrid in the console atm
    # But we should on a way to display it in a UI
    # --> Tkinter

    visualgrid = updatevisualgrid(fenetre)
    for list in visualgrid:
        for elem in list:
            print(elem, end=" | ")
        print("")

    fenetre.mainloop()

    """Program end"""
    # End of the program
    # We stop the different thread
    logging.info("Main      : Stopping environment thread.")
    environment.stop()
    time.sleep(0.1)  # Little time sleep to have a clear console display (Might get removed)
    logging.info("Main      : Main program stopped.")
