from math import cos, sin, pi
from time import time


def formule_rotation(a, b, c, angle):
    return a * int(cos(angle)) - b * int(sin(angle)), a * int(sin(angle)) + b * int(cos(angle)), c

def conversion_to_base5(iCoord):
    return iCoord[0]*25 + iCoord[1]*5 + iCoord[2]

def conversion_to_coord(iCase):
    iCoord = [0,0,0]
    for i in range(2, -1, -1):
        iCoord[i] = iCase % 5 
        iCase //= 5
    return iCoord

def arrangement():
    selon_coordonnee = [[] for _ in range(125)]
    for iPiece, piece in enumerate(positions):  
        for iCoord in piece:    
            iCase = conversion_to_base5(iCoord)
            #print(iCoord, iCase)
            selon_coordonnee[iCase].append(iPiece)
    return selon_coordonnee

def arrangement_bis():
    selon_coordonnee = [[] for _ in range(125)]
    for i in range(125):
        icase = conversion_to_coord(i)
        for iPiece, piece in enumerate(positions):
            if icase in piece:
                selon_coordonnee[i].append(iPiece)
    return selon_coordonnee



def translate_x(piece, distance): # on définit la fonction qui réalise une translation de la pièce parallèle à l'axe x
        p = []
        for i in range(len(piece)):
            p.append([piece[i][0] + distance, piece[i][1], piece[i][2]])
        return p

def translate_y(piece, distance): # on définit la fonction qui réalise une translation de la pièce parallèle à l'axe y
    p = []
    for i in range(len(piece)):
        p.append([piece[i][0], piece[i][1] + distance, piece[i][2]])
    return p

def translate_z(piece, distance): # on définit la fonction qui réalise une translation de la pièce parallèle à l'axe z
    p = []
    for i in range(len(piece)):
        p.append([piece[i][0], piece[i][1], piece[i][2] + distance])
    return p


def rotation_xy(piece, n): # on définit la fonction qui réalisise une rotation sens horaire, 90°, 180°, 270°
    p = []
    angle  = n*pi/2
    for i in range(len(piece)):
        p.append([piece[i][0] * int(cos(angle)) - piece[i][1]* int(sin(angle)), \
                    piece[i][0] * int(sin(angle)) + piece[i][1]* int(cos(angle)), \
                    piece[i][2]])
    return p

def rotation_yz(piece, n): # sens horaire si on regarde la piece par derrière
    p = []
    angle  = n*pi/2
    for i in range(len(piece)):
        p.append([piece[i][0], \
                    piece[i][1] * int(cos(angle)) - piece[i][2]* int(sin(angle)), \
                    piece[i][1] * int(sin(angle)) + piece[i][2]* int(cos(angle))])
    return p

def rotation_zx(piece, n): # sens anti-horaire
    p = []
    angle  = n*pi/2
    for i in range(len(piece)):
        p.append([piece[i][2] * int(sin(angle)) + piece[i][0]* int(cos(angle)), \
                    piece[i][1], \
                    piece[i][2] * int(cos(angle)) - piece[i][0]* int(sin(angle))])
    return p
def verif_coordonnees(piece):
    for x, y, z in piece:
        if not (0 <= x <= 4 and 0 <= y <= 4 and 0 <= z <= 4):
            return False
    return True

def trouve_position(piece): # On définit la fonction qui détermine toutes les positions possibles d'une pièce pour un cube vide
        possibilite = []
        for tx in range(-4, 5):
            nv_position1 = translate_x(piece, tx)
            for ty in range(-4, 5):
                nv_position2 = translate_y(nv_position1, ty)
                for tz in range(-4, 5):
                    nv_position3 = translate_z(nv_position2, tz)
                    for rxy in range(4):
                        nv_position4 = rotation_xy(nv_position3, rxy)
                        for ryz in range(4):
                            nv_position5 = rotation_yz(nv_position4, ryz)
                            for rzx in range(4):
                                nv_position6 = rotation_zx(nv_position5, rzx)
                                if verif_coordonnees(nv_position6):
                                    nv_position6.sort()
                                    if nv_position6 not in possibilite:
                                        possibilite.append(nv_position6)
        return possibilite

p1 = [[0,0,0], [1,0,0], [1,1,0], [2,0,0], [3,0,0]]
positions = sorted(trouve_position(p1))


class Cube:

    def __init__(self, coordonnees):
        self.coord = coordonnees

    def remplir(self, iPiece): # insere une piece transformée
        for x, y, z in positions[iPiece]:
            self.coord[x][y][z] = False

    def vider(self, iPiece): # retire la piece transformée
        for x, y, z in positions[iPiece]:
            self.coord[x][y][z] = True

    def piece_possible(self, iPiece):
        for x, y, z in positions[iPiece]:
            if not self.coord[x][y][z]:
                return False
        return True
    
    def recherche_case_vide(self):

        for iCase in range(125):
            x, y, z = conversion_to_coord(iCase)
            if self.coord[x][y][z]:
                return iCase
        return -1
        


    def solution(self, nb_pieces): # fonction recursive qui explore toutes les combinaisons possibles
        if nb_pieces == 25:
            return []
        iCase = self.recherche_case_vide()
        if iCase >= 0:           
            for iPiece in selon_coordonnee[iCase]:            
                if self.piece_possible(iPiece):
                    self.remplir(iPiece)
                    s = self.solution(nb_pieces+1) #on renvoit nv_position
                    if s is not None:
                        return [iPiece] + s
                    self.vider(iPiece)
            return None
        return None
selon_coordonnee = arrangement()
cube = Cube([[[True]*5 for i in range(5)] for i in range(5)] )

def principal():
    
    resultat = cube.solution(0)
    return resultat

if __name__ == "__main__":
    debut = time()
    
    resultat = principal()
  
    
    for i, iPiece in enumerate(sorted(resultat)):
        print('La piece p' + str(i+1), 'a pour coordonnées', positions[iPiece])

    print('\n\nAfficher coupe cube\n')
    for x in cube.coord:
        for y in x:
            print(*y)
        print()
        print()

    verification = Cube([[[True]*5 for i in range(5)] for i in range(5)])
    for iPiece in resultat:
        verification.remplir(iPiece)

    print('\n\nAfficher coupe Verfication\n')
    for x in cube.coord:
        for y in x:
            print(*y)
        print()
        print()


    fin = time()
    print('Le résultat a été affiché en',round(fin - debut, 2),'secondes')
    