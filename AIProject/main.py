import time

import logging
import threading
from tkinter import *
import math

import AIProject.threads.environmentthread as envithreads
import AIProject.Node as Node

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

    fenetre = Tk()
    fenetre.geometry("900x900")

    frame_grille = Frame(fenetre, width=420, height=420)
    frame_grille.place(x=250, y=250)
    frame_grille.configure(bg='yellow')

    listOfUnlockyNode = []
    firstAstarStep = False

    def grilleConvertisseur():
        grille = []
        for ligne in range(5):
            ligneGrille = []
            for colonne in range(5):
                if environment.getenv().grid[ligne][colonne].hasDust and not environment.getenv().grid[ligne][colonne].hasJewelry:
                    ligneGrille.append("☁")
                if not environment.getenv().grid[ligne][colonne].hasDust and  environment.getenv().grid[ligne][colonne].hasJewelry:
                    ligneGrille.append("💎")
                if environment.getenv().grid[ligne][colonne].hasDust and  environment.getenv().grid[ligne][colonne].hasJewelry:
                    ligneGrille.append("☁💎")
                if not environment.getenv().grid[ligne][colonne].hasDust and not environment.getenv().grid[ligne][colonne].hasJewelry:
                    ligneGrille.append("0")
            grille.append(ligneGrille)
        return grille

    # def explorationAstar(coordonnees):
    #     listReturn = []
    #     listPoids = []
    #     H = 0
    #     xRobot = coordonnees[0]
    #     yRobot = coordonnees[1]
    #     for ligne in range(5):
    #         casePoids = []
    #         for colonne in range(5):
    #             w = 0
    #             if environment.getenv().grid[ligne][colonne].hasDust and not environment.getenv().grid[ligne][colonne].hasJewelry:
    #                 w = 6 + math.sqrt((ligne-yRobot)**2 + (colonne-xRobot)**2)
    #                 H+=1
    #             if environment.getenv().grid[ligne][colonne].hasJewelry and not environment.getenv().grid[ligne][colonne].hasDust:
    #                 w = 9 + math.sqrt((ligne-yRobot)**2 + (colonne-xRobot)**2)
    #                 H += 1
    #             if environment.getenv().grid[ligne][colonne].hasJewelry and environment.getenv().grid[ligne][colonne].hasDust:
    #                 w = 3 + math.sqrt((ligne-yRobot)**2 + (colonne-xRobot)**2)
    #                 H += 1
    #             casePoids.append(w)
    #         listPoids.append(casePoids)
    #     listReturn.append(H)
    #     listReturn.append(listPoids)
    #     return listReturn

    def explorationAstar(coordonnees, grille):
        listReturn = []
        listPoids = []
        H = 0
        xRobot = coordonnees[0]
        yRobot = coordonnees[1]
        for ligne in range(5):
            casePoids = []
            for colonne in range(5):
                w = 0
                if grille[ligne][colonne]=="☁":
                    w = math.sqrt((ligne-yRobot)**2 + (colonne-xRobot)**2) - 6
                    H+=1
                if grille[ligne][colonne]=="💎":
                    w = math.sqrt((ligne-yRobot)**2 + (colonne-xRobot)**2) - 9
                    H += 1
                if grille[ligne][colonne]=="☁💎":
                    w = math.sqrt((ligne-yRobot)**2 + (colonne-xRobot)**2) - 3
                    H += 1
                casePoids.append(w)
            listPoids.append(casePoids)
        listReturn.append(H)
        listReturn.append(listPoids)
        return listReturn


    def astar(coordonnees, listOfUnlockyNode, firstAstarStep, grille):
        listOfNode = []
        possibleMove = robot.possibleMove(coordonnees)
        luckyNode = 0
        firstNode = 0
        ordre = ""
        coupleNodeOrdre = []
        print("coups possible : "+str(possibleMove))

        for move in possibleMove:
            if move == "aller a droite":
                ordre = move
                print(coordonnees)
                coordonnees = [coordonnees[0]+1, coordonnees[1]]
                print(coordonnees)
                listReturn = explorationAstar(coordonnees, grille)
                # calcul de f
                f = listReturn[0] + listReturn[1][coordonnees[0]][coordonnees[1]] + 1
                # creation nouveau noeud
                node = Node.Node(coordonnees, f, possibleMove, grille)
                #ajout nouveau noeud a la liste
                coupleNodeOrdre = []
                coupleNodeOrdre.append(node)
                coupleNodeOrdre.append(ordre)
                listOfNode.append(coupleNodeOrdre)
            if move == "aller a gauche":
                ordre = move
                coordonnees = [coordonnees[0]-1, coordonnees[1]]
                listReturn = explorationAstar(coordonnees, grille)
                f = listReturn[0] + listReturn[1][coordonnees[0]][coordonnees[1]] + 1
                node = Node.Node(coordonnees, f, possibleMove, grille)
                coupleNodeOrdre = []
                coupleNodeOrdre.append(node)
                coupleNodeOrdre.append(ordre)
                listOfNode.append(coupleNodeOrdre)
            if move == "aller en haut":
                ordre = move
                coordonnees = [coordonnees[0], coordonnees[1]+1]
                listReturn = explorationAstar(coordonnees, grille)
                f = listReturn[0] + listReturn[1][coordonnees[0]][coordonnees[1]] + 1
                node = Node.Node(coordonnees, f, possibleMove, grille)
                coupleNodeOrdre = []
                coupleNodeOrdre.append(node)
                coupleNodeOrdre.append(ordre)
                listOfNode.append(coupleNodeOrdre)
            if move == "aller en bas":
                ordre = move
                coordonnees = [coordonnees[0], coordonnees[1]-1]
                listReturn = explorationAstar(coordonnees, grille)
                f = listReturn[0] + listReturn[1][coordonnees[0]][coordonnees[1]] + 1
                node = Node.Node(coordonnees, f, possibleMove, grille)
                coupleNodeOrdre = []
                coupleNodeOrdre.append(node)
                coupleNodeOrdre.append(ordre)
                listOfNode.append(coupleNodeOrdre)
        #Selection du prochain noeud
        f1 = listOfNode[0][0].f
        orderPrime = ""
        for couple in listOfNode:
            print(f1)
            if couple[0].f <= f1:
                f1 = couple[0].f
                orderPrime = couple[1]
        for couple in listOfNode:
            if couple[0].f >= f1:
                listOfUnlockyNode.append(couple)
        for couple in listOfNode:
            if couple[1] == orderPrime:
                luckyNode = couple
                print(luckyNode)
        luckyNode[0].grille[luckyNode[0].coordonnees[0]][luckyNode[0].coordonnees[1]] = "0"
        print(str(luckyNode[0].coordonnees[0]) + " " + str(luckyNode[0].coordonnees[1]))

        if firstAstarStep:
            firstNodeOrdre = luckyNode[1]
            firstAstarStep = True
        # for couple in listOfUnlockyNode:
        #     if couple[0].f < f1:
        #         print("ouiiii")
        #         luckyNode = couple

        #condition d'arret et appel récursif
        if listReturn[0] == 0 and firstAstarStep:
            return firstNodeOrdre
        else:
            print("order : "+luckyNode[1])
            print("H = "+str(listReturn[0]))
            print("x = " + str(luckyNode[0].coordonnees[0]) + " y = " + str(luckyNode[0].coordonnees[1]))
            print(grille)
            astar(luckyNode[0].coordonnees, listOfUnlockyNode, firstAstarStep, luckyNode[0].grille)



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

    robot = environment.getenv().putrobot()

    """Interface"""
    # --> Tkinter

    while True:
        tkinterwindowsupdate()
        #explorationAstar(robot.position)
        ordre = astar(robot.position, listOfUnlockyNode, firstAstarStep, grilleConvertisseur())
        print(ordre)
        fenetre.update_idletasks()
        fenetre.update()


    """Program end"""
    # End of the program
    # We stop the different thread
    logging.info("Main      : Stopping environment thread.")
    environment.stop()
    time.sleep(0.1)  # Little time sleep to have a clear console display (Might get removed)
    logging.info("Main      : Main program stopped.")
