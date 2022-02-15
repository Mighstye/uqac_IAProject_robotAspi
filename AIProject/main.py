import logging
import threading
from tkinter import *
import time

import AIProject.threads.environmentthread as envithreads
import AIProject.threads.robotthread as robotthread

if __name__ == "__main__":
    """Initialization"""
    mode = ""
    while not(mode == "0" or mode == "1"):
        mode = input("Version du robot ? \n 0 : Non informé \n 1 : Informé \n")
    iteration = ""
    while not(iteration.isdigit()):
        iteration = input("Combien d'itération ? \n")

    stopSignal = False
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
    robotT = robotthread.robotthread(threading.Lock(), robot, mode, environment, int(iteration))
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
        label1 = Label(master=fenetre, text="Poussières aspirées : "+str(robot.poussiere), width=20, height=3, font=(30))
        label2 = Label(master=fenetre, text="Bijoux récupérés    : "+str(robot.bijoux), width=20, height=3, font=(30))
        label3 = Label(master=fenetre, text="Bijoux perdu        : " +str(robot.erreur), width=20, height=3, font=(30))
        label1.configure(fg='green')
        label2.configure(fg='blue')
        label3.configure(fg='red')
        label1.grid(row=0, column=0)
        label2.grid(row=1, column=0)
        label3.grid(row=2, column=0)
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
                label = Label(master=frame_grille, text=text, borderwidth=1, relief="solid", width=10, height=5)
                label.grid(row=ligne, column=colonne)
                list_ligne_label.append(label)
                text = ""
            newlist.append(list_ligne_label)
        return newlist

    """Interface"""
    # --> Tkinter

    while not stopSignal:
        for widget in frame_grille.winfo_children():
            widget.destroy()
        if not environment.is_alive():
            stopSignal = True
        tkinterwindowsupdate()
        fenetre.update_idletasks()
        fenetre.update()
        time.sleep(0.5)

    """Program end"""
    # End of the program
    fenetre.destroy()
    time.sleep(0.1)  # Little time sleep to have a clear console display (Might get removed)
    logging.info("Main      : Main program stopped.")
