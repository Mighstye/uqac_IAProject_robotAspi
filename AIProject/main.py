import logging
import threading
from tkinter import *
import time

import AIProject.threads.environmentthread as envithreads
import AIProject.threads.robotthread as robotthread

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
    # Starting the environment thread (It actually runs the run() method of the thread

    robot = environment.getenv().putrobot()
    robotT = robotthread.robotthread(threading.Lock(), robot)
    environment.start()
    robotT.start()

    visualgrid = [[["☁" if environment.getenv().grid[i][j].hasDust == True else " ",
                    "💎" if environment.getenv().grid[i][j].hasJewelry == True else " ",
                    "🤖" if environment.getenv().grid[i][j].robothere == True else " "] for j in range(5)] for i in range(5)]

    """Data Treatment"""
    # Here, we will treat the environmental data
    # to be able to put these in a UI
    grid = environment.getenv().grid  # We get the grid of the environment

    fenetre = Tk()
    fenetre.geometry("900x900")

    frame_grille = Frame(fenetre, width=420, height=420)
    frame_grille.place(x=250, y=250)
    frame_grille.configure(bg='yellow')

    def tkinterwindowsupdate():
        newlist = []
        for ligne in range(5):
            text = ""
            list_ligne_label = []
            for colonne in range(5):
                if environment.getenv().grid[ligne][colonne].hasDust:
                    text += "☁"
                if environment.getenv().grid[ligne][colonne].hasJewelry:
                    text += "💎"
                if environment.getenv().grid[ligne][colonne].robothere:
                    text += "🤖"
                label = Label(master=frame_grille, text=text, borderwidth=1, relief="raised", width=10, height=5)
                label.grid(row=ligne, column=colonne)
                list_ligne_label.append(label)
                text = ""
            newlist.append(list_ligne_label)
        return newlist

    """Interface"""
    # --> Tkinter

    while True:
        visualgrid = [[["☁" if environment.getenv().grid[i][j].hasDust == True else " ",
                        "💎" if environment.getenv().grid[i][j].hasJewelry == True else " ",
                        "🤖" if environment.getenv().grid[i][j].robothere == True else " "] for j in range(5)] for i in
                      range(5)]
        for ligne in visualgrid:
            for elem in ligne:
                print(elem, end=" | ")
            print()
        print("--------------------------------------------")
        tkinterwindowsupdate()
        fenetre.update_idletasks()
        fenetre.update()
        time.sleep(1)

    """Program end"""
    # End of the program
    # We stop the different thread
    logging.info("Main      : Stopping environment thread.")
    environment.stop()
    time.sleep(0.1)  # Little time sleep to have a clear console display (Might get removed)
    logging.info("Main      : Main program stopped.")
