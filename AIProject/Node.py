import AIProject.environment.env as env
class Node:

    coordonnees = []
    move = ""
    grille = []
    f = 0

    def __init__(self, coordonnees, f, move, grille):
        self.coordonnees = coordonnees
        self.f = f
        self.move = move
        self.grille = grille
