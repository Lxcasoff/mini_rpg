import random

class Personnage:
    def __init__(self, nom, sexe, classe):
        self.nom = nom
        self.sexe = sexe
        self.classe = classe
        self.potion_utilisee = False

        if classe == "G": #guerrier
            self.degats = 8
            self.points_de_vie = 50
        elif classe == "M": #mage
            self.degats = 16
            self.points_de_vie = 25
        elif classe == "A": #archer
            self.degats = 13
            self.points_de_vie = 35

    def attaquer(self, ennemi):
        ennemi.points_de_vie -= self.degats
        print(f"{self.nom} attaque {ennemi.nom} et lui inflige {self.degats} points de dégâts!")

    def utiliser_potion(self):
        if not self.potion_utilisee:
            self.points_de_vie += 15
            self.potion_utilisee = True
            print(f"{self.nom} utilise une potion et récupère 15 points de vie!")
        else:
            print("La potion est déjà utilisée!")

class Ennemi:
    def __init__(self, nom, sexe, degats, points_de_vie):
        self.nom = nom
        self.sexe = sexe
        self.degats = degats
        self.points_de_vie = points_de_vie

    def attaquer(self, personnage):
        personnage.points_de_vie -= self.degats
        print(f"{self.nom} attaque {personnage.nom} et lui inflige {self.degats} points de dégâts!")

    def passer_tour(self):
        print(f"{self.nom} passe son tour.")

def sauvegarder(personnage, ennemis):
    with open("save.txt", "w") as f:
        f.write(f"{personnage.nom},{personnage.sexe},{personnage.classe},{personnage.degats},{personnage.points_de_vie},{personnage.potion_utilisee}\n")
        for ennemi in ennemis:
            f.write(f"{ennemi.nom},{ennemi.sexe},{ennemi.degats},{ennemi.points_de_vie}\n")

def charger():
    with open("save.txt", "r") as f:
        lines = f.readlines()

    personnage_data = lines[0].strip().split(',')
    personnage = Personnage(personnage_data[0], personnage_data[1], personnage_data[2])
    personnage.degats = int(personnage_data[3])
    personnage.points_de_vie = int(personnage_data[4])
    personnage.potion_utilisee = personnage_data[5] == 'True'

    ennemis = []
    for line in lines[1:]:
        ennemi_data = line.strip().split(',')
        ennemi = Ennemi(ennemi_data[0], ennemi_data[1], int(ennemi_data[2]), int(ennemi_data[3]))
        ennemis.append(ennemi)

    return personnage, ennemis

def main():
    nom = input("Entrez le nom de votre personnage: ")
    sexe = input("Entrez le sexe de votre personnage (M / F / Dragon celeste : D): ")
    if sexe == "D":
        print("AH Dommage... Fin de la partie!\n")
        return main()
    classe = input("Choisissez une classe (Guerrier : G / Mage : M / Archer : A): ")
    personnage = Personnage(nom, sexe, classe)

    ennemis = [
        Ennemi("ennemie 1", "M", 5, 30),
        Ennemi("ennemie 2", "F", 3, 15),
        Ennemi("ennemie 3", "M", 6, 17)
    ]

    while personnage.points_de_vie > 0 and any(e.points_de_vie > 0 for e in ennemis):
        choix = input("Que voulez-vous faire? (Attaquer : A / Potion : P): ")
        if choix == "A":
            cible = int(input("Quel ennemi voulez-vous attaquer? (1/2/3): "))
            personnage.attaquer(ennemis[cible-1])
        elif choix == "P":
            personnage.utiliser_potion()

        
        for ennemi in ennemis:
            if ennemi.points_de_vie <= 0:
                continue
            action = random.choice(["attaquer", "passer"])
            if action == "attaquer":
                ennemi.attaquer(personnage)
            else:
                ennemi.passer_tour()

        sauvegarder(personnage, ennemis)
    

    print("Fin de la partie!")

if __name__ == "__main__":
    main()

