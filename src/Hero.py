# src/Hero.py
"""
Classe Hero - Personnage joueur avec système XP/niveaux.
Hérite de Personnage (vie, combat, arme/armure).
Compatible tests pytest + documentation officielle.
"""

from .Personnage import Personnage
import random
import math


uniform = random.uniform

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
        return uniform(a, b)

    def exp_pour_prochain_niveau(self) -> int:
        """
        Formule officielle: 100 * niveau^2 + 100 * niveau
        Ex: niv1=200, niv2=600, niv3=1200
        """
        n = self.niveau
        return 100 * n * n + 100 * n

    def monter_niveau(self) -> None:
        self.niveau += 1
        pct_boost = self.uniform(1, 10) / 100
        boost = 1 + pct_boost
        
        self.vie_max = math.ceil(self.vie_max * boost)
        self.force = math.ceil(self.force * boost)
        self.vie = self.vie_max


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
