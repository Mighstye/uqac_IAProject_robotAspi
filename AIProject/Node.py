import AIProject.environment.env as env
class Node:

    coordonnees = []
    possibleMove = []
    grille = []
    f = 0

    def __init__(self, coordonnees, f, possibleMove, grille):
        self.coordonnees = coordonnees
        self.f = f
        self.possibleMove = possibleMove
        self.grille = grille
