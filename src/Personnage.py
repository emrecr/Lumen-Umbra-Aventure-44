import random

class Personnage:
    """
    Classe de base représentant un combattant.
    
    Attributes:
        nom (str): Nom du personnage.
        vie_max (int): Points de vie maximum.
        vie (int): Points de vie actuels.
        force (int): Force du personnage.
        arme (int): Dégâts de l'arme.
        armure (int): Points de défense.
    """

    def __init__(self, nom: str, vie_max: int, force: int, arme: int, armure: int):
        self.nom = nom
        self.vie_max = vie_max
        self.vie = vie_max
        self.force = force
        self.arme = arme
        self.armure = armure

    def est_vivant(self) -> bool:
        """Indique si le personnage a encore des PV."""
        return self.vie > 0

    def subir_degats(self, valeur: int) -> int:
        """Applique les dégâts et retourne la valeur réelle retirée."""
        degats_reels = max(0, valeur)
        self.vie -= degats_reels
        if self.vie < 0:
            self.vie = 0
        return degats_reels

    def calcul_degats_sur(self, cible) -> int:
        """Calcule les dégâts selon la formule du cahier des charges."""
        multiplicateur = random.uniform(0.8, 1.2)
        degats = (self.force + self.arme) * multiplicateur - cible.armure
        return int(max(0, degats))

    def attaquer(self, cible) -> int:
        """Exécute une attaque sur une cible."""
        degats = self.calcul_degats_sur(cible)
        return cible.subir_degats(degats)