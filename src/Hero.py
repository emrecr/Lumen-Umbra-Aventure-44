# src/Hero.py
"""
Classe Hero - Personnage joueur avec système XP/niveaux.
Hérite de Personnage (vie, combat, arme/armure).
Compatible tests pytest + documentation officielle.
"""

from .Personnage import Personnage
import random
import math


class Hero(Personnage):
    """
    Représente le héros principal (joueur).
    
    Constructeur (doc officielle):
        Hero(nom: str, vie_max: int, force: int, arme: int=0, armure: int=0)
    
    Attributs spécifiques:
        - niveau: int = 1
        - exp: int = 0 (cumulatif)
    
    Inherited: nom, vie_max, vie, force, arme, armure
    """
    
    def __init__(self, nom: str, vie_max: int, force: int, arme: int = 0, armure: int = 0):
        """
        Initialise héros avec stats + système niveaux.
        """
        super().__init__(nom, vie_max, force, arme, armure)
        self.niveau = 1
        self.exp = 0

    @staticmethod
    def uniform(a: float, b: float) -> float:
        """
        Aléatoire pour tests (monkeypatch-able).
        """
        return random.uniform(a, b)

    def exp_pour_prochain_niveau(self) -> int:
        """
        Formule officielle: 100 * niveau^2 + 100 * niveau
        Ex: niv1=200, niv2=600, niv3=1200
        """
        n = self.niveau
        return 100 * n * n + 100 * n

    def monter_niveau(self) -> None:
        """
        Monte niveau + boost aléatoire 1-10% (ceil).
        Réinitialise vie = vie_max.
        Effets de bord (modifie état interne).
        """
        self.niveau += 1
        boost = 1 + self.uniform(0.01, 0.1)  # +1% à +10%
        self.vie_max = math.ceil(self.vie_max * boost)
        self.force = math.ceil(self.force * boost)
        self.vie = self.vie_max  # Doc officielle: vie réinitialisée

    def gagner_exp(self, exp: int) -> None:
        """
        XP cumulatif + montées multiples.
        Continue tant que exp >= prochain_seuil.
        Ignore exp <= 0.
        """
        if exp <= 0:
            return
        self.exp += exp  # Cumulatif (non consommé)
        while self.exp >= self.exp_pour_prochain_niveau():
            self.monter_niveau()
