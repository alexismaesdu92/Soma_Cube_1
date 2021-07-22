# Créé par alexi, le 14/07/2021 en Python 3.7

from math import cos, sin, pi
from time import time

def formule_rotation(a, b, c):
    return - b , a, c

class Piece:

    def __init__(self, blocs):
        self.blocs = blocs

    def translate_x(self, distance): # on définit la fonction qui réalise une translation de la pièce parallèle à l'axe x
        for bloc in self.blocs:
            bloc[0] += distance

    def translate_y(self, distance): # on définit la fonction qui réalise une translation de la pièce parallèle à l'axe y
        for bloc in self.blocs:
            bloc[1] += distance

    def translate_z(self, distance): # on définit la fonction qui réalise une translation de la pièce parallèle à l'axe z
        for bloc in self.blocs:
            bloc[2] += distance

    def rotation_xy(self): # on définit la fonction qui réalisise une rotation sens horaire, 90°, 180°, 270°
        for i, bloc in enumerate(self.blocs):
            x, y, z = -bloc[1], bloc[0], bloc[2] 
            self.blocs[i] = [x, y, z]

    def rotation_yz(self): # sens horaire si on regarde la coord par derrière
        for i, bloc in enumerate(self.blocs):
            x, y, z = bloc[0], -bloc[2], bloc[1]
            self.blocs[i] = [z, x, y]

    def rotation_zx(self): # sens anti-horaire
        for i, bloc in enumerate(self.blocs):
            x, y, z = bloc[2], bloc[1], -bloc[0]
            self.blocs[i] = [y, z, x]

    def verif_coordonnees(self):
        for x, y, z in self.blocs:
            if not (0 <= x <= 4 and 0 <= y <= 4 and 0 <= z <= 4):
                return False
        return True
    '''
    Essayer dans la fonction ci-dessous de réduire le nombre d'opérations. --> retirer les opérations inverses
    Pour les rotations, faire le sens inverse
    '''
    '''
    Changer l'ordre des operations pour ne pas faire les -d. Si sela est possible, possibilité de virer l'argument!
    '''
    def trouve_position(self): # On définit la fonction qui détermine toutes les positions possibles d'une pièce pour un cube vide
        possibilite = []
        for tx in range(-4, 5):
            self.translate_x(tx)
            for ty in range(-4, 5):
                self.translate_y(ty)
                for tz in range(-4, 5):
                    self.translate_z(tz)
                    for rxy in range(4):
                        self.rotation_xy()
                        for ryz in range(4):
                            self.rotation_yz()
                            for rzx in range(4):
                                self.rotation_zx()
                                if self.verif_coordonnees():
                                    nv_position = sorted(self.blocs)
                                    if nv_position not in possibilite:
                                        possibilite.append(nv_position)
                    self.translate_z(-tz)
                self.translate_y(-ty)
            self.translate_x(-tx)
        return possibilite

class Cube:

    def __init__(self, coordonnees):
        self.coord = coordonnees

    def remplir(self, piece): # insere une piece transformée
        for x, y, z in piece:
            self.coord[x][y][z] = False

    def vider(self, piece): # retire la piece transformée
        for x, y, z in piece:
            self.coord[x][y][z] = True

    def piece_possible(self, piece):
        for x, y, z in piece:
            if not self.coord[x][y][z]:
                return False
        return True
    
    def actualisation_position(self, position):
        nv_position = []
        for piece in position:
            if self.piece_possible(piece):
                nv_position.append(piece)  
        return nv_position


    def solution(self, positions, nb_pieces): # fonction recursive qui explore toutes les combinaisons possibles

        if nb_pieces == 20:
            return []
             
        positions = self.actualisation_position(positions)
        for piece in positions:
            if self.piece_possible(piece):
                self.remplir(piece)
                s = self.solution(positions, nb_pieces+1) #on renvoit nv_position
                if s is not None:
                    return [piece] + s
                self.vider(piece)
        return None

def principal():
    p1 = Piece([[0,0,0], [1,0,0], [1,1,0], [2,0,0], [3,0,0]])
    positions = p1.trouve_position()

    cube = Cube([[[True]*5 for i in range(5)] for i in range(5)] )

    resultat = cube.solution(positions, 0)
    return resultat

if __name__ == "__main__":
  debut = time()

  resultat = principal()

  for i, piece in enumerate(sorted(resultat)):
    print('La piece p' + str(i+1), 'a pour coordonnées', piece)

  fin = time()
  print('Le résultat a été affiché en',round(fin - debut, 2),'secondes')
